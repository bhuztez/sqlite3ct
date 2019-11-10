# Copyright (C) 2004-2010 Gerhard Häring <gh@ghaering.de>
#
# This file is part of pysqlite.
#
# This software is provided 'as-is', without any express or implied
# warranty.  In no event will the authors be held liable for any damages
# arising from the use of this software.
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
#
# 1. The origin of this software must not be misrepresented; you must not
#    claim that you wrote the original software. If you use this software
#    in a product, an acknowledgment in the product documentation would be
#    appreciated but is not required.
# 2. Altered source versions must be plainly marked as such, and must not be
#    misrepresented as being the original software.
# 3. This notice may not be removed or altered from any source distribution.

import string
from itertools import takewhile
from threading import get_ident
from os import fsencode
from weakref import WeakSet
from collections.abc import Sequence
from ._sqlite3 import (
    sqlite3_threadsafe,
    sqlite3_errstr,
    Database,
    SQLITE_OK,
    SQLITE_ROW,
    SQLITE_DONE,
    SQLITE_INTEGER,
    SQLITE_FLOAT,
    SQLITE_TEXT,
    SQLITE_BLOB,
    SQLITE_NULL,
    SQLITE_OPEN_READWRITE,
    SQLITE_OPEN_CREATE,
    SQLITE_OPEN_URI,
    SQLITE_DETERMINISTIC)

threadsafety = sqlite3_threadsafe()

from .utils import (
    _set_error,
    _check_remaining_sql,
    _adapt)

from sqlite3 import (
    Warning,
    Error,
    InterfaceError,
    DatabaseError,
    DataError,
    OperationalError,
    IntegrityError,
    InternalError,
    ProgrammingError,
    NotSupportedError,
    PARSE_DECLTYPES,
    PARSE_COLNAMES,
    adapters,
    converters,
    PrepareProtocol)

from .callbacks import (
    enable_callback_tracebacks,
    _collation_callback,
    _authorizer_callback,
    _progress_handler,
    _trace_callback,
    _function_callback,
    _aggregate_step,
    _aggregate_final)


class Row(Sequence):
    __class__ = dict

    def __init__(self, cursor, data):
        t = type(cursor)
        if t != Cursor and not issubclass(t, Cursor):
            raise TypeError("cursor must be a cursor, not {}".format(type(cursor).__name__))

        self.cursor = cursor
        self.data = data
        self.description = tuple(c[0] for c in cursor.description)

    def __getitem__(self, name):
        if isinstance(name, slice):
            return self.data[name]
        elif isinstance(name, int):
            return self.data[name]
        elif isinstance(name, str):
            try:
                index = self.description.index(name.lower())
            except ValueError:
                raise IndexError("No item with that key")
            return self.data[index]
        else:
            raise IndexError("Index must be int or string")

    def __len__(self):
        return len(self.data)

    def keys(self):
        return list(self.description)

    def iter(self):
        return iter(self.data)

    def __hash__(self):
        return hash(self.description) ^ hash(self.data)

    def __eq__(self, other):
        return (self.description == other.description) and (self.data == other.data)



def _column_name(stmt, i):
    name = stmt.column_name(i)
    name, *_ = name.split(b'[', 1)
    name = name.rstrip().decode().lower()
    return (name, None, None, None, None, None, None)


collation_name_letters = string.ascii_letters + string.digits + '_'


class Cursor:
    _initialized = False

    def __init__(self, connection):
        if not isinstance(connection, Connection):
            raise TypeError("argument 1 must be Connection, not {}".format(type(connection).__name__))

        connection._cursors.add(self)
        self.connection = connection
        self.arraysize = 1
        self.row_factory = self.connection.row_factory
        self._stmt = None
        self._row_cast_map = ()
        self._reset = False
        self._locked = False
        self._closed = False
        self._initialized = True

    def _check(self):
        if not self._initialized:
            raise ProgrammingError("Base Cursor.__init__ not called.")

        if self._locked:
            raise ProgrammingError("Recursive use of cursors not allowed")

        if self._closed:
            raise ProgrammingError("Cannot operate on a closed cursor.")

        self.connection._check()

    def _set_error(self):
        self.connection._set_error()

    def _bind(self, stmt, parameters):
        num_params_needed = stmt.bind_parameter_count()
        if not hasattr(type(parameters), '__len__'):
            raise ValueError("parameters are of unsupported type")

        if isinstance(parameters, dict):
            for i in range(num_params_needed):
                name = stmt.bind_parameter_name(i+1)
                if not name:
                    raise ProgrammingError("Binding {} has no name, but you supplied a dictionary (which has only names).".format(i))

                name = name.decode()[1:]
                try:
                    param = parameters[name]
                except LookupError:
                    raise ProgrammingError("You did not supply a value for binding {}.".format(i))

                param = _adapt(param, PrepareProtocol, param)
                rc = stmt.bind(i+1, param)
                if rc != SQLITE_OK:
                    raise InterfaceError("Error binding parameter :{} - probably unsupported type.".format(name))

        else:
            num_params = len(parameters)

            if num_params != num_params_needed:
                raise ProgrammingError("Incorrect number of bindings supplied. The current statement uses {}, and there are {} supplied.".format(num_params_needed, num_params))

            for i in range(num_params_needed):
                param = parameters[i]
                param = _adapt(param, PrepareProtocol, param)
                rc = stmt.bind(i+1, param)
                if rc != SQLITE_OK:
                    raise InterfaceError("Error binding parameter {} - probably unsupported type.".format(i))

    def _get_converter(self, stmt, index):
        if self.connection.detect_types & PARSE_COLNAMES:
            name = stmt.column_name(index)
            _, *name = name.split(b'[', 1)
            if name:
                name, *tail = name[0].split(b']', 1)
                if tail:
                    name = str.upper(name.decode())
                    converter = converters.get(name, None)
                    if converter is not None:
                        return converter

        if self.connection.detect_types & PARSE_DECLTYPES:
            decltype = stmt.column_decltype(index)
            name = str.upper(bytes(takewhile(lambda c: c not in b'( ', decltype)).decode())
            return converters.get(name, None)


    def _execute(self, sql):
        if self._stmt is not None:
            self._stmt.finalize()
        self._stmt = None
        if not isinstance(sql, str):
            raise TypeError("operation parameter must be str")

        self._reset = False

        stmt, remain = self.connection._prepare(sql.encode())
        if stmt is None:
            return
        if _check_remaining_sql(remain):
            stmt.finalize()
            raise Warning("You can only execute one statement at a time.")

        self.description = tuple(_column_name(stmt, i) for i in range(stmt.column_count())) if not stmt.is_dml else None

        self._row_cast_map = tuple(self._get_converter(stmt, i) for i in range(stmt.column_count()))

        if self.connection._begin_statement is not None and stmt.is_dml:
            if not self.connection.in_transaction:
                self.connection.begin()
        return stmt

    def execute(self, sql, parameters=()):
        self._check()
        self._locked = True
        try:
            self._stmt = self._execute(sql)
            if self._stmt is None:
                return

            stmt = self._stmt

            self._bind(self._stmt, parameters)

            rc = self._stmt.step()
            if rc != SQLITE_ROW:
                self._stmt.finalize()
                self._stmt = None

            if rc not in (SQLITE_ROW, SQLITE_DONE):
                self._set_error()

            self.rowcount = self.connection._db.changes() if stmt.is_dml else -1
            self.lastrowid = self.connection._db.last_insert_rowid()
            return self
        finally:
            self._locked = False

    def executemany(self, sql, parameters):
        self._check()
        self._locked = True
        try:
            self._stmt = self._execute(sql)
            if self._stmt is None:
                return

            rowcount = 0

            if hasattr(parameters, '__next__'):
                def wrapper():
                    while True:
                        try:
                            yield next(parameters)
                        except StopIteration:
                            break

                params = wrapper()
            else:
                params = parameters

            for p in params:
                self._bind(self._stmt, p)

                rc = self._stmt.step()
                if rc == SQLITE_ROW:
                    raise ProgrammingError("executemany() can only execute DML statements.")
                if rc != SQLITE_DONE:
                    self._set_error()

                rowcount += self.connection._db.changes()
                self._stmt.reset()

            self.rowcount = rowcount
            return self
        finally:
            self._locked = False

    def executescript(self, sql_script):
        self._check()
        self._reset = False
        if self._stmt is not None:
            self._stmt.finalize()
        self._stmt = None

        if not isinstance(sql_script, str):
            raise ValueError("script argument must be unicode.")

        script = sql_script.encode()
        self.connection.commit()

        while script:
            self._stmt, script = self.connection._prepare(script)
            if self._stmt is not None:
                while True:
                    rc = self._stmt.step()
                    if rc == SQLITE_DONE:
                        break
                    if rc != SQLITE_ROW:
                        self._set_error()
                self._stmt.finalize()
                self._stmt = None
        return self

    def _fetch(self, index):
        if self.connection.detect_types and index < len(self._row_cast_map):
            converter = self._row_cast_map[index]
            if converter is not None:
                return converter(self._stmt.column_blob(index))

        coltype = self._stmt.column_type(index)
        if coltype == SQLITE_NULL:
            return None
        elif coltype == SQLITE_INTEGER:
            return self._stmt.column_int(index)
        elif coltype == SQLITE_FLOAT:
            return self._stmt.column_double(index)
        elif coltype == SQLITE_TEXT:
            text = self._stmt.column_text(index)
            text_factory = self.connection.text_factory
            if text_factory is str:
                try:
                    return text.decode()
                except UnicodeDecodeError:
                    raise OperationalError("Could not decode to UTF-8 column {!r} with text {}".format(self.description[index][0], str(text)[1:]))
            else:
                return text_factory(text)
        elif coltype == SQLITE_BLOB:
            return self._stmt.column_blob(index)
        else:
            assert False

    def fetchone(self):
        self._check()
        if self._reset:
            raise InterfaceError("Cursor needed to be reset because of commit/rollback and can no longer be fetched from.")

        if self._stmt is None:
            return None

        numcols = self._stmt.data_count()
        row = tuple(self._fetch(i) for i in range(numcols))

        if self.row_factory is not None:
            row = self.row_factory(self, row)

        rc = self._stmt.step()
        if rc != SQLITE_ROW:
            self._stmt.finalize()
            self._stmt = None
        if rc not in (SQLITE_ROW, SQLITE_DONE):
            self._set_error()
        return row

    def fetchmany(self, size=None):
        if size is None:
            size = self.arraysize
        return list(row for _, row in zip(range(size), self))

    def fetchall(self):
        return list(self)

    def __iter__(self):
        while True:
            row = self.fetchone()
            if row is None:
                break
            yield row

    def close(self):
        if self._initialized and self._closed:
            return
        self._check()
        self.connection._check_thread()
        if self._stmt is not None:
            self._stmt.finalize()
        self._stmt = None
        self._closed = True

    def __del__(self):
        if not self._initialized:
            return
        self.close()

    def setinputsizes(self, sizes):
        pass

    def setoutputsize(self, size, column=None):
        pass

class Connection:
    Warning = Warning
    Error = Error
    InterfaceError = InterfaceError
    DatabaseError = DatabaseError
    DataError = DataError
    OperationalError = OperationalError
    IntegrityError = IntegrityError
    InternalError = InternalError
    ProgrammingError = ProgrammingError
    NotSupportedError = NotSupportedError

    _initialized = False

    def __init__(self,
                 database,
                 timeout=5.0,
                 detect_types=False,
                 isolation_level="",
                 check_same_thread=True,
                 cached_statements=100,
                 uri=False):
        flags = SQLITE_OPEN_READWRITE | SQLITE_OPEN_CREATE
        if uri:
            flags |= SQLITE_OPEN_URI
            path = database.encode()
        else:
            path = fsencode(database)

        self._db = Database()
        self._db.open(path, flags)
        self._set_error()

        self._cursors = WeakSet()
        self._thread_ident = get_ident() if check_same_thread else None
        self._isolation_level = None
        self._collations = {}
        self._function_pinboard = {}

        self.row_factory = None
        self.text_factory = str
        self.detect_types = detect_types

        self._initialized = True
        self.isolation_level = isolation_level


    def _set_error(self):
        _set_error(self._db.errcode(), self._db.errmsg().decode())

    def _check_thread(self):
        if self._thread_ident is not None:
            thread_ident = get_ident()
            if thread_ident != self._thread_ident:
                raise ProgrammingError(
                    "SQLite objects created in a thread can only be used in that same thread. The object was created in thread id {} and this is thread id {}.".format(self._thread_ident, thread_ident))

    def _check(self):
        if not self._initialized:
            raise ProgrammingError("Base Connection.__init__ not called")

        self._check_thread()
        if self._db is None:
            raise ProgrammingError("Cannot operate on a closed database")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_type is None and exc_value is None and exc_tb is None:
            self.commit()
        else:
            self.rollback()

    def __call__(self, sql=''):
        self._check()
        if not isinstance(sql, str):
            raise TypeError("operation parameter must be str")
        self._prepare(sql.encode())

    def begin(self):
        stmt, _ = self._prepare(self._begin_statement.encode())
        stmt.step()
        stmt.finalize()

    def commit(self):
        self._check()
        if self.in_transaction:
            stmt, _ = self._prepare(b"COMMIT")
            stmt.step()
            stmt.finalize()

    def rollback(self):
        self._check()
        if self.in_transaction:
            for c in self._cursors:
                c._reset = True
            stmt, _ = self._prepare(b"ROLLBACK")
            stmt.step()
            stmt.finalize()

    def close(self):
        if self._db is None:
            return
        self._check()
        for c in self._cursors:
            c.close()
        _set_error(self._db.close())
        self._db = None

    def __del__(self):
        if not self._initialized:
            return
        if self._db is None:
            return
        self._db.close_v2()

    def cursor(self, factory=Cursor):
        self._check()
        cur = factory(self)
        t = type(cur)
        if t != Cursor and not issubclass(t, Cursor):
            raise TypeError("factory must return a cursor, not {}".format(type(cur).__name__))
        return cur

    def execute(self, sql, parameters=()):
        return self.cursor().execute(sql, parameters)

    def executemany(self, sql, parameters):
        return self.cursor().executemany(sql, parameters)

    def executescript(self, sql_script):
        return self.cursor().executescript(sql_script)

    def create_function(self, name, num_params, func, *, deterministic=False):
        self._check()
        self._function_pinboard[func] = None
        rc = self._db.create_function(name.encode(), num_params, SQLITE_DETERMINISTIC if deterministic else 0, id(func), _function_callback, None, None)
        if rc != SQLITE_OK:
            raise OperationalError("Error creating function")

    def create_aggregate(self, name, num_params, aggregate_class):
        self._check()
        self._function_pinboard[aggregate_class] = None
        rc = self._db.create_function(name.encode(), num_params, 0, id(aggregate_class), None, _aggregate_step, _aggregate_final)

        if rc != SQLITE_OK:
            raise OperationalError("Error creating aggregate")

    def create_collation(self, name, callback):
        self._check()
        if callback is not None and not callable(callback):
            raise TypeError("parameter must be callable")

        if not isinstance(name, str):
            raise TypeError("create_collation(name, callback)() argument 1 must be str, not {}".format(type(name).__name__))

        if not all(c in collation_name_letters for c in name):
            raise ProgrammingError("invalid character in collation name")

        upper = str.upper(name)
        if callback is None:
            self._db.create_collation(upper.encode(), None, None)
            self._set_error()
        else:
            self._db.create_collation(upper.encode(), _collation_callback, id(callback))
            self._set_error()
            self._collations[upper] = callback

    def set_authorizer(self, authorizer_callback):
        self._check()
        if authorizer_callback is None:
            self._db.set_authorizer(None, None)
            self._set_error()
        else:
            self._function_pinboard[authorizer_callback] = None
            self._db.set_authorizer(_authorizer_callback, id(authorizer_callback))
            self._set_error()

    def set_progress_handler(self, progress_handler, n):
        self._check()
        if progress_handler is None:
            self._db.progress_handler(0, None, None)
        else:
            self._function_pinboard[progress_handler] = None
            self._db.progress_handler(n, _progress_handler, id(progress_handler))

    def set_trace_callback(self, trace_callback):
        self._check()
        if trace_callback is None:
            self._db.trace(None, None)
        else:
            self._function_pinboard[trace_callback] = None
            self._db.trace(_trace_callback, id(trace_callback))


    @property
    def in_transaction(self):
        return not self._db.get_autocommit()

    @property
    def isolation_level(self):
        return self._isolation_level

    @isolation_level.setter
    def isolation_level(self, isolation_level):
        if isolation_level is None:
            self.commit()
            self._begin_statement = None
        else:
            candidate = "BEGIN " + str.upper(isolation_level)
            if candidate not in ("BEGIN ", "BEGIN DEFERRED", "BEGIN IMMEDIATE", "BEGIN EXCLUSIVE"):
                raise ValueError("invalid value for isolation_level")
            self._begin_statement = candidate

        self._isolation_level = isolation_level

    @property
    def total_changes(self):
        return self._db.total_changes()

    def _prepare(self, sql):
        if b'\0' in sql:
            raise ValueError("the query contains a null character")

        sql = sql.lstrip()
        is_dml = (
            sql[:6].lower() in (b'insert', b'update', b'delete') or
            sql[:7].lower() == b'replace')

        _, stmt, remain = self._db.prepare(sql)
        self._set_error()
        if stmt is not None:
            stmt.is_dml = is_dml
        return stmt, remain

    def iterdump(self):
        from sqlite3.dump import _iterdump
        return _iterdump(self)

    def backup(self, target, *, pages=0, progress=None, name="main", sleep=0.250):
        if not isinstance(target, Connection):
            raise TypeError("backup() argument 1 must be Connection, not {}".format(type(target).__name__))

        if target is self:
            raise ValueError("target cannot be the same connection instance")

        self._check()
        target._check()

        if pages == 0:
            pages = -1

        if progress is not None and not callable(progress):
            raise TypeError("progress argument must be a callable")

        backup = target._db.backup(b"main", self._db, name.encode())
        rc = target._db.errcode()
        _set_error(rc)
        sleep_ms = int(sleep * 1000.0)

        while rc != SQLITE_DONE:
            rc = backup.step(pages, sleep_ms)
            if progress is not None:
                progress(rc, backup.remaining(), backup.pagecount())

def connect(
        database,
        timeout=5.0,
        detect_types=False,
        isolation_level="",
        check_same_thread=True,
        factory=Connection,
        cached_statements=100,
        uri=False):
    return factory(
        database,
        timeout,
        detect_types,
        isolation_level,
        check_same_thread,
        cached_statements,
        uri)
