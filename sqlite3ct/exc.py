import sys

from ctypes import (
    pythonapi, PYFUNCTYPE, Structure, POINTER, byref,
    c_ssize_t, c_char_p, c_uint, c_int, c_void_p, py_object,
    string_at, cast, sizeof)

class PyObject(Structure):
    _fields_ = [
        ("ob_refcnt", c_ssize_t),
        ("objtype", py_object)
    ]

    if hasattr(sys, "getobjects"):
        _fields_ = [("ob_next", c_void_p), ("ob_prev", c_void_p)] + _fields_

PyErr_GetExcInfo = pythonapi.PyErr_GetExcInfo
PyErr_GetExcInfo.argtypes = [POINTER(py_object), POINTER(py_object), POINTER(py_object)]
PyErr_GetExcInfo.restype = None

PyErr_SetExcInfo = pythonapi.PyErr_SetExcInfo
PyErr_SetExcInfo.argtypes = [py_object, py_object, py_object]
PyErr_SetExcInfo.restype = None

PyErr_Fetch = pythonapi.PyErr_Fetch
PyErr_Fetch.argtypes = [POINTER(py_object), POINTER(py_object), POINTER(py_object)]
PyErr_Fetch.restype = None

PyErr_Clear = pythonapi.PyErr_Clear
PyErr_Clear.argtypes = []
PyErr_Clear.restype = None

PyErr_Restore = pythonapi.PyErr_Restore
PyErr_Restore.argtypes = [py_object, py_object, py_object]
PyErr_Restore.restype = None

def throw():
    exc_type = py_object()
    exc_value = py_object()
    exc_tb = py_object()
    PyErr_GetExcInfo(byref(exc_type), byref(exc_value), byref(exc_tb))

    if exc_type.value is None:
        return

    PyErr_SetExcInfo(None, None, None)
    raise exc_value.value
