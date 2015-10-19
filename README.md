# pydwimmer

The files in builtin/ demonstrate the syntax for writing new functions.
The file main.py illustrates the syntax for invoking functions.

You should install the directory as a package and make sure it is on your PYTHONPATH.
Commands are best executed with [vim-dwimmer](https://github.com/paulfchristiano/vim-dwimmer).

Objects manipulated by pydwimmer are typically instances of Term,
but many Python objects (lists, dictionaries, strings, ints, classes with docstrings...)
can be automatically converted to Terms.
