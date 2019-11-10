from traceback import print_exc
import sys

_enable_callback_tracebacks = False

def enable_callback_tracebacks(flag):
    global _enable_callback_tracebacks
    _enable_callback_tracebacks = flag

from ctypes import (
    PYFUNCTYPE, POINTER, sizeof, cast, string_at,
    c_int, c_void_p, py_object, c_char_p)

from ._sqlite3 import (
    SQLITE_DENY,
    SQLITE_ABORT,
    sqlite3_value,
    sqlite3_result,
    sqlite3_user_data,
    sqlite3_result_error,
    sqlite3_result_error_code,
    sqlite3_aggregate_context)

from .exc import (
    PyErr_SetExcInfo,
    PyObject,
    throw)


class ExcWrapper:

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.exception = (exc_type, exc_value, exc_tb)
        return True

def wraps_exception(func):
    def wrapper(ctx, *args):
        with ExcWrapper() as cm:
            func(ctx, *args)
        exc_type, exc_value, exc_tb = cm.exception
        if exc_type is not None:
            sqlite3_result_error_code(ctx, SQLITE_ABORT)
            PyErr_SetExcInfo(exc_type, exc_value, exc_tb)

    return wrapper


@PYFUNCTYPE(c_int, py_object, c_int, c_void_p, c_int, c_void_p)
def _collation_callback(p, lena, pa, lenb, pb):
    r = p(string_at(pa, lena).decode(), string_at(pb, lenb).decode())
    return (r > 0) - (r < 0)


def _decode(x):
    return None if x is None else x.decode()

@PYFUNCTYPE(c_int, py_object, c_int, c_char_p, c_char_p, c_char_p, c_char_p)
def _authorizer_callback(callback, action, arg1, arg2, dbname, source):
    try:
        ret = callback(action, _decode(arg1), _decode(arg2), _decode(dbname), _decode(source))
        if type(ret) is int and ret <= 2:
            return ret
        return SQLITE_DENY
    except Exception:
        return SQLITE_DENY

@PYFUNCTYPE(c_int, py_object)
def _progress_handler(handler):
    return handler()

# @PYFUNCTYPE(c_int, c_uint, py_object, c_void_p, c_void_p)
# def _trace_callback(trace_type, callback, stmt, sql):
#     callback(string_at(sql).decode())
#     return 0

@PYFUNCTYPE(None, py_object, c_char_p)
def _trace_callback(callback, sql):
    callback(sql.decode())


@PYFUNCTYPE(None, c_void_p, c_int, POINTER(c_void_p))
@wraps_exception
def _function_callback(ctx, argc, argv):
    args = tuple(sqlite3_value(argv[i]) for i in range(argc))
    callback = cast(sqlite3_user_data(ctx), py_object).value
    try:
        ret = callback(*args)
    except Exception:
        if _enable_callback_tracebacks:
            print_exc()
        sqlite3_result_error(ctx, b"user-defined function raised exception", -1)
    else:
        sqlite3_result(ctx, ret)


@PYFUNCTYPE(None, c_void_p, c_int, POINTER(c_void_p))
@wraps_exception
def _aggregate_step(ctx, argc, argv):
    instance = py_object.from_address(sqlite3_aggregate_context(ctx, sizeof(py_object)))
    try:
        obj = instance.value
    except ValueError:
        klass = cast(sqlite3_user_data(ctx), py_object).value

        try:
            obj = klass()
        except Exception:
            if _enable_callback_tracebacks:
                print_exc()
            sqlite3_result_error(ctx, b"user-defined aggregate's '__init__' method raised error", -1)
            return

        o = PyObject.from_address(id(obj))
        o.ob_refcnt += 1

        instance.value = obj

    method = getattr(obj, 'step')
    args = tuple(sqlite3_value(argv[i]) for i in range(argc))

    try:
        method(*args)
    except Exception:
        if _enable_callback_tracebacks:
            print_exc()
        sqlite3_result_error(ctx, b"user-defined aggregate's 'step' method raised error", -1)


@PYFUNCTYPE(None, c_void_p)
@wraps_exception
def _aggregate_final(ctx):
    addr = sqlite3_aggregate_context(ctx, sizeof(py_object))
    instance = py_object.from_address(addr)
    try:
        obj = instance.value
    except ValueError:
        return

    o = PyObject.from_address(id(obj))
    o.ob_refcnt -= 1
    c_void_p.from_address(addr).value = None

    restore = sys.exc_info()[0] is not None

    try:
        ret = obj.finalize()
    except Exception:
        if _enable_callback_tracebacks:
            print_exc()
        sqlite3_result_error(ctx, b"user-defined aggregate's 'finalize' method raised error", -1)
    else:
        sqlite3_result(ctx, ret)
        if restore:
            throw()
            raise
