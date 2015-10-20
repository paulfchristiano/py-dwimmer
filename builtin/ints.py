import pydwimmer.builtin.core
import pydwimmer.builtin.ints
import ints
from pydwimmer.terms import template
from pydwimmer.compiler import dwim
from pydwimmer.builtin import core
from pydwimmer.builtin.bools import yes, no

def to_term(n):
    if n == 0:
        return zero()
    if n < 0:
        return negative(-n)
    if n % 2 == 0:
        return double(n / 2)
    if n % 2 == 1:
        return double_inc(n / 2)


@template
class double:
    """two times [x]"""
@template
class double_inc:
    """two times [x] plus one"""
@template
class zero:
    """the number zero"""
@template
class negative:
    """the additive inverse of [x]"""

@dwim
def add(x, y):
    """what is [x] + [y]?"""
    x
    with double(z):
        y
        with double(w):
            return double(z + w)
        with double_inc(w):
            return double_inc(z+w)
        with zero():
            return x
        with pydwimmer.builtin.ints.negative(x2):
            x2
            with pydwimmer.builtin.ints.double_inc(x3):
                minus(z, x3)
    with double_inc(z):
        y
        with double(w):
            return double_inc(z+w)
        with double_inc(w):
            return double(inc(z+w))
        with zero():
            return x
        with pydwimmer.builtin.ints.negative(x2):
            x2
    with zero():
        return y

@dwim
def minus(x, y):
    """what [x] - [y]?"""
    x
    with pydwimmer.builtin.ints.double_inc(x2):
        y
        with pydwimmer.builtin.ints.double_inc(x3):
            minus(x2, x3)
            with pydwimmer.builtin.core.answer(A):
                return double(A)
    with pydwimmer.builtin.ints.zero():
        return negative(y)

@dwim
def inc(x):
    """what is one more than [x]?"""
    return x + 1

@dwim
def eq(x, y):
    """is [x] equal to [y]?"""
    x
    with double(z):
        y
        with double(w):
            return z == w
        with double_inc(w):
            raise core.probably(no())
        with zero():
            return z == 0
    with double_inc(z):
        y
        with double(w):
            raise core.probably(no())
        with double_inc(w):
            return z == w
        with zero():
            return core.probably(no())
    with zero():
        y
        with zero():
            return yes()
        with double(z):
            return z == 0
        with double_inc(z):
            raise core.probably(no())

