import re
import inspect
from types import CodeType as code, FunctionType as function
import sys
import contextlib
import os

modulename = __name__.split(".")[0]

"""
    uncompile credit:
    http://code.activestate.com/recipes/578353-code-to-source-and-back/
    Written by Oren Tirosh. Dec 1, 2012. Shared with MIT License.
"""
import __future__
PyCF_MASK = sum(v for k, v in vars(__future__).items() if k.startswith('CO_FUTURE'))

def uncompile(c):
    """ uncompile(codeobj) -> [source, filename, mode, flags, firstlineno, privateprefix] """
    if c.co_flags & inspect.CO_NESTED or c.co_freevars:
        raise Unsupported('nested functions not supported')
    if c.co_name == '<lambda>':
        raise Unsupported('lambda functions not supported')
    if c.co_filename == '<string>':
        raise Unsupported('code without source file not supported')

    filename = inspect.getfile(c)
    try:
        lines, firstlineno = inspect.getsourcelines(c)
    except IOError:
        raise NoSource('source code not available')
    source = ''.join(lines)

    # __X is mangled to _ClassName__X in methods. Find this prefix:
    privateprefix = None
    for name in c.co_names:
        m = re.match('^(_[A-Za-z][A-Za-z0-9_]*)__.*$', name)
        if m:
            privateprefix = m.group(1)
            break

    return [source, filename, firstlineno]
    return [source, filename, 'exec', c.co_flags & PyCF_MASK, firstlineno, privateprefix]


def remove_bracketed(s):
    unbracketed_parts = [""]
    bracketed_parts = []
    stack = []
    parens = {"[":"]", "{":"}", "(":")"}
    depth = 0
    openers = "[({"
    closers = "})]"
    for c in s:
        if c in parens.keys():
            if '[' in stack:
                bracketed_parts[-1] += c
            else:
                if c == '[':
                    bracketed_parts.append("")
                else:
                    unbracketed_parts[-1] += c
            stack.append(c)
        elif c in parens.values():
            if c != parens[stack[-1]]:
                raise ValueError("mismatched parens")
            stack = stack[:-1]
            if '[' in stack:
                bracketed_parts[-1] += c
            else:
                if c == ']':
                    unbracketed_parts.append("")
                elif c != ']':
                    unbracketed_parts[-1] += c
        else:
            if '[' in stack:
                bracketed_parts[-1] += c
            else:
                unbracketed_parts[-1] += c
    return "{}".join([double_chars(part, "{}") for part in unbracketed_parts]), bracketed_parts

def double_chars(s, chars):
    result = []
    for c in s:
        result.append(c)
        if c in chars:
            result.append(c)
    return "".join(result)

def permutation_from(a, b):
    """
    what is a permutation D such that the ith element of [a]
    is equal to the D(i)th element of [b], for every i?
    """
    removed = [False for _ in b]
    if len(a) != len(b):
        raise ValueError("the two lists are not permutations of each other")
    result = {}
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            if x == y and not removed[j]:
                result[i] = j
                removed[j] = True
                break
        else:
            raise ValueError("the two lists are not permutations of each other")
    return result

def index_in(x, ys):
    for i, y in enumerate(ys):
        if x == y:
            return i
    else:
        raise ValueError("that element does not appear in that list")

def module_path(x):
    name = inspect.getsourcefile(x)
    path = os.path.abspath(name)
    steps = path.split("/")
    module_index = index_in(modulename, steps)
    result = ".".join(steps[module_index:])
    result = ".".join(result.split(".")[:-1])
    return result

def first_line(x):
    return inspect.getsourcelines(x)[1]

"""credit:Alex Martelli, 2013
    http://stackoverflow.com/questions/2828953/
    silence-the-stdout-of-a-function-in-python-without-trashing-sys-stdout-and-resto
"""
class DummyFile(object):
    def write(self, x): pass

class ScreenedOut(object):
    def __init__(self, writer, f):
        self.writer = writer
        self.filter = f
        self.resume = True
        
    def write(self, x):
        if self.resume and self.filter(x):
            self.writer.write(x)
        else:
            self.resume = '\n' in x

def starts_with(prefixes, s):
    for prefix in prefixes:
        if len(s) >= len(prefix) and s[:len(prefix)] == prefix:
            return True
    else:
        return False

@contextlib.contextmanager
def noreloads():
    save_stdout = sys.stdout
    sys.stdout = ScreenedOut(sys.stdout, lambda x : not starts_with(["Reloading"], x))
    yield
    sys.stdout = save_stdout

@contextlib.contextmanager
def nostdout():
    save_stdout = sys.stdout
    sys.stdout = DummyFile()
    yield
    sys.stdout = save_stdout
