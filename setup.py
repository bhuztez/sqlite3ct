#!/usr/bin/env python3

from setuptools import setup

setup(
    name = 'sqlite3ct',
    version = '0.0.1',

    url = 'https://github.com/bhuztez/sqlite3ct',
    description = 'An implementation of the sqlite3 module using ctypes.',
    license = 'zlib/libpng license',

    classifiers = [
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: zlib/libpng License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3 :: Only",
    ],

    author = 'bhuztez',
    author_email = 'bhuztez@gmail.com',
    packages = ['sqlite3ct'],
)
