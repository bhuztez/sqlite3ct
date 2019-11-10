from functools import wraps
from inspect import signature, Signature
from ctypes import (
    PyDLL, pythonapi, CFUNCTYPE, POINTER, Structure, cast, byref,
    c_ubyte, c_int, c_uint, c_double,
    c_char_p, c_void_p, string_at)

import sys
libsqlite = None

if sys.platform == 'win32':
    libsqlite = PyDLL("C:/ProgramData/chocolatey/lib/SQLite/tools/sqlite3.dll")
else:
    import _sqlite3
    libsqlite = PyDLL(_sqlite3.__file__)

def annotate(func):
    sig = signature(func)
    cfunc = getattr(libsqlite, func.__name__)
    argtypes = [p.annotation for p in sig.parameters.values()]
    cfunc.argtypes = argtypes
    if sig.return_annotation is Signature.empty:
        cfunc.restype = None
    else:
        cfunc.restype = sig.return_annotation
    return cfunc

# The author disclaims copyright to this source code.  In place of
# a legal notice, here is a blessing:
#
#    May you do good and not evil.
#    May you find forgiveness for yourself and forgive others.
#    May you share freely, never taking more than you give.
#

# Run-Time Library Version Numbers

@annotate
def sqlite3_libversion() -> c_char_p:
    pass

@annotate
def sqlite3_sourceid() -> c_char_p:
    pass

@annotate
def sqlite3_libversion_number() -> c_int:
    pass

# Database Connection Handle
sqlite3_p = c_void_p

# Run-Time Library Compilation Options Diagnostics
@annotate
def sqlite3_compileoption_used(zOptName: c_char_p) -> c_int:
    pass

@annotate
def sqlite3_compileoption_get(n: c_int) -> c_char_p:
    pass

# Test To See If The Library Is Threadsafe
@annotate
def sqlite3_threadsafe() -> c_int:
    pass

# 64-Bit Integer Types
from ctypes import c_int64 as sqlite_int64, c_uint64 as sqlite_uint64
sqlite3_int64 = sqlite_int64
sqlite3_uint64 = sqlite_uint64

# Closing A Database Connection
@annotate
def sqlite3_close(db: sqlite3_p) -> c_int:
    pass

@annotate
def sqlite3_close_v2(db: sqlite3_p) -> c_int:
    pass

# Result Codes
SQLITE_OK         =  0   # Successful result
# beginning-of-error-codes
SQLITE_ERROR      =  1   # Generic error
SQLITE_INTERNAL   =  2   # Internal logic error in SQLite
SQLITE_PERM       =  3   # Access permission denied
SQLITE_ABORT      =  4   # Callback routine requested an abort
SQLITE_BUSY       =  5   # The database file is locked
SQLITE_LOCKED     =  6   # A table in the database is locked
SQLITE_NOMEM      =  7   # A malloc() failed
SQLITE_READONLY   =  8   # Attempt to write a readonly database
SQLITE_INTERRUPT  =  9   # Operation terminated by sqlite3_interrupt()*/
SQLITE_IOERR      = 10   # Some kind of disk I/O error occurred
SQLITE_CORRUPT    = 11   # The database disk image is malformed
SQLITE_NOTFOUND   = 12   # Unknown opcode in sqlite3_file_control()
SQLITE_FULL       = 13   # Insertion failed because database is full
SQLITE_CANTOPEN   = 14   # Unable to open the database file
SQLITE_PROTOCOL   = 15   # Database lock protocol error
SQLITE_EMPTY      = 16   # Internal use only
SQLITE_SCHEMA     = 17   # The database schema changed
SQLITE_TOOBIG     = 18   # String or BLOB exceeds size limit
SQLITE_CONSTRAINT = 19   # Abort due to constraint violation
SQLITE_MISMATCH   = 20   # Data type mismatch
SQLITE_MISUSE     = 21   # Library used incorrectly
SQLITE_NOLFS      = 22   # Uses OS features not supported on host
SQLITE_AUTH       = 23   # Authorization denied
SQLITE_FORMAT     = 24   # Not used
SQLITE_RANGE      = 25   # 2nd parameter to sqlite3_bind out of range
SQLITE_NOTADB     = 26   # File opened that is not a database file
SQLITE_NOTICE     = 27   # Notifications from sqlite3_log()
SQLITE_WARNING    = 28   # Warnings from sqlite3_log()
SQLITE_ROW        = 100  # sqlite3_step() has another row ready
SQLITE_DONE       = 101  # sqlite3_step() has finished executing
# end-of-error-codes

# Extended Result Codes

SQLITE_ERROR_MISSING_COLLSEQ   = (SQLITE_ERROR | (1<<8))
SQLITE_ERROR_RETRY             = (SQLITE_ERROR | (2<<8))
SQLITE_ERROR_SNAPSHOT          = (SQLITE_ERROR | (3<<8))
SQLITE_IOERR_READ              = (SQLITE_IOERR | (1<<8))
SQLITE_IOERR_SHORT_READ        = (SQLITE_IOERR | (2<<8))
SQLITE_IOERR_WRITE             = (SQLITE_IOERR | (3<<8))
SQLITE_IOERR_FSYNC             = (SQLITE_IOERR | (4<<8))
SQLITE_IOERR_DIR_FSYNC         = (SQLITE_IOERR | (5<<8))
SQLITE_IOERR_TRUNCATE          = (SQLITE_IOERR | (6<<8))
SQLITE_IOERR_FSTAT             = (SQLITE_IOERR | (7<<8))
SQLITE_IOERR_UNLOCK            = (SQLITE_IOERR | (8<<8))
SQLITE_IOERR_RDLOCK            = (SQLITE_IOERR | (9<<8))
SQLITE_IOERR_DELETE            = (SQLITE_IOERR | (10<<8))
SQLITE_IOERR_BLOCKED           = (SQLITE_IOERR | (11<<8))
SQLITE_IOERR_NOMEM             = (SQLITE_IOERR | (12<<8))
SQLITE_IOERR_ACCESS            = (SQLITE_IOERR | (13<<8))
SQLITE_IOERR_CHECKRESERVEDLOCK = (SQLITE_IOERR | (14<<8))
SQLITE_IOERR_LOCK              = (SQLITE_IOERR | (15<<8))
SQLITE_IOERR_CLOSE             = (SQLITE_IOERR | (16<<8))
SQLITE_IOERR_DIR_CLOSE         = (SQLITE_IOERR | (17<<8))
SQLITE_IOERR_SHMOPEN           = (SQLITE_IOERR | (18<<8))
SQLITE_IOERR_SHMSIZE           = (SQLITE_IOERR | (19<<8))
SQLITE_IOERR_SHMLOCK           = (SQLITE_IOERR | (20<<8))
SQLITE_IOERR_SHMMAP            = (SQLITE_IOERR | (21<<8))
SQLITE_IOERR_SEEK              = (SQLITE_IOERR | (22<<8))
SQLITE_IOERR_DELETE_NOENT      = (SQLITE_IOERR | (23<<8))
SQLITE_IOERR_MMAP              = (SQLITE_IOERR | (24<<8))
SQLITE_IOERR_GETTEMPPATH       = (SQLITE_IOERR | (25<<8))
SQLITE_IOERR_CONVPATH          = (SQLITE_IOERR | (26<<8))
SQLITE_IOERR_VNODE             = (SQLITE_IOERR | (27<<8))
SQLITE_IOERR_AUTH              = (SQLITE_IOERR | (28<<8))
SQLITE_IOERR_BEGIN_ATOMIC      = (SQLITE_IOERR | (29<<8))
SQLITE_IOERR_COMMIT_ATOMIC     = (SQLITE_IOERR | (30<<8))
SQLITE_IOERR_ROLLBACK_ATOMIC   = (SQLITE_IOERR | (31<<8))
SQLITE_LOCKED_SHAREDCACHE      = (SQLITE_LOCKED |  (1<<8))
SQLITE_LOCKED_VTAB             = (SQLITE_LOCKED |  (2<<8))
SQLITE_BUSY_RECOVERY           = (SQLITE_BUSY   |  (1<<8))
SQLITE_BUSY_SNAPSHOT           = (SQLITE_BUSY   |  (2<<8))
SQLITE_CANTOPEN_NOTEMPDIR      = (SQLITE_CANTOPEN | (1<<8))
SQLITE_CANTOPEN_ISDIR          = (SQLITE_CANTOPEN | (2<<8))
SQLITE_CANTOPEN_FULLPATH       = (SQLITE_CANTOPEN | (3<<8))
SQLITE_CANTOPEN_CONVPATH       = (SQLITE_CANTOPEN | (4<<8))
SQLITE_CANTOPEN_DIRTYWAL       = (SQLITE_CANTOPEN | (5<<8)) # Not Used
SQLITE_CORRUPT_VTAB            = (SQLITE_CORRUPT | (1<<8))
SQLITE_CORRUPT_SEQUENCE        = (SQLITE_CORRUPT | (2<<8))
SQLITE_READONLY_RECOVERY       = (SQLITE_READONLY | (1<<8))
SQLITE_READONLY_CANTLOCK       = (SQLITE_READONLY | (2<<8))
SQLITE_READONLY_ROLLBACK       = (SQLITE_READONLY | (3<<8))
SQLITE_READONLY_DBMOVED        = (SQLITE_READONLY | (4<<8))
SQLITE_READONLY_CANTINIT       = (SQLITE_READONLY | (5<<8))
SQLITE_READONLY_DIRECTORY      = (SQLITE_READONLY | (6<<8))
SQLITE_ABORT_ROLLBACK          = (SQLITE_ABORT | (2<<8))
SQLITE_CONSTRAINT_CHECK        = (SQLITE_CONSTRAINT | (1<<8))
SQLITE_CONSTRAINT_COMMITHOOK   = (SQLITE_CONSTRAINT | (2<<8))
SQLITE_CONSTRAINT_FOREIGNKEY   = (SQLITE_CONSTRAINT | (3<<8))
SQLITE_CONSTRAINT_FUNCTION     = (SQLITE_CONSTRAINT | (4<<8))
SQLITE_CONSTRAINT_NOTNULL      = (SQLITE_CONSTRAINT | (5<<8))
SQLITE_CONSTRAINT_PRIMARYKEY   = (SQLITE_CONSTRAINT | (6<<8))
SQLITE_CONSTRAINT_TRIGGER      = (SQLITE_CONSTRAINT | (7<<8))
SQLITE_CONSTRAINT_UNIQUE       = (SQLITE_CONSTRAINT | (8<<8))
SQLITE_CONSTRAINT_VTAB         = (SQLITE_CONSTRAINT | (9<<8))
SQLITE_CONSTRAINT_ROWID        = (SQLITE_CONSTRAINT |(10<<8))
SQLITE_NOTICE_RECOVER_WAL      = (SQLITE_NOTICE | (1<<8))
SQLITE_NOTICE_RECOVER_ROLLBACK = (SQLITE_NOTICE | (2<<8))
SQLITE_WARNING_AUTOINDEX       = (SQLITE_WARNING | (1<<8))
SQLITE_AUTH_USER               = (SQLITE_AUTH | (1<<8))
SQLITE_OK_LOAD_PERMANENTLY     = (SQLITE_OK | (1<<8))

# Flags For File Open Operations
SQLITE_OPEN_READONLY        = 0x00000001  # Ok for sqlite3_open_v2()
SQLITE_OPEN_READWRITE       = 0x00000002  # Ok for sqlite3_open_v2()
SQLITE_OPEN_CREATE          = 0x00000004  # Ok for sqlite3_open_v2()
SQLITE_OPEN_DELETEONCLOSE   = 0x00000008  # VFS only
SQLITE_OPEN_EXCLUSIVE       = 0x00000010  # VFS only
SQLITE_OPEN_AUTOPROXY       = 0x00000020  # VFS only
SQLITE_OPEN_URI             = 0x00000040  # Ok for sqlite3_open_v2()
SQLITE_OPEN_MEMORY          = 0x00000080  # Ok for sqlite3_open_v2()
SQLITE_OPEN_MAIN_DB         = 0x00000100  # VFS only
SQLITE_OPEN_TEMP_DB         = 0x00000200  # VFS only
SQLITE_OPEN_TRANSIENT_DB    = 0x00000400  # VFS only
SQLITE_OPEN_MAIN_JOURNAL    = 0x00000800  # VFS only
SQLITE_OPEN_TEMP_JOURNAL    = 0x00001000  # VFS only
SQLITE_OPEN_SUBJOURNAL      = 0x00002000  # VFS only
SQLITE_OPEN_MASTER_JOURNAL  = 0x00004000  # VFS only
SQLITE_OPEN_NOMUTEX         = 0x00008000  # Ok for sqlite3_open_v2()
SQLITE_OPEN_FULLMUTEX       = 0x00010000  # Ok for sqlite3_open_v2()
SQLITE_OPEN_SHAREDCACHE     = 0x00020000  # Ok for sqlite3_open_v2()
SQLITE_OPEN_PRIVATECACHE    = 0x00040000  # Ok for sqlite3_open_v2()
SQLITE_OPEN_WAL             = 0x00080000  # VFS only

# Device Characteristics
SQLITE_IOCAP_ATOMIC                = 0x00000001
SQLITE_IOCAP_ATOMIC512             = 0x00000002
SQLITE_IOCAP_ATOMIC1K              = 0x00000004
SQLITE_IOCAP_ATOMIC2K              = 0x00000008
SQLITE_IOCAP_ATOMIC4K              = 0x00000010
SQLITE_IOCAP_ATOMIC8K              = 0x00000020
SQLITE_IOCAP_ATOMIC16K             = 0x00000040
SQLITE_IOCAP_ATOMIC32K             = 0x00000080
SQLITE_IOCAP_ATOMIC64K             = 0x00000100
SQLITE_IOCAP_SAFE_APPEND           = 0x00000200
SQLITE_IOCAP_SEQUENTIAL            = 0x00000400
SQLITE_IOCAP_UNDELETABLE_WHEN_OPEN = 0x00000800
SQLITE_IOCAP_POWERSAFE_OVERWRITE   = 0x00001000
SQLITE_IOCAP_IMMUTABLE             = 0x00002000
SQLITE_IOCAP_BATCH_ATOMIC          = 0x00004000

# File Locking Levels
SQLITE_LOCK_NONE         = 0
SQLITE_LOCK_SHARED       = 1
SQLITE_LOCK_RESERVED     = 2
SQLITE_LOCK_PENDING      = 3
SQLITE_LOCK_EXCLUSIVE    = 4

# Synchronization Type Flags
SQLITE_SYNC_NORMAL       = 0x00002
SQLITE_SYNC_FULL         = 0x00003
SQLITE_SYNC_DATAONLY     = 0x00010

# OS Interface Open File Handle
class sqlite3_file(Structure):
    pass

class sqlite3_io_methods(Structure):
    pass

sqlite3_file._fields_ = [
    ("pMethods", POINTER(sqlite3_io_methods)), # Methods for an open file
]

sqlite3_io_methods._fields_ = [
    ("iVersion", c_int),
    ("xClose", c_void_p),
    ("xRead", c_void_p),
    ("xWrite", c_void_p),
    ("xTruncate", c_void_p),
    ("xSync", c_void_p),
    ("xFileSize", c_void_p),
    ("xLock", c_void_p),
    ("xUnlock", c_void_p),
    ("xCheckReservedLock", c_void_p),
    ("xFileControl", c_void_p),
    ("xSectorSize", c_void_p),
    ("xDeviceCharacteristics", c_void_p),
    # Methods above are valid for version 1
    ("xShmMap", c_void_p),
    ("xShmLock", c_void_p),
    ("xShmBarrier", c_void_p),
    ("xShmUnmap", c_void_p),
    # Methods above are valid for version 2
    ("xFetch", c_void_p),
    ("xUnfetch", c_void_p),
    # Methods above are valid for version 3
    # Additional methods may be added in future releases
]

# Standard File Control Opcodes
SQLITE_FCNTL_LOCKSTATE             =  1
SQLITE_FCNTL_GET_LOCKPROXYFILE     =  2
SQLITE_FCNTL_SET_LOCKPROXYFILE     =  3
SQLITE_FCNTL_LAST_ERRNO            =  4
SQLITE_FCNTL_SIZE_HINT             =  5
SQLITE_FCNTL_CHUNK_SIZE            =  6
SQLITE_FCNTL_FILE_POINTER          =  7
SQLITE_FCNTL_SYNC_OMITTED          =  8
SQLITE_FCNTL_WIN32_AV_RETRY        =  9
SQLITE_FCNTL_PERSIST_WAL           = 10
SQLITE_FCNTL_OVERWRITE             = 11
SQLITE_FCNTL_VFSNAME               = 12
SQLITE_FCNTL_POWERSAFE_OVERWRITE   = 13
SQLITE_FCNTL_PRAGMA                = 14
SQLITE_FCNTL_BUSYHANDLER           = 15
SQLITE_FCNTL_TEMPFILENAME          = 16
SQLITE_FCNTL_MMAP_SIZE             = 18
SQLITE_FCNTL_TRACE                 = 19
SQLITE_FCNTL_HAS_MOVED             = 20
SQLITE_FCNTL_SYNC                  = 21
SQLITE_FCNTL_COMMIT_PHASETWO       = 22
SQLITE_FCNTL_WIN32_SET_HANDLE      = 23
SQLITE_FCNTL_WAL_BLOCK             = 24
SQLITE_FCNTL_ZIPVFS                = 25
SQLITE_FCNTL_RBU                   = 26
SQLITE_FCNTL_VFS_POINTER           = 27
SQLITE_FCNTL_JOURNAL_POINTER       = 28
SQLITE_FCNTL_WIN32_GET_HANDLE      = 29
SQLITE_FCNTL_PDB                   = 30
SQLITE_FCNTL_BEGIN_ATOMIC_WRITE    = 31
SQLITE_FCNTL_COMMIT_ATOMIC_WRITE   = 32
SQLITE_FCNTL_ROLLBACK_ATOMIC_WRITE = 33
SQLITE_FCNTL_LOCK_TIMEOUT          = 34
SQLITE_FCNTL_DATA_VERSION          = 35
SQLITE_FCNTL_SIZE_LIMIT            = 36

# deprecated names
SQLITE_GET_LOCKPROXYFILE     = SQLITE_FCNTL_GET_LOCKPROXYFILE
SQLITE_SET_LOCKPROXYFILE     = SQLITE_FCNTL_SET_LOCKPROXYFILE
SQLITE_LAST_ERRNO            = SQLITE_FCNTL_LAST_ERRNO

# Mutex Handle
sqlite3_mutex_p = c_void_p

# OS Interface Objecth
class sqlite3_vfs(Structure):
    pass

sqlite3_syscall_ptr = CFUNCTYPE(None);

sqlite3_vfs._fields_ = [
    ("iVersion", c_int),    # Structure version number (currently 3)
    ("szOsFile", c_int),    # Size of subclassed sqlite3_file
    ("mxPathname", c_int),  # Maximum file pathname length
    ("pNext", POINTER(sqlite3_vfs)), # Next registered VFS
    ("zName", c_char_p),    # Name of this virtual file system
    ("pAppData", c_void_p), # Pointer to application-specific data
    ("xOpen", c_void_p),
    ("xDelete", c_void_p),
    ("xAccess", c_void_p),
    ("xFullPathname", c_void_p),
    ("xDlOpen", c_void_p),
    ("xDlError", c_void_p),
    ("xDlSym", c_void_p),
    ("xDlClose", c_void_p),
    ("xRandomness", c_void_p),
    ("xSleep", c_void_p),
    ("xCurrentTime", c_void_p),
    ("xGetLastError", c_void_p),
    # The methods above are in version 1 of the sqlite_vfs object
    # definition.  Those that follow are added in version 2 or later
    ("xCurrentTimeInt64", c_void_p),
    # The methods above are in versions 1 and 2 of the sqlite_vfs object.
    # Those below are for version 3 and greater.
    ("xSetSystemCall", c_void_p),
    ("xGetSystemCall", c_void_p),
    ("xNextSystemCall", c_void_p),
    # The methods above are in versions 1 through 3 of the sqlite_vfs object.
    # New fields may be appended in future versions.  The iVersion
    # value will increment whenever this happens.
]

# Flags for the xAccess VFS method
SQLITE_ACCESS_EXISTS    = 0
SQLITE_ACCESS_READWRITE = 1   # Used by PRAGMA temp_store_directory
SQLITE_ACCESS_READ      = 2   # Unused

# Flags for the xShmLock VFS method
SQLITE_SHM_UNLOCK       = 1
SQLITE_SHM_LOCK         = 2
SQLITE_SHM_SHARED       = 4
SQLITE_SHM_EXCLUSIVE    = 8

# Maximum xShmLock index
SQLITE_SHM_NLOCK        = 8

# Configuring The SQLite Library
sqlite3_config = libsqlite.sqlite3_config

# Configure database connections
sqlite3_db_config = libsqlite.sqlite3_db_config

# Memory Allocation Routines
class sqlite3_mem_methods(Structure):
    _fields_ = [
        ("xMalloc", c_void_p),             # Memory allocation function
        ("xFree", c_void_p),               # Free a prior allocation
        ("xRealloc", c_void_p),            # Resize an allocation
        ("xSize", c_void_p),               # Return the size of an allocation
        ("xRoundup", c_void_p),            # Round up request size to allocation size
        ("xInit", c_void_p),               # Initialize the memory allocator
        ("xShutdown", c_void_p),           # Deinitialize the memory allocator
        ("pAppData", c_void_p),            # Argument to xInit() and xShutdown()
    ]

# Configuration Options

SQLITE_CONFIG_SINGLETHREAD        =  1  # nil
SQLITE_CONFIG_MULTITHREAD         =  2  # nil
SQLITE_CONFIG_SERIALIZED          =  3  # nil
SQLITE_CONFIG_MALLOC              =  4  # sqlite3_mem_methods*
SQLITE_CONFIG_GETMALLOC           =  5  # sqlite3_mem_methods*
SQLITE_CONFIG_SCRATCH             =  6  # No longer used
SQLITE_CONFIG_PAGECACHE           =  7  # void*, int sz, int N
SQLITE_CONFIG_HEAP                =  8  # void*, int nByte, int min
SQLITE_CONFIG_MEMSTATUS           =  9  # boolean
SQLITE_CONFIG_MUTEX               = 10  # sqlite3_mutex_methods*
SQLITE_CONFIG_GETMUTEX            = 11  # sqlite3_mutex_methods*
# previously SQLITE_CONFIG_CHUNKALLOC 12 which is now unused.
SQLITE_CONFIG_LOOKASIDE           = 13  # int int
SQLITE_CONFIG_PCACHE              = 14  # no-op
SQLITE_CONFIG_GETPCACHE           = 15  # no-op
SQLITE_CONFIG_LOG                 = 16  # xFunc, void*
SQLITE_CONFIG_URI                 = 17  # int
SQLITE_CONFIG_PCACHE2             = 18  # sqlite3_pcache_methods2*
SQLITE_CONFIG_GETPCACHE2          = 19  # sqlite3_pcache_methods2*
SQLITE_CONFIG_COVERING_INDEX_SCAN = 20  # int
SQLITE_CONFIG_SQLLOG              = 21  # xSqllog, void*
SQLITE_CONFIG_MMAP_SIZE           = 22  # sqlite3_int64, sqlite3_int64
SQLITE_CONFIG_WIN32_HEAPSIZE      = 23  # int nByte
SQLITE_CONFIG_PCACHE_HDRSZ        = 24  # int *psz
SQLITE_CONFIG_PMASZ               = 25  # unsigned int szPma
SQLITE_CONFIG_STMTJRNL_SPILL      = 26  # int nByte
SQLITE_CONFIG_SMALL_MALLOC        = 27  # boolean
SQLITE_CONFIG_SORTERREF_SIZE      = 28  # int nByte
SQLITE_CONFIG_MEMDB_MAXSIZE       = 29  # sqlite3_int64

# Database Connection Configuration Options
SQLITE_DBCONFIG_MAINDBNAME            = 1000 # const char*
SQLITE_DBCONFIG_LOOKASIDE             = 1001 # void* int int
SQLITE_DBCONFIG_ENABLE_FKEY           = 1002 # int int*
SQLITE_DBCONFIG_ENABLE_TRIGGER        = 1003 # int int*
SQLITE_DBCONFIG_ENABLE_FTS3_TOKENIZER = 1004 # int int*
SQLITE_DBCONFIG_ENABLE_LOAD_EXTENSION = 1005 # int int*
SQLITE_DBCONFIG_NO_CKPT_ON_CLOSE      = 1006 # int int*
SQLITE_DBCONFIG_ENABLE_QPSG           = 1007 # int int*
SQLITE_DBCONFIG_TRIGGER_EQP           = 1008 # int int*
SQLITE_DBCONFIG_RESET_DATABASE        = 1009 # int int*
SQLITE_DBCONFIG_DEFENSIVE             = 1010 # int int*
SQLITE_DBCONFIG_WRITABLE_SCHEMA       = 1011 # int int*
SQLITE_DBCONFIG_LEGACY_ALTER_TABLE    = 1012 # int int*
SQLITE_DBCONFIG_DQS_DML               = 1013 # int int*
SQLITE_DBCONFIG_DQS_DDL               = 1014 # int int*
SQLITE_DBCONFIG_ENABLE_VIEW           = 1015 # int int*
SQLITE_DBCONFIG_LEGACY_FILE_FORMAT    = 1016 # int int*
SQLITE_DBCONFIG_MAX                   = 1016 # Largest DBCONFIG

# Enable Or Disable Extended Result Codes
@annotate
def sqlite3_extended_result_codes(db: sqlite3_p, onoff: c_int) -> c_int:
    pass

# Last Insert Rowid
@annotate
def sqlite3_last_insert_rowid(db: sqlite3_p) -> sqlite3_int64:
    pass

# Set the Last Insert Rowid value
# @annotate
# def sqlite3_set_last_insert_rowid(db: sqlite3_p, rowid: sqlite3_int64):
#     pass

# Count The Number Of Rows Modified
@annotate
def sqlite3_changes(db: sqlite3_p) -> c_int:
    pass

# Total Number Of Rows Modified
@annotate
def sqlite3_total_changes(db: sqlite3_p) -> c_int:
    pass

# Interrupt A Long-Running Query
@annotate
def sqlite3_interrupt(db: sqlite3_p):
    pass

# Determine If An SQL Statement Is Complete
@annotate
def sqlite3_complete(sql: c_char_p) -> c_int:
    pass

# Register A Callback To Handle SQLITE_BUSY Errors
@annotate
def sqlite3_busy_handler(db: sqlite3_p, callback: c_void_p, pArg: c_void_p) -> c_int:
    pass

# Set A Busy Timeout
@annotate
def sqlite3_busy_timeout(db: sqlite3_p, ms: c_int) -> c_int:
    pass

# Formatted String Printing Functions
sqlite3_mprintf = libsqlite.sqlite3_mprintf
sqlite3_snprintf = libsqlite.sqlite3_snprintf

# Memory Allocation Subsystem
@annotate
def sqlite3_malloc(size: c_int) -> c_void_p:
    pass

@annotate
def sqlite3_malloc64(size: sqlite3_uint64) -> c_void_p:
    pass

@annotate
def sqlite3_realloc(ptr: c_void_p, size: c_int) -> c_void_p:
    pass

@annotate
def sqlite3_realloc64(ptr: c_void_p, size: sqlite3_uint64) -> c_void_p:
    pass

@annotate
def sqlite3_free(ptr: c_void_p):
    pass

@annotate
def sqlite3_msize(ptr: c_void_p) -> sqlite3_uint64:
    pass

# Memory Allocator Statistics
@annotate
def sqlite3_memory_used() -> sqlite3_int64:
    pass

@annotate
def sqlite3_memory_highwater(resetFlag: c_int) -> sqlite3_int64:
    pass

# Pseudo-Random Number Generator
@annotate
def sqlite3_randomness(N: c_int, P: c_void_p):
    pass

# Compile-Time Authorization Callbacks
@annotate
def sqlite3_set_authorizer(db: sqlite3_p, xAuth: c_void_p, pUserData: c_void_p) -> c_int:
    pass

# Authorizer Return Codes
SQLITE_DENY   = 1   # Abort the SQL statement with an error
SQLITE_IGNORE = 2   # Don't allow access, but don't generate an error

# Authorizer Action Codes
SQLITE_CREATE_INDEX        =  1   # Index Name      Table Name
SQLITE_CREATE_TABLE        =  2   # Table Name      NULL
SQLITE_CREATE_TEMP_INDEX   =  3   # Index Name      Table Name
SQLITE_CREATE_TEMP_TABLE   =  4   # Table Name      NULL
SQLITE_CREATE_TEMP_TRIGGER =  5   # Trigger Name    Table Name
SQLITE_CREATE_TEMP_VIEW    =  6   # View Name       NULL
SQLITE_CREATE_TRIGGER      =  7   # Trigger Name    Table Name
SQLITE_CREATE_VIEW         =  8   # View Name       NULL
SQLITE_DELETE              =  9   # Table Name      NULL
SQLITE_DROP_INDEX          = 10   # Index Name      Table Name
SQLITE_DROP_TABLE          = 11   # Table Name      NULL
SQLITE_DROP_TEMP_INDEX     = 12   # Index Name      Table Name
SQLITE_DROP_TEMP_TABLE     = 13   # Table Name      NULL
SQLITE_DROP_TEMP_TRIGGER   = 14   # Trigger Name    Table Name
SQLITE_DROP_TEMP_VIEW      = 15   # View Name       NULL
SQLITE_DROP_TRIGGER        = 16   # Trigger Name    Table Name
SQLITE_DROP_VIEW           = 17   # View Name       NULL
SQLITE_INSERT              = 18   # Table Name      NULL
SQLITE_PRAGMA              = 19   # Pragma Name     1st arg or NULL
SQLITE_READ                = 20   # Table Name      Column Name
SQLITE_SELECT              = 21   # NULL            NULL
SQLITE_TRANSACTION         = 22   # Operation       NULL
SQLITE_UPDATE              = 23   # Table Name      Column Name
SQLITE_ATTACH              = 24   # Filename        NULL
SQLITE_DETACH              = 25   # Database Name   NULL
SQLITE_ALTER_TABLE         = 26   # Database Name   Table Name
SQLITE_REINDEX             = 27   # Index Name      NULL
SQLITE_ANALYZE             = 28   # Table Name      NULL
SQLITE_CREATE_VTABLE       = 29   # Table Name      Module Name
SQLITE_DROP_VTABLE         = 30   # Table Name      Module Name
SQLITE_FUNCTION            = 31   # NULL            Function Name
SQLITE_SAVEPOINT           = 32   # Operation       Savepoint Name
SQLITE_COPY                =  0   # No longer used
SQLITE_RECURSIVE           = 33   # NULL            NULL

# SQL Trace Event Codes
SQLITE_TRACE_STMT      = 0x01
SQLITE_TRACE_PROFILE   = 0x02
SQLITE_TRACE_ROW       = 0x04
SQLITE_TRACE_CLOSE     = 0x08

# SQL Trace Hook
@annotate
def sqlite3_trace(db: sqlite3_p, xTrace: c_void_p, pCtx: c_void_p) -> c_void_p:
    pass

# @annotate
# def sqlite3_trace_v2(db: sqlite3_p, uMask: c_uint, xCallback: c_void_p, pCtx: c_void_p) -> c_int:
#     pass

# Query Progress Callbacks
@annotate
def sqlite3_progress_handler(db: sqlite3_p, n: c_int, callback: c_void_p, param: c_void_p):
    pass

# Opening A New Database Connection
@annotate
def sqlite3_open_v2(
        filename: c_char_p,       # Database filename (UTF-8)
        ppDb: POINTER(sqlite3_p), # OUT: SQLite db handle
        flags: c_int,             # Flags
        zVfs: c_char_p            # Name of VFS module to use
) -> c_int:
    pass

# Obtain Values For URI Parameters
@annotate
def sqlite3_uri_parameter(zFilename: c_char_p, zParam: c_char_p) -> c_char_p:
    pass

@annotate
def sqlite3_uri_boolean(zFile: c_char_p, zParam: c_char_p, bDefault: c_int) -> c_int:
    pass

@annotate
def sqlite3_uri_int64(zFile: c_char_p, zParam: c_char_p, default: sqlite3_int64) -> sqlite3_int64:
    pass

# Error Codes And Messages
@annotate
def sqlite3_errcode(db: sqlite3_p) -> c_int:
    pass

@annotate
def sqlite3_extended_errcode(db: sqlite3_p) -> c_int:
    pass

@annotate
def sqlite3_errmsg(db: sqlite3_p) -> c_char_p:
    pass

@annotate
def sqlite3_errstr(n: c_int) -> c_char_p:
    pass

# Prepared Statement Object
sqlite3_stmt_p = c_void_p

# Run-time Limits
@annotate
def sqlite3_limit(db: sqlite3_p, id: c_int, newVal: c_int) -> c_int:
    pass

# Run-Time Limit Categories
SQLITE_LIMIT_LENGTH                  =  0
SQLITE_LIMIT_SQL_LENGTH              =  1
SQLITE_LIMIT_COLUMN                  =  2
SQLITE_LIMIT_EXPR_DEPTH              =  3
SQLITE_LIMIT_COMPOUND_SELECT         =  4
SQLITE_LIMIT_VDBE_OP                 =  5
SQLITE_LIMIT_FUNCTION_ARG            =  6
SQLITE_LIMIT_ATTACHED                =  7
SQLITE_LIMIT_LIKE_PATTERN_LENGTH     =  8
SQLITE_LIMIT_VARIABLE_NUMBER         =  9
SQLITE_LIMIT_TRIGGER_DEPTH           = 10
SQLITE_LIMIT_WORKER_THREADS          = 11

# Prepare Flags
SQLITE_PREPARE_PERSISTENT             = 0x01
SQLITE_PREPARE_NORMALIZE              = 0x02
SQLITE_PREPARE_NO_VTAB                = 0x04

# Compiling An SQL Statement
@annotate
def sqlite3_prepare_v2(
        db: sqlite3_p,                    # Database handle
        zSql: c_void_p,                   # SQL statement, UTF-8 encoded
        nByte: c_int,                     # Maximum length of zSql in bytes.
        ppStmt: POINTER(sqlite3_stmt_p),  # OUT: Statement handle
        pzTail: POINTER(c_void_p)         # OUT: Pointer to unused portion of zSql
) -> c_int:
    pass

# @annotate
# def sqlite3_prepare_v3(
#         db: sqlite3_p,                    # Database handle
#         zSql: c_void_p,                   # SQL statement, UTF-8 encoded
#         nByte: c_int,                     # Maximum length of zSql in bytes.
#         prepFlags: c_uint,                # Zero or more SQLITE_PREPARE_ flags
#         ppStmt: POINTER(sqlite3_stmt_p),  # OUT: Statement handle
#         pzTail: POINTER(c_void_p)         # OUT: Pointer to unused portion of zSql
# ) -> c_int:
#     pass

# Retrieving Statement SQL
@annotate
def sqlite3_sql(pStmt: sqlite3_stmt_p) -> c_char_p:
    pass

# @annotate
# def sqlite3_expanded_sql(pStmt: sqlite3_stmt_p) -> c_char_p:
#     pass

# @annotate
# def sqlite3_normalized_sql(pStmt: sqlite3_stmt_p) -> c_char_p:
#     pass

# Determine If An SQL Statement Writes The Database
@annotate
def sqlite3_stmt_readonly(pStmt: sqlite3_stmt_p) -> c_int:
    pass

# Query The EXPLAIN Setting For A Prepared Statement
# @annotate
# def sqlite3_stmt_isexplain(pStmt: sqlite3_stmt_p) -> c_int:
#     pass

# Determine If A Prepared Statement Has Been Reset
@annotate
def sqlite3_stmt_busy(pStmt: sqlite3_stmt_p) -> c_int:
    pass

# Dynamically Typed Value Object
sqlite3_value_p = c_void_p

# SQL Function Context Object
sqlite3_context_p = c_void_p

# Constants Defining Special Destructor Behavior
sqlite3_destructor_type = CFUNCTYPE(None, c_void_p)
SQLITE_STATIC      = sqlite3_destructor_type(0)
SQLITE_TRANSIENT   = sqlite3_destructor_type(-1)

# Binding Values To Prepared Statements
@annotate
def sqlite3_bind_blob64(
        pStmt: sqlite3_stmt_p,
        index: c_int,
        value: c_void_p,
        nByte: sqlite3_uint64,
        destructor: sqlite3_destructor_type
) -> c_int:
    pass

@annotate
def sqlite3_bind_double(pStmt: sqlite3_stmt_p, index: c_int, value: c_double) -> c_int:
    pass

@annotate
def sqlite3_bind_int64(pStmt: sqlite3_stmt_p, index: c_int, value: sqlite3_int64) -> c_int:
    pass

@annotate
def sqlite3_bind_null(pStmt: sqlite3_stmt_p, index: c_int) -> c_int:
    pass

@annotate
def sqlite3_bind_text64(
        pStmt: sqlite3_stmt_p,
        index: c_int,
        value: c_char_p,
        nByte: sqlite3_uint64,
        destructor: sqlite3_destructor_type,
        encoding: c_ubyte) -> c_int:
    pass


@annotate
def sqlite3_bind_value(pStmt: sqlite3_stmt_p, index: c_int, value: sqlite3_value_p) -> c_int:
    pass

# @annotate
# def sqlite3_bind_pointer(pStmt: sqlite3_stmt_p, index: c_int, value: c_void_p, type: c_char_p, destructor: sqlite3_destructor_type) -> c_int:
#     pass

@annotate
def sqlite3_bind_zeroblob64(pStmt: sqlite3_stmt_p, index: c_int, n: sqlite3_uint64) -> c_int:
    pass

# Number Of SQL Parameters
@annotate
def sqlite3_bind_parameter_count(pStmt: sqlite3_stmt_p) -> c_int:
    pass

# Name Of A Host Parameter
@annotate
def sqlite3_bind_parameter_name(pStmt: sqlite3_stmt_p, index: c_int) -> c_char_p:
    pass


# Index Of A Parameter With A Given Name
@annotate
def sqlite3_bind_parameter_index(pStmt: sqlite3_stmt_p, zName: c_char_p) -> c_int:
    pass

# Reset All Bindings On A Prepared Statement
@annotate
def sqlite3_clear_bindings(pStmt: sqlite3_stmt_p) -> c_int:
    pass

# Number Of Columns In A Result Set
@annotate
def sqlite3_column_count(pStmt: sqlite3_stmt_p) -> c_int:
    pass

# Column Names In A Result Set
@annotate
def sqlite3_column_name(pStmt: sqlite3_stmt_p, n: c_int) -> c_char_p:
    pass

# Source Of Data In A Query Result
# @annotate
# def sqlite3_column_database_name(pStmt: sqlite3_stmt_p, n: c_int) -> c_char_p:
#     pass

# @annotate
# def sqlite3_column_table_name(pStmt: sqlite3_stmt_p, n: c_int) -> c_char_p:
#     pass

# @annotate
# def sqlite3_column_origin_name(pStmt: sqlite3_stmt_p, n: c_int) -> c_char_p:
#     pass

# Declared Datatype Of A Query Result
@annotate
def sqlite3_column_decltype(pStmt: sqlite3_stmt_p, n: c_int) -> c_char_p:
    pass

# Evaluate An SQL Statement
@annotate
def sqlite3_step(pStmt: sqlite3_stmt_p) -> c_int:
    pass


# Number of columns in a result set
@annotate
def sqlite3_data_count(pStmt: sqlite3_stmt_p) -> c_int:
    pass

# Fundamental Datatypes
SQLITE_INTEGER = 1
SQLITE_FLOAT   = 2
SQLITE_TEXT    = 3
SQLITE_BLOB    = 4
SQLITE_NULL    = 5

# Result Values From A Query
@annotate
def sqlite3_column_blob(pStmt: sqlite3_stmt_p, iCol: c_int) -> c_void_p:
    pass

@annotate
def sqlite3_column_double(pStmt: sqlite3_stmt_p, iCol: c_int) -> c_double:
    pass

# @annotate
# def sqlite3_column_int(pStmt: sqlite3_stmt_p, iCol: c_int) -> c_int:
#     pass

@annotate
def sqlite3_column_int64(pStmt: sqlite3_stmt_p, iCol: c_int) -> sqlite3_int64:
    pass

@annotate
def sqlite3_column_text(pStmt: sqlite3_stmt_p, iCol: c_int) -> c_void_p:
    pass

@annotate
def sqlite3_column_value(pStmt: sqlite3_stmt_p, iCol: c_int) -> sqlite3_value_p:
    pass

@annotate
def sqlite3_column_bytes(pStmt: sqlite3_stmt_p, iCol: c_int) -> c_int:
    pass

@annotate
def sqlite3_column_type(pStmt: sqlite3_stmt_p, iCol: c_int) -> c_int:
    pass

# Destroy A Prepared Statement Object
@annotate
def sqlite3_finalize(pStmt: sqlite3_stmt_p) -> c_int:
    pass

# Reset A Prepared Statement Object
@annotate
def sqlite3_reset(pStmt: sqlite3_stmt_p) -> c_int:
    pass

# Create Or Redefine SQL Functions
@annotate
def sqlite3_create_function_v2(
        db: c_void_p,
        zFunctionName: c_char_p,
        nArg: c_int,
        eTextRep: c_int,
        pApp: c_void_p,
        xFunc: c_void_p,
        xStep: c_void_p,
        xFinal: c_void_p,
        xDestroy: sqlite3_destructor_type) -> c_int:
    pass

# @annotate
# def sqlite3_create_window_function(
#         db: c_void_p,
#         zFunctionName: c_char_p,
#         nArg: c_int,
#         eTextRep: c_int,
#         pApp: c_void_p,
#         xFunc: c_void_p,
#         xStep: c_void_p,
#         xFinal: c_void_p,
#         xInverse: c_void_p,
#         xDestroy: sqlite3_destructor_type) -> c_int:
#     pass

# Text Encodings
SQLITE_UTF8          = 1    # IMP: R-37514-35566
SQLITE_UTF16LE       = 2    # IMP: R-03371-37637
SQLITE_UTF16BE       = 3    # IMP: R-51971-34154
SQLITE_UTF16         = 4    # Use native byte order
SQLITE_ANY           = 5    # Deprecated
SQLITE_UTF16_ALIGNED = 8    # sqlite3_create_collation only

# Function Flags
SQLITE_DETERMINISTIC   = 0x000000800
SQLITE_DIRECTONLY      = 0x000080000
SQLITE_SUBTYPE         = 0x000100000

# Obtaining SQL Values
@annotate
def sqlite3_value_blob(value: sqlite3_value_p) -> c_void_p:
    pass

@annotate
def sqlite3_value_double(value: sqlite3_value_p) -> c_double:
    pass

@annotate
def sqlite3_value_int(value: sqlite3_value_p) -> c_int:
    pass

@annotate
def sqlite3_value_int64(value: sqlite3_value_p) -> sqlite3_int64:
    pass

# @annotate
# def sqlite3_value_pointer(value: sqlite3_value_p, type: c_char_p) -> c_void_p:
#     pass

@annotate
def sqlite3_value_text(value: sqlite3_value_p) -> c_void_p:
    pass

@annotate
def sqlite3_value_bytes(value: sqlite3_value_p) -> c_int:
    pass

@annotate
def sqlite3_value_type(value: sqlite3_value_p) -> c_int:
    pass

@annotate
def sqlite3_value_numeric_type(value: sqlite3_value_p) -> c_int:
    pass

# @annotate
# def sqlite3_value_nochange(value: sqlite3_value_p) -> c_int:
#     pass

# Finding The Subtype Of SQL Values
# @annotate
# def sqlite3_value_subtype(value: sqlite3_value_p) -> c_uint:
#     pass

# Copy And Free SQL Values
@annotate
def sqlite3_value_dup(value: sqlite3_value_p) -> sqlite3_value_p:
    pass

@annotate
def sqlite3_value_free(value: sqlite3_value_p):
    pass

# Obtain Aggregate Function Context
@annotate
def sqlite3_aggregate_context(context: sqlite3_context_p, nBytes: c_int) -> c_void_p:
    pass

# User Data For Functions
@annotate
def sqlite3_user_data(context: sqlite3_context_p) -> c_void_p:
    pass

# Database Connection For Functions
@annotate
def sqlite3_context_db_handle(context: sqlite3_context_p) -> sqlite3_p:
    pass

# Function Auxiliary Data
@annotate
def sqlite3_get_auxdata(context: sqlite3_context_p, N: c_int) -> c_void_p:
    pass

@annotate
def sqlite3_set_auxdata(context: sqlite3_context_p, N: c_int, data: c_void_p, destructor: sqlite3_destructor_type):
    pass

# Setting The Result Of An SQL Function
@annotate
def sqlite3_result_blob64(context: sqlite3_context_p, value: c_void_p, nBytes: sqlite3_uint64, destructor: sqlite3_destructor_type):
    pass

@annotate
def sqlite3_result_double(context: sqlite3_context_p, value: c_double):
    pass

@annotate
def sqlite3_result_error(context: sqlite3_context_p, message: c_char_p, nBytes: c_int):
    pass

@annotate
def sqlite3_result_error_toobig(context: sqlite3_context_p):
    pass

@annotate
def sqlite3_result_error_nomem(context: sqlite3_context_p):
    pass

@annotate
def sqlite3_result_error_code(context: sqlite3_context_p, error: c_int):
    pass

@annotate
def sqlite3_result_int(context: sqlite3_context_p, value: c_int):
    pass

@annotate
def sqlite3_result_int64(context: sqlite3_context_p, value: sqlite3_int64):
    pass

@annotate
def sqlite3_result_null(context: sqlite3_context_p):
    pass

@annotate
def sqlite3_result_text64(context: sqlite3_context_p, value: c_char_p, nBytes: sqlite3_uint64, destructor: sqlite3_destructor_type, encoding: c_ubyte):
    pass

@annotate
def sqlite3_result_value(context: sqlite3_context_p, value: sqlite3_value_p):
    pass

# @annotate
# def sqlite3_result_pointer(context: sqlite3_context_p, value: c_void_p, type: c_char_p, destructor: sqlite3_destructor_type):
#     pass

@annotate
def sqlite3_result_zeroblob64(context: sqlite3_context_p, n: sqlite3_uint64) -> c_int:
    pass

# Setting The Subtype Of An SQL Function
# @annotate
# def sqlite3_result_subtype(context: sqlite3_context_p, subtype: c_uint):
#     pass

# Define New Collating Sequences
@annotate
def sqlite3_create_collation_v2(
        db: sqlite3_p,
        zName: c_char_p,
        eTextRep: c_int,
        pArg: c_void_p,
        xCompare: c_void_p,
        xDestroy: sqlite3_destructor_type) -> c_int:
    pass

# Collation Needed Callbacks
@annotate
def sqlite3_collation_needed(db: sqlite3_p, pArg: c_void_p, callback: c_void_p) -> c_int:
    pass

# Suspend Execution For A Short Time
@annotate
def sqlite3_sleep(ms: c_int) -> c_int:
    pass

# Test For Auto-Commit Mode
@annotate
def sqlite3_get_autocommit(db: sqlite3_p) -> c_int:
    pass

# Find The Database Handle Of A Prepared Statement
@annotate
def sqlite3_db_handle(pStmt: sqlite3_stmt_p) -> sqlite3_p:
    pass

# Return The Filename For A Database Connection
@annotate
def sqlite3_db_filename(db: sqlite3_p, zDbName: c_char_p) -> c_char_p:
    pass

# Determine if a database is read-only
@annotate
def sqlite3_db_readonly(db: sqlite3_p, zDbName: c_char_p) -> c_int:
    pass

# Find the next prepared statement
@annotate
def sqlite3_next_stmt(db: sqlite3_p, pStmt: sqlite3_stmt_p) -> sqlite3_stmt_p:
    pass

# Commit And Rollback Notification Callbacks
@annotate
def sqlite3_commit_hook(db: sqlite3_p, callback: c_void_p, pArg: c_void_p) -> c_void_p:
    pass

@annotate
def sqlite3_rollback_hook(db: sqlite3_p, callback: c_void_p) -> c_void_p:
    pass

# Data Change Notification Callbacks
@annotate
def sqlite3_update_hook(db: sqlite3_p, callback: c_void_p, pArg: c_void_p) -> c_void_p:
    pass

# Enable Or Disable Shared Pager Cache
@annotate
def sqlite3_enable_shared_cache(onoff: c_int):
    pass

# Attempt To Free Heap Memory
@annotate
def sqlite3_release_memory(n: c_int) -> c_int:
    pass

# Free Memory Used By A Database Connection
@annotate
def sqlite3_db_release_memory(db: sqlite3_p) -> c_int:
    pass

# Impose A Limit On Heap Size
@annotate
def sqlite3_soft_heap_limit64(n: sqlite3_int64) -> sqlite3_int64:
    pass

# Extract Metadata About A Column Of A Table
@annotate
def sqlite3_table_column_metadata(
  db: sqlite3_p,                    # Connection handle
  zDbName: c_char_p,                # Database name or NULL
  zTableName: c_char_p,             # Table name
  zColumnName: c_char_p,            # Column name
  pzDataType: POINTER(c_char_p),    # OUTPUT: Declared data type
  pzCollSeq: POINTER(c_char_p),     # OUTPUT: Collation sequence name
  pNotNull: POINTER(c_int),         # OUTPUT: True if NOT NULL constraint exists
  pPrimaryKey: POINTER(c_int),      # OUTPUT: True if column part of PK
  pAutoinc: POINTER(c_int)          # OUTPUT: True if column is auto-increment
) -> c_int:
    pass

# Load An Extension
@annotate
def sqlite3_load_extension(
  db: sqlite3_p,               # Load the extension into this database connection
  zFile: c_char_p,             # Name of the shared library containing extension
  zProc: c_char_p,             # Entry point.  Derived from zFile if 0
  pzErrMsg: POINTER(c_char_p)  # Put error message here if not 0
) -> c_int:
    pass

# Enable Or Disable Extension Loading
@annotate
def sqlite3_enable_load_extension(db: sqlite3_p, onoff: c_int) -> c_int:
    pass

# Automatically Load Statically Linked Extensions
@annotate
def sqlite3_auto_extension(xEntryPoint: c_void_p) -> c_int:
    pass

# Cancel Automatic Extension Loading
@annotate
def sqlite3_cancel_auto_extension(xEntryPoint: c_void_p) -> c_int:
    pass

# Reset Automatic Extension Loading
@annotate
def sqlite3_reset_auto_extension():
    pass

# Structures used by the virtual table interface

class sqlite3_vtab(Structure):
    pass

class sqlite3_index_info(Structure):
    pass

class sqlite3_vtab_cursor(Structure):
    pass

class sqlite3_module(Structure):
    pass

# Virtual Table Object
sqlite3_module._fields_ = [
    ("iVersion", c_int),
    ("xCreate", c_void_p),
    ("xConnect", c_void_p),
    ("xBestIndex", c_void_p),
    ("xDisconnect", c_void_p),
    ("xDestroy", c_void_p),
    ("xOpen", c_void_p),
    ("xClose", c_void_p),
    ("xFliter", c_void_p),
    ("xNext", c_void_p),
    ("xEof", c_void_p),
    ("xColumn", c_void_p),
    ("xRowid", c_void_p),
    ("xUpdate", c_void_p),
    ("xBegin", c_void_p),
    ("xSync", c_void_p),
    ("xCommit", c_void_p),
    ("xRollback", c_void_p),
    ("xFindFunction", c_void_p),
    ("xRename", c_void_p),
    # The methods above are in version 1 of the sqlite_module object. Those
    # below are for version 2 and greater.
    ("xSavepoint", c_void_p),
    ("xRelease", c_void_p),
    ("xRollbackTo", c_void_p),
    # The methods above are in versions 1 and 2 of the sqlite_module object.
    # Those below are for version 3 and greater.
    ("xShadowName", c_void_p),
]

# Virtual Table Indexing Information
class sqlite3_index_constraint(Structure):
    _fields_ = [
        ("iColumn", c_int),       # Column constrained.  -1 for ROWID
        ("op", c_ubyte),          # Constraint operator
        ("usable", c_ubyte),      # True if this constraint is usable
        ("iTermOffset", c_int),   # Used internally - xBestIndex should ignore
    ]

class sqlite3_index_orderby(Structure):
    _fields_ = [
        ("iColumn", c_int),              # Column number
        ("desc", c_ubyte),               # True for DESC.  False for ASC
    ]

class sqlite3_index_constraint_usage(Structure):
    _fields_ = [
        ("argvIndex", c_int),          # if >0, constraint is part of argv to xFilter
        ("omit", c_ubyte),             # Do not code a test for this constraint
    ]

sqlite3_index_info._fields_ = [
    # Inputs
    ("nConstraint", c_int),                              # Number of entries in aConstraint
    ("aConstraint", POINTER(sqlite3_index_constraint)),  # Table of WHERE clause constraints
    ("nOrderBy", c_int),                                 # Number of terms in the ORDER BY clause
    ("aOrderBy", POINTER(sqlite3_index_orderby)),        # The ORDER BY clause
    # Outputs
    ("aConstraintUsage", POINTER(sqlite3_index_constraint_usage)),
    ("idxNum", c_int),                                   # Number used to identify the index
    ("idxStr", c_char_p),                                # String, possibly obtained from sqlite3_malloc
    ("needToFreeIdxStr", c_int),                         # Free idxStr using sqlite3_free() if true
    ("orderByConsumed", c_int),                          # True if output is already ordered
    ("estimatedCost", c_double),                         # Estimated cost of using this index
    # Fields below are only available in SQLite 3.8.2 and later
    ("estimatedRows", sqlite3_int64),                    # Estimated number of rows returned
    # Fields below are only available in SQLite 3.9.0 and later
    ("idxFlags", c_int),                                 # Mask of SQLITE_INDEX_SCAN_* flags
    # Fields below are only available in SQLite 3.10.0 and later
    ("colUsed", sqlite3_uint64),                         # Input: Mask of columns used by statement
]

# Virtual Table Scan Flags
SQLITE_INDEX_SCAN_UNIQUE      = 1    # Scan visits at most 1 row

# Virtual Table Constraint Operator Codes
SQLITE_INDEX_CONSTRAINT_EQ        =   2
SQLITE_INDEX_CONSTRAINT_GT        =   4
SQLITE_INDEX_CONSTRAINT_LE        =   8
SQLITE_INDEX_CONSTRAINT_LT        =  16
SQLITE_INDEX_CONSTRAINT_GE        =  32
SQLITE_INDEX_CONSTRAINT_MATCH     =  64
SQLITE_INDEX_CONSTRAINT_LIKE      =  65
SQLITE_INDEX_CONSTRAINT_GLOB      =  66
SQLITE_INDEX_CONSTRAINT_REGEXP    =  67
SQLITE_INDEX_CONSTRAINT_NE        =  68
SQLITE_INDEX_CONSTRAINT_ISNOT     =  69
SQLITE_INDEX_CONSTRAINT_ISNOTNULL =  70
SQLITE_INDEX_CONSTRAINT_ISNULL    =  71
SQLITE_INDEX_CONSTRAINT_IS        =  72
SQLITE_INDEX_CONSTRAINT_FUNCTION  = 150

# Register A Virtual Table Implementation
@annotate
def sqlite3_create_module(
  db: sqlite3_p,               # SQLite connection to register module with
  zName: c_char_p,             # Name of the module
  p: POINTER(sqlite3_module),  # Methods for the module
  pClientData: c_void_p        # Client data for xCreate/xConnect
) -> c_int:
    pass

@annotate
def sqlite3_create_module_v2(
  db: sqlite3_p,                     # SQLite connection to register module with
  zName: c_char_p,                   # Name of the module
  p: POINTER(sqlite3_module),        # Methods for the module
  pClientData: c_void_p,             # Client data for xCreate/xConnect
  xDestroy: sqlite3_destructor_type  # Module destructor function
) -> c_int:
    pass


# Remove Unnecessary Virtual Table Implementations
def sqlite3_drop_modules(
    db: sqlite3_p,           # Remove modules from this connection
    azKeep: c_char_p         # Except, do not remove the ones named here
) -> c_int:
    pass


# Virtual Table Instance Object
sqlite3_vtab._fields_ = [
  ("pModule", POINTER(sqlite3_module)),   # The module for this virtual table
  ("nRef", c_int),                        # Number of open cursors
  ("zErrMsg", c_char_p),                  # Error message from sqlite3_mprintf()
  # Virtual table implementations will typically add additional fields
]

# Virtual Table Cursor Object
sqlite3_vtab_cursor._fields_ = [
    ("pVTab", POINTER(sqlite3_vtab)),    # Virtual table of this cursor
    # Virtual table implementations will typically add additional fields
]

# Declare The Schema Of A Virtual Table
@annotate
def sqlite3_declare_vtab(db: sqlite3_p, zSQL: c_char_p) -> c_int:
    pass

# Overload A Function For A Virtual Table
@annotate
def sqlite3_overload_function(db: sqlite3_p, zFuncName: c_char_p, nArg: c_int) -> c_int:
    pass

# A Handle To An Open BLOB
sqlite3_blob_p = c_void_p

# Open A BLOB For Incremental I/O
@annotate
def sqlite3_blob_open(
    db: sqlite3_p,
    zDb: c_char_p,
    zTable: c_char_p,
    zColumn: c_char_p,
    iRow: sqlite3_int64,
    flags: c_int,
    ppBlob: POINTER(sqlite3_blob_p)) -> c_int:
    pass

# Move a BLOB Handle to a New Row
@annotate
def sqlite3_blob_reopen(blob: sqlite3_blob_p, iRow: sqlite3_int64) -> c_int:
    pass

# Close A BLOB Handle
@annotate
def sqlite3_blob_close(blob: sqlite3_blob_p) -> c_int:
    pass

# Return The Size Of An Open BLOB
@annotate
def sqlite3_blob_bytes(blob: sqlite3_blob_p) -> c_int:
    pass

# Read Data From A BLOB Incrementally
@annotate
def sqlite3_blob_read(blob: sqlite3_blob_p, z: c_void_p, n: c_int, iOffset: c_int) -> c_int:
    pass

# Write Data Into A BLOB Incrementally
@annotate
def sqlite3_blob_write(blob: sqlite3_blob_p, z: c_void_p, n: c_int, iOffset: c_int) -> c_int:
    pass

# Virtual File System Objects
@annotate
def sqlite3_vfs_find(zVfsName: c_char_p) -> POINTER(sqlite3_vfs):
    pass


@annotate
def sqlite3_vfs_register(vfs: POINTER(sqlite3_vfs), makeDflt: c_int) -> c_int:
    pass

@annotate
def sqlite3_vfs_unregister(vfs: POINTER(sqlite3_vfs)) -> c_int:
    pass

# Mutexes
@annotate
def sqlite3_mutex_alloc(type: c_int) -> sqlite3_mutex_p:
    pass

@annotate
def sqlite3_mutex_free(mutex: sqlite3_mutex_p):
    pass

@annotate
def sqlite3_mutex_enter(mutex: sqlite3_mutex_p):
    pass

@annotate
def sqlite3_mutex_try(mutex: sqlite3_mutex_p) -> c_int:
    pass

@annotate
def sqlite3_mutex_leave(mutex: sqlite3_mutex_p):
    pass

# Mutex Methods Object
class sqlite3_mutex_methods(Structure):
    _fields_ = [
        ("xMutexInit", c_void_p),
        ("xMutexEnd", c_void_p),
        ("xMutexAlloc", c_void_p),
        ("xMutexFree", c_void_p),
        ("xMutexEnter", c_void_p),
        ("xMutexTry", c_void_p),
        ("xMutexLeave", c_void_p),
        ("xMutexHeld", c_void_p),
        ("xMutexNotheld", c_void_p),
    ]

# Mutex Types
SQLITE_MUTEX_FAST            =  0
SQLITE_MUTEX_RECURSIVE       =  1
SQLITE_MUTEX_STATIC_MASTER   =  2
SQLITE_MUTEX_STATIC_MEM      =  3  # sqlite3_malloc()
SQLITE_MUTEX_STATIC_MEM2     =  4  # NOT USED
SQLITE_MUTEX_STATIC_OPEN     =  4  # sqlite3BtreeOpen()
SQLITE_MUTEX_STATIC_PRNG     =  5  # sqlite3_randomness()
SQLITE_MUTEX_STATIC_LRU      =  6  # lru page list
SQLITE_MUTEX_STATIC_LRU2     =  7  # NOT USED
SQLITE_MUTEX_STATIC_PMEM     =  7  # sqlite3PageMalloc()
SQLITE_MUTEX_STATIC_APP1     =  8  # For use by application
SQLITE_MUTEX_STATIC_APP2     =  9  # For use by application
SQLITE_MUTEX_STATIC_APP3     = 10  # For use by application
SQLITE_MUTEX_STATIC_VFS1     = 11  # For use by built-in VFS
SQLITE_MUTEX_STATIC_VFS2     = 12  # For use by extension VFS
SQLITE_MUTEX_STATIC_VFS3     = 13  # For use by application VFS

# Retrieve the mutex for a database connection
@annotate
def sqlite3_db_mutex(db: sqlite3_p) -> sqlite3_mutex_p:
    pass

# Low-Level Control Of Database Files
@annotate
def sqlite3_file_control(db: sqlite3_p, zDbName: c_char_p, op: c_int, pArg: c_void_p):
    pass

# SQL Keyword Checking
# @annotate
# def sqlite3_keyword_count() -> c_int:
#     pass

# @annotate
# def sqlite3_keyword_name(N: c_int, Z: POINTER(c_char_p), L: POINTER(c_int)) -> c_int:
#     pass

# @annotate
# def sqlite3_keyword_check(Z: POINTER(c_char_p), L: POINTER(c_int)) -> c_int:
#     pass

# SQLite Runtime Status
@annotate
def sqlite3_status64(op: c_int, pCurrent: POINTER(sqlite3_int64), pHighwater: POINTER(sqlite3_int64), resetFlag: c_int) -> c_int:
    pass

# Status Parameters
SQLITE_STATUS_MEMORY_USED          = 0
SQLITE_STATUS_PAGECACHE_USED       = 1
SQLITE_STATUS_PAGECACHE_OVERFLOW   = 2
SQLITE_STATUS_SCRATCH_USED         = 3  # NOT USED
SQLITE_STATUS_SCRATCH_OVERFLOW     = 4  # NOT USED
SQLITE_STATUS_MALLOC_SIZE          = 5
SQLITE_STATUS_PARSER_STACK         = 6
SQLITE_STATUS_PAGECACHE_SIZE       = 7
SQLITE_STATUS_SCRATCH_SIZE         = 8  # NOT USED
SQLITE_STATUS_MALLOC_COUNT         = 9

# Database Connection Status
@annotate
def sqlite3_db_status(db: sqlite3_p, op: c_int, pCur: POINTER(c_int), pHiwtr: POINTER(c_int), resetFlg: c_int) -> c_int:
    pass

# Status Parameters for database connections
SQLITE_DBSTATUS_LOOKASIDE_USED      =  0
SQLITE_DBSTATUS_CACHE_USED          =  1
SQLITE_DBSTATUS_SCHEMA_USED         =  2
SQLITE_DBSTATUS_STMT_USED           =  3
SQLITE_DBSTATUS_LOOKASIDE_HIT       =  4
SQLITE_DBSTATUS_LOOKASIDE_MISS_SIZE =  5
SQLITE_DBSTATUS_LOOKASIDE_MISS_FULL =  6
SQLITE_DBSTATUS_CACHE_HIT           =  7
SQLITE_DBSTATUS_CACHE_MISS          =  8
SQLITE_DBSTATUS_CACHE_WRITE         =  9
SQLITE_DBSTATUS_DEFERRED_FKS        = 10
SQLITE_DBSTATUS_CACHE_USED_SHARED   = 11
SQLITE_DBSTATUS_CACHE_SPILL         = 12
SQLITE_DBSTATUS_MAX                 = 12   # Largest defined DBSTATUS

# Prepared Statement Status
@annotate
def sqlite3_stmt_status(pStmt: sqlite3_stmt_p, op: c_int, resetFlg: c_int) -> c_int:
    pass

# Status Parameters for prepared statements
SQLITE_STMTSTATUS_FULLSCAN_STEP     = 1
SQLITE_STMTSTATUS_SORT              = 2
SQLITE_STMTSTATUS_AUTOINDEX         = 3
SQLITE_STMTSTATUS_VM_STEP           = 4
SQLITE_STMTSTATUS_REPREPARE         = 5
SQLITE_STMTSTATUS_RUN               = 6
SQLITE_STMTSTATUS_MEMUSED           = 99

# Custom Page Cache Object
sqlite3_pcache_p = c_void_p

# Custom Page Cache Object
class sqlite3_pcache_page(Structure):
    _fields_ = [
        ("pBuf", c_void_p),        # The content of the page
        ("pExtra", c_void_p),      # Extra information associated with the page
    ]

# Application Defined Page Cache
class sqlite3_pcache_methods2(Structure):
    _fields_ = [
        ("iVersion", c_int),
        ("pArg", c_void_p),
        ("xInit", c_void_p),
        ("xShutdown", c_void_p),
        ("xCreate", c_void_p),
        ("xCachesize", c_void_p),
        ("xPagecount", c_void_p),
        ("xFetch", c_void_p),
        ("xUnpin", c_void_p),
        ("xRekey", c_void_p),
        ("xTruncate", c_void_p),
        ("xDestroy", c_void_p),
        ("xShrink", c_void_p),
    ]

# Online Backup Object
sqlite3_backup_p = c_void_p

@annotate
def sqlite3_backup_init(
    pDest: sqlite3_p,                    # Destination database handle
    zDestName: c_char_p,                 # Destination database name
    pSource: sqlite3_p,                  # Source database handle
    zSourceName: c_char_p                # Source database name
) -> sqlite3_backup_p:
    pass

@annotate
def sqlite3_backup_step(p: sqlite3_backup_p, nPage: c_int) -> c_int:
    pass

@annotate
def sqlite3_backup_finish(p: sqlite3_backup_p) -> c_int:
    pass

@annotate
def sqlite3_backup_remaining(p: sqlite3_backup_p) -> c_int:
    pass

@annotate
def sqlite3_backup_pagecount(p: sqlite3_backup_p) -> c_int:
    pass

# Error Logging Interface
sqlite3_log = libsqlite.sqlite3_log

# Write-Ahead Log Commit Hook
@annotate
def sqlite3_wal_hook(db: sqlite3_p, callback: c_void_p, pArg: c_void_p) -> c_void_p:
    pass

# Configure an auto-checkpoint
@annotate
def sqlite3_wal_autocheckpoint(db: sqlite3_p, N: c_int) -> c_int:
    pass

# Checkpoint a database
@annotate
def sqlite3_wal_checkpoint(db: sqlite3_p, zDb: c_char_p) -> c_int:
    pass

# Checkpoint a database
@annotate
def sqlite3_wal_checkpoint_v2(
  db: sqlite3_p,                # Database handle
  zDb: c_char_p,                # Name of attached database (or NULL)
  eMode: c_int,                 # SQLITE_CHECKPOINT_* value
  pnLog: POINTER(c_int),        # OUT: Size of WAL log in frames
  pnCkpt: POINTER(c_int)        # OUT: Total number of frames checkpointed
) -> c_int:
    pass

# Checkpoint Mode Values
SQLITE_CHECKPOINT_PASSIVE  = 0  # Do as much as possible w/o blocking
SQLITE_CHECKPOINT_FULL     = 1  # Wait for writers, then checkpoint
SQLITE_CHECKPOINT_RESTART  = 2  # Like FULL but wait for for readers
SQLITE_CHECKPOINT_TRUNCATE = 3  # Like RESTART but also truncate WAL

# Virtual Table Interface Configuration
sqlite3_vtab_config = libsqlite.sqlite3_vtab_config

# Virtual Table Configuration Options
SQLITE_VTAB_CONSTRAINT_SUPPORT = 1

# Determine The Virtual Table Conflict Policy
@annotate
def sqlite3_vtab_on_conflict(db: sqlite3_p) -> c_int:
    pass

# Determine If Virtual Table Column Access Is For UPDATE
# @annotate
# def sqlite3_vtab_nochange(context: sqlite3_context_p) -> c_int:
#     pass

# conflict resolution modes
SQLITE_ROLLBACK = 1
# SQLITE_IGNORE = 2 # Also used by sqlite3_authorizer() callback
SQLITE_FAIL     = 3
# SQLITE_ABORT  = 4  # Also an error code
SQLITE_REPLACE  = 5

# Flush caches to disk mid-transaction
# @annotate
# def sqlite3_db_cacheflush(db: sqlite3_p) -> c_int:
#     pass


def sqlite3_value(arg):
    t = sqlite3_value_type(arg)
    if t == SQLITE_NULL:
        return None
    elif t == SQLITE_INTEGER:
        return sqlite3_value_int64(arg)
    elif t == SQLITE_FLOAT:
        return sqlite3_value_double(arg)
    elif t == SQLITE_TEXT:
        return string_at(sqlite3_value_text(arg), sqlite3_value_bytes(arg)).decode()
    elif t == SQLITE_BLOB:
        return string_at(sqlite3_value_blob(arg), sqlite3_value_bytes(arg))
    else:
        assert False

def sqlite3_result(ctx, value):
    if value is None:
        sqlite3_result_null(ctx)
    elif isinstance(value, int):
        sqlite3_result_int64(ctx, value)
    elif isinstance(value, float):
        sqlite3_result_double(ctx, value)
    elif isinstance(value, str):
        value = value.encode()
        sqlite3_result_text64(ctx, value, len(value), SQLITE_TRANSIENT, SQLITE_UTF8)
    elif isinstance(value, bytes):
        sqlite3_result_blob64(ctx, value, len(value), SQLITE_TRANSIENT)
    else:
        assert False


class Statement:

    def __init__(self):
        self._stmt = sqlite3_stmt_p(None)

    def sql(self):
        return sqlite3_sql(self._stmt)

    def expanded_sql(self):
        return sqlite3_expanded_sql(self._stmt)

    def normalized_sql(self):
        return sqlite3_normalized_sql(self._stmt)

    def readonly(self):
        return bool(sqlite3_stmt_readonly(self._stmt))

    def isexplain(self):
        return sqlite3_stmt_isexplain(self._stmt)

    def busy(self):
        return sqlite3_stmt_busy(self._stmt)

    def _bind_parameter(self, index, value):
        if value is None:
            return sqlite3_bind_null(self._stmt, index)
        elif isinstance(value, int):
            return sqlite3_bind_int64(self._stmt, index, value)
        elif isinstance(value, float):
            return sqlite3_bind_double(self._stmt, index, value)
        elif isinstance(value, str):
            s = value.encode()
            return sqlite3_bind_text64(self._stmt, index, s, len(s), SQLITE_TRANSIENT, SQLITE_UTF8)
        elif isinstance(value, bytes):
            return sqlite3_bind_blob64(self._stmt, index, value, len(value), SQLITE_TRANSIENT)
        elif isinstance(value, memoryview):
            return sqlite3_bind_blob64(self._stmt, index, value.tobytes(), len(value), SQLITE_TRANSIENT)
        else:
            return -1

    def bind(self, name, value):
        if isinstance(name, int):
            return self._bind_parameter(name, value)

    def bind_parameter_count(self):
        return sqlite3_bind_parameter_count(self._stmt)

    def bind_parameter_name(self, index):
        return sqlite3_bind_parameter_name(self._stmt, index)

    def bind_parameter_index(self, name):
        return sqlite3_bind_parameter_index(self._stmt, name)

    def clear_bindings(self):
        return sqlite3_clear_bindings(self._stmt)

    def column_count(self):
        return sqlite3_column_count(self._stmt)

    def column_name(self, index):
        return sqlite3_column_name(self._stmt, index)

    # def column_database_name(self, index):
    #     return sqlite3_column_database_name(self._stmt, index)

    # def column_table_name(self, index):
    #     return sqlite3_column_table_name(self._stmt, index)

    # def column_origin_name(self, index):
    #     return sqlite3_column_origin_name(self._stmt, index)

    def column_decltype(self, index):
        return sqlite3_column_decltype(self._stmt, index)

    def step(self):
        rc = sqlite3_step(self._stmt)
        # if rc not in (SQLITE_DONE, SQLITE_ROW):
        #     self.reset()
        return rc

    def data_count(self):
        return sqlite3_data_count(self._stmt)

    def column_type(self, index):
        return sqlite3_column_type(self._stmt, index)

    def column_int(self, index):
        return sqlite3_column_int64(self._stmt, index)

    def column_double(self, index):
        return sqlite3_column_double(self._stmt, index)

    def column_text(self, index):
        nbytes = sqlite3_column_bytes(self._stmt, index)
        s = sqlite3_column_text(self._stmt, index)
        return string_at(s, nbytes)

    def column_blob(self, index):
        nbytes = sqlite3_column_bytes(self._stmt, index)
        b = sqlite3_column_blob(self._stmt, index)
        return string_at(b, nbytes)

    def column(self, index, text_factory=str):
        coltype = sqlite3_column_type(self._stmt, index)
        if coltype == SQLITE_NULL:
            return None
        elif coltype == SQLITE_INTEGER:
            return sqlite3_column_int64(self._stmt, index)
        elif coltype == SQLITE_FLOAT:
            return sqlite3_column_double(self._stmt, index)
        elif coltype == SQLITE_TEXT:
            nbytes = sqlite3_column_bytes(self._stmt, index)
            s = sqlite3_column_text(self._stmt, index)
            b = string_at(s, nbytes)
            if text_factory is str:
                return b.decode()
            else:
                return text_factory(b)
        elif coltype == SQLITE_BLOB:
            nbytes = sqlite3_column_bytes(self._stmt, index)
            b = sqlite3_column_blob(self._stmt, index)
            return string_at(b, nbytes)
        else:
            assert False

    def db_handle(self):
        return sqlite3_db_handle(self._stmt)

    def reset(self):
        return sqlite3_reset(self._stmt)

    def finalize(self):
        return sqlite3_finalize(self._stmt)


class Database:

    def __init__(self):
        self._db = sqlite3_p(None)

    def open(self, filename, flags, vfs=None):
        return sqlite3_open_v2(filename, byref(self._db), flags, vfs)

    def close(self):
        return sqlite3_close(self._db)

    def close_v2(self):
        return sqlite3_close_v2(self._db)

    def extended_result_codes(self, onoff):
        return sqlite3_extended_result_codes(self._db, onoff)

    def last_insert_rowid(self):
        return sqlite3_last_insert_rowid(self._db)

    def changes(self):
        return sqlite3_changes(self._db)

    def total_changes(self):
        return sqlite3_total_changes(self._db)

    def interrupt(self):
        sqlite3_interrupt(self._db)

    def set_authorizer(self, callback, arg):
        return sqlite3_set_authorizer(self._db, callback, arg)

    def trace(self, callback, arg):
        sqlite3_trace(self._db, callback, arg)

    def progress_handler(self, n, handler, arg):
        sqlite3_progress_handler(self._db, n, handler, arg)

    def errcode(self):
        return sqlite3_errcode(self._db)

    def errmsg(self):
        return sqlite3_errmsg(self._db)

    def extended_errcode(self):
        return sqlite3_extended_errcode(self._db)

    def limit(self, key, val):
        return sqlite3_limit(self._db, key, val)

    def prepare(self, sql):
        stmt = Statement()
        tail = c_void_p(None)
        rc = sqlite3_prepare_v2(
            self._db,
            sql,
            len(sql),
            byref(stmt._stmt),
            byref(tail))
        if rc == SQLITE_OK:
            if stmt._stmt.value is not None:
                b = cast(c_char_p(sql), c_void_p)
                return rc, stmt, sql[tail.value - b.value:]

        return rc, None, b''

    def create_function(self, name, narg, eTextRep, arg, func, step, final):
        return sqlite3_create_function_v2(
            self._db, name, narg, eTextRep, arg, func, step, final, SQLITE_STATIC)

    def create_aggregate(self, name, narg, eTextRep, klass):
        if klass is None:
            return sqlite3_create_function_v2(
                self._db, name, narg, eTextRep,
                None, None, None, None, SQLITE_STATIC)
        else:
            return sqlite3_create_function_v2(
                self._db, name, narg, eTextRep,
                id(klass), None, _aggregate_step, _aggregate_final, SQLITE_STATIC)

    def create_collation(self, name, callback, arg):
        return sqlite3_create_collation_v2(self._db, name, SQLITE_UTF8, arg, callback, SQLITE_STATIC)

    def get_autocommit(self):
        return bool(sqlite3_get_autocommit(self._db))

    def filename(self, dbname):
        return sqlite3_db_filename(self._db, dbname)

    def readonly(self, dbname):
        return sqlite3_db_readonly(self._db, dbname)

    def backup(self, name, src, src_name):
        return Backup(self, name, src, src_name)

class Backup:

    def __init__(self, dst, dst_name, src, src_name):
        self._backup = sqlite3_backup_p(sqlite3_backup_init(dst._db, dst_name, src._db, src_name))

    def step(self, pages, sleep_ms):
        while True:
            rc = sqlite3_backup_step(self._backup, pages)
            if rc not in (SQLITE_BUSY, SQLITE_LOCKED):
                break
            sqlite3_sleep(sleep_ms)
        return rc

    def remaining(self):
        return sqlite3_backup_remaining(self._backup)

    def pagecount(self):
        return sqlite3_backup_pagecount(self._backup)

    def __del__(self):
        sqlite3_backup_finish(self._backup)
