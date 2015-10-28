import pydwimmer.builtin.core
import pydwimmer.builtin.ints
import pydwimmer.compiler
import pydwimmer.terms
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

@pydwimmer.compiler.dwim
def list_integers(n):
    """what is a list of the first [n] integers?"""
    decrement_if_nonzero(n)
    with one_less_is(m):
        pydwimmer.builtin.lists.list_integers(m)
        with pydwimmer.builtin.core.answer(A):
            return snoc(n, A)
    with is_zero():
        return []

@pydwimmer.compiler.dwim
def decrement_if_nonzero(n):
    """is [n] zero? if not, what is one less than it?"""
    n
    with pydwimmer.builtin.ints.double(x):
        pydwimmer.builtin.lists.decrement_if_nonzero(x)
        with one_less_is(m):
            raise one_less_is(pydwimmer.builtin.ints.double_inc(m))
    with pydwimmer.builtin.ints.double_inc(x):
        ""
        pydwimmer.builtin.ints.compare_within_one(x, 0)
        with pydwimmer.builtin.ints.are_equal():
            raise one_less_is(0)
        with pydwimmer.builtin.ints.first_one_larger():
            raise one_less_is(pydwimmer.builtin.ints.double(x))
        with pydwimmer.builtin.ints.first_larger():
            raise one_less_is(pydwimmer.builtin.ints.double(x))
    with pydwimmer.builtin.ints.zero():
        raise is_zero()

@pydwimmer.terms.template
class one_less_is:
    """it is not zero, one less than it is [m]"""


@pydwimmer.terms.template
class is_zero:
    """it is zero"""


@pydwimmer.terms.template
class snoc:
    """the result of appending [last] to [init]"""

@pydwimmer.compiler.dwim
def length(l):
    """what is the length of [l]?"""
    l
    with snoc(last, init):
        length(init)
        with pydwimmer.builtin.core.answer(A):
            return A + 1
    with empty():
        return 0


@pydwimmer.compiler.dwim
def length_of_first_n(n):
    """what is the length of the list of the first [n] integers?"""
    pydwimmer.builtin.lists.list_integers(n)
    with pydwimmer.builtin.core.answer(A):
        length(A)
        with pydwimmer.builtin.core.answer(AA):
            return AA

