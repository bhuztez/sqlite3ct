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

from ._sqlite3 import (
    sqlite3_errstr,
    SQLITE_OK,
    SQLITE_ERROR,
    SQLITE_INTERNAL,
    SQLITE_PERM,
    SQLITE_ABORT,
    SQLITE_BUSY,
    SQLITE_LOCKED,
    SQLITE_NOMEM,
    SQLITE_READONLY,
    SQLITE_INTERRUPT,
    SQLITE_IOERR,
    SQLITE_CORRUPT,
    SQLITE_NOTFOUND,
    SQLITE_FULL,
    SQLITE_CANTOPEN,
    SQLITE_PROTOCOL,
    SQLITE_EMPTY,
    SQLITE_SCHEMA,
    SQLITE_TOOBIG,
    SQLITE_CONSTRAINT,
    SQLITE_MISMATCH,
    SQLITE_MISUSE,
)

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

from .exc import throw

def _set_error(rc, errmsg=None):
    throw()

    if rc == SQLITE_OK:
        return
    if errmsg is None:
        errmsg = sqlite3_errstr(rc).decode()

    if rc in (
            SQLITE_INTERNAL,
            SQLITE_NOTFOUND):
        raise InteralError(errmsg)
    elif rc == SQLITE_NOMEM:
        raise MemoryError()
    elif rc in (
            SQLITE_ERROR,
            SQLITE_PERM,
            SQLITE_ABORT,
            SQLITE_BUSY,
            SQLITE_LOCKED,
            SQLITE_READONLY,
            SQLITE_INTERRUPT,
            SQLITE_IOERR,
            SQLITE_FULL,
            SQLITE_CANTOPEN,
            SQLITE_PROTOCOL,
            SQLITE_EMPTY,
            SQLITE_SCHEMA,
    ):
        raise OperationalError(errmsg)
    elif rc == SQLITE_CORRUPT:
        raise DatabaseError(errmsg)
    elif rc == SQLITE_TOOBIG:
        raise DataError(errmsg)
    elif rc in (SQLITE_CONSTRAINT, SQLITE_MISMATCH):
        raise IntegrityError(errmsg)
    elif rc == SQLITE_MISUSE:
        raise ProgrammingError(errmsg)
    else:
        raise DatabaseError(errmsg)


NORMAL = 0
LINECOMMENT_1 = 1
IN_LINECOMMENT = 2
COMMENTSTART_1 = 3
IN_COMMENT = 4
COMMENTEND_1 = 5

def _check_remaining_sql(s):
    state = NORMAL

    for c in s:
        if c in b'-': # line comment
            if state == NORMAL:
                state = LINECOMMENT_1
            elif state == LINECOMMENT_1:
                state = IN_LINECOMMENT
        elif c in b' \t':
            pass
        elif c in b'\r\n':
            if state == IN_LINECOMMENT:
                state = NORMAL
        elif c in b'/':
            if state == NORMAL:
                state = COMMENTSTART_1
            elif state == COMMENTEND_1:
                state = NORMAL
            elif state == COMMENTSTART_1:
                return True
        elif c in b'*':
            if state in (NORMAL, LINECOMMENT_1):
                return True
            elif state == COMMENTSTART_1:
                state = IN_COMMENT
            elif state == IN_COMMENT:
                state = COMMENTEND_1
        else:
            if state == COMMENTEND_1:
                state = IN_COMMENT
            elif state not in (IN_LINECOMMENT, IN_COMMENT):
                return True

    return False


_null = object()

def _adapt(obj, proto, alt=_null):
    key = (type(obj), proto)
    adapter = adapters.get(key, None)
    if adapter is not None:
        return adapter(obj)
    adapter = getattr(adapter, "__adapt__", None)
    if adapter is not None:
        try:
            return adapter(obj)
        except TypeError:
            pass

    adapter = getattr(obj, '__conform__', None)
    if adapter is not None:
        try:
            return adapter(proto)
        except TypeError:
            pass

    if alt is not _null:
        return alt
    raise ProgrammingError("can't adapt")
