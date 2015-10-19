from pydwimmer.terms import template
from pydwimmer.compiler import dwim

@template
class empty:
    """the empty list"""

@template
class cons:
    """the list with first element [x] and following elements in [xs]"""

@template
class concatenation:
    """the concatenation of [a] and [b]"""

@template
class singleton:
    """the list with only element [x]"""


def to_term(xs):
    result = empty()
    for x in reversed(xs):
        result = cons(x, result)
    return result

@dwim
def reverse(xs):
    """what is the result of reversing [xs]?"""
    xs
    with cons(a, b):
        return reverse_and_cat(b, singleton(a))
    with empty():
        return empty()
    with concatenation(a, b):
        return concatenation(reverse(b), reverse(a))
    with singleton(a):
        return singleton(a)

@dwim
def reverse_and_cat(l, l2):
    """what is the result of reversing [l] and then concatenating it with [l2]?"""
    l
    with cons(a, b):
        return reverse_and_cat(b, cons(a, l2))
    with empty():
        return l2
    with concatenation(a, b):
        return concatenation(reverse(b), reverse_and_cat(b, l2))
    with singleton(a):
        return cons(a, l2)
