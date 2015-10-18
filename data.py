import terms
from terms import template

@template
class empty:
    """the empty list"""

@template
class cons:
    """the list with first element {} and following elements in {}"""

def list_to_term(xs):
    result = empty()
    for x in reversed(xs):
        result = cons(x, result)
    return result

@template
class empty_dict:
    "the dictionary that doesn't map anything to anything"

@template
class dict_cons:
    "the dictionary that maps {} to {} and other keys according to {}"

def dict_to_term(x):
    result = empty_dict()
    for k, v in x.items():
        result = dict_cons(k, v, empty_dict)
    return result

@template
class double:
    """two times {}"""
@template
class double_inc:
    """two times {} plus one"""
@template
class zero:
    """the number zero"""
@template
class negative:
    """the additive inverse of {}"""

def int_to_term(n):
    if n == 0:
        return zero()
    if n < 0:
        return negative(-n)
    if n % 2 == 0:
        return double(n / 2)
    if n % 2 == 1:
        return double_inc(n / 2)

@template
class yes:
    """yes"""
@template
class no:
    """no"""

def bool_to_term(b):
    return yes() if b else no()

@template
class string:
    """the string with list of characters {}"""

def string_to_term(s):
    return string([char_to_term(c) for c in s])

@template
class char:
    """the character with ASCII code {}"""

def char_to_term(c):
    return char(ord(c))

@template
class meta:
    """what action should be taken in the setting with template {}?"""

@template
class answer:
    """the answer is {}"""
