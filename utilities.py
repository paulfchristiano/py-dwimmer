import re
import inspect
from types import CodeType as code, FunctionType as function

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
    varname = r"[a-zA-Z_][a-zA-Z0-9_']*"
    result = []
    while True:
        m = re.match(r'(.*?)\[({})\](.*)'.format(varname), s, flags=re.DOTALL)
        if m is None:
            return s, result
        s = m.group(1) + "{}" + m.group(3)
        result.append(m.group(2))

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

