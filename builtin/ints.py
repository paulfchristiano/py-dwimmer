import pydwimmer.builtin.strings
import pydwimmer.builtin.dicts
import pydwimmer.builtin.bools
import pydwimmer.compiler
import pydwimmer.terms
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
    """what is [x] plus [y]?"""
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
                decrement(double(minus(z, x3)))
                with core.answer(result):
                    return result
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
    with pydwimmer.builtin.strings.string(chars):
        y
        with pydwimmer.builtin.strings.string(chars2):

@dwim
def minus(x, y):
    """what [x] minus [y]?"""
    x
    with pydwimmer.builtin.ints.double_inc(x2):
        y
        with pydwimmer.builtin.ints.double_inc(x3):
            minus(x2, x3)
            with pydwimmer.builtin.core.answer(A):
                return double(A)
        with pydwimmer.builtin.ints.double(x3):
            minus(x2, x3)
            with pydwimmer.builtin.core.answer(A):
                return double_inc(A)
        with pydwimmer.builtin.ints.zero():
            return x
    with pydwimmer.builtin.ints.zero():
        return negative(y)
    with pydwimmer.builtin.ints.double(x2):
        y
        with pydwimmer.builtin.ints.double_inc(x3):
            minus(x2, x3)
            with pydwimmer.builtin.core.answer(A):
                return decrement(double(A))
        with pydwimmer.builtin.ints.double(x3):
            minus(x2, x3)
            with pydwimmer.builtin.core.answer(A):
                return double(A)

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
    with pydwimmer.builtin.dicts.int_type():
        y
        with pydwimmer.builtin.dicts.int_type():
            return yes()

@pydwimmer.compiler.dwim
def decrement(x):
    """what is one less than [x]?"""
    x
    with pydwimmer.builtin.ints.double(x2):
        decrement(x2)
        with pydwimmer.builtin.core.answer(A):
            return double_inc(A)
    with pydwimmer.builtin.ints.negative(x2):
        inc(x2)
        with pydwimmer.builtin.core.answer(A):
            return negative(A)
    with pydwimmer.builtin.ints.double_inc(x2):
        return double(x2)

@dwim
def times(x, y):
    """what is [x] times [y]?"""
    x
    with pydwimmer.builtin.ints.double_inc(x2):
        times(x2, y)
        with pydwimmer.builtin.core.answer(A):
            return double(A) + y
    with pydwimmer.builtin.ints.zero():
        return 0
    with pydwimmer.builtin.ints.double(x2):
        times(x2, y)
        with pydwimmer.builtin.core.answer(A):
            return double(A)

@dwim
def quotient(x, y):
    """what is the quotient of [x] by [y], and what is the remainder?"""
    greater(y,x)
    with pydwimmer.builtin.core.answer(A):
        A
        with pydwimmer.builtin.bools.no():
            quotient(x, double(y))
            with pydwimmer.builtin.ints.quotient_and_remainder(q, r):
                if at_least(r, y):
                    raise quotient_and_remainder(double_inc(q), minus(r, y))
                else:
                    raise quotient_and_remainder(double(q), r)
        with pydwimmer.builtin.bools.yes():
            raise quotient_and_remainder(0, x)
    with pydwimmer.builtin.ints.first_larger():
        raise quotient_and_remainder(0, x)

@pydwimmer.compiler.dwim
def greater(x,y):
    """is [x] greater than [y]?"""
    x
    with pydwimmer.builtin.ints.double_inc(x2):
        y
        with pydwimmer.builtin.ints.double(x3):
            compare_within_one(x2,x3)
            with pydwimmer.builtin.ints.second_larger():
                return no()
            with pydwimmer.builtin.ints.second_one_larger():
                return no()
            with pydwimmer.builtin.ints.are_equal():
                return yes()
        with pydwimmer.builtin.ints.double_inc(x3):
            greater(x2, x3)
            with pydwimmer.builtin.core.answer(A):
                return A
        with pydwimmer.builtin.ints.zero():
            compare_within_one(x2, 0)
            with pydwimmer.builtin.ints.are_equal():
                return yes()
    with pydwimmer.builtin.ints.double(x2):
        y
        with pydwimmer.builtin.ints.double(x3):
            greater(x2, x3)
            with pydwimmer.builtin.core.answer(A):
                return A
        with pydwimmer.builtin.ints.double_inc(x3):
            compare_within_one(x2, x3)
            with pydwimmer.builtin.ints.first_one_larger():
                return yes()
            with pydwimmer.builtin.ints.first_larger():
                raise first_larger()
    with pydwimmer.builtin.ints.zero():
        y
        with pydwimmer.builtin.ints.zero():
            return no()


@pydwimmer.compiler.dwim
def compare_within_one(x,y):
    """are [x] and [y] within one of each other? if so, what is the difference, if not, which is larger?"""
    x
    with pydwimmer.builtin.ints.double_inc(x2):
        y
        with pydwimmer.builtin.ints.double(x3):
            compare_within_one(x2, x3)
            with pydwimmer.builtin.ints.second_larger():
                raise second_larger()
            with pydwimmer.builtin.ints.second_one_larger():
                raise second_one_larger()
            with pydwimmer.builtin.ints.are_equal():
                raise first_one_larger()
        with pydwimmer.builtin.ints.double_inc(x3):
            compare(x2,x3)
            with pydwimmer.builtin.ints.are_equal():
                raise are_equal()
            with pydwimmer.builtin.ints.first_larger():
                raise first_larger()
        with pydwimmer.builtin.ints.zero():
            compare_within_one(x2, 0)
            with pydwimmer.builtin.ints.are_equal():
                raise first_one_larger()
            with first_one_larger():
                raise first_one_larger()
            with first_larger():
                raise first_one_larger()
    with pydwimmer.builtin.ints.zero():
        y
        with pydwimmer.builtin.ints.double(x2):
            compare_within_one(0, x2)
            with pydwimmer.builtin.ints.second_one_larger():
                raise second_larger()
        with pydwimmer.builtin.ints.double_inc(x2):
            compare_within_one(0, x2)
            with pydwimmer.builtin.ints.are_equal():
                raise second_one_larger()
        with pydwimmer.builtin.ints.zero():
            raise are_equal()
    with pydwimmer.builtin.ints.double(x2):
        y
        with pydwimmer.builtin.ints.double_inc(x3):
            compare_within_one(x2, x3)
            with pydwimmer.builtin.ints.first_one_larger():
                raise first_one_larger()
        with zero():
            pydwimmer.builtin.ints.compare_within_one(x2, 0)
            with are_equal():
                raise pydwimmer.builtin.ints.are_equal()
            with first_one_larger():
                raise pydwimmer.builtin.ints.first_larger()
            with first_larger():
                raise first_larger()


@pydwimmer.terms.template
class are_equal:
    """they are equal"""


@pydwimmer.terms.template
class second_one_larger:
    """the second argument is one larger"""


@pydwimmer.terms.template
class second_larger:
    """the second argument is larger"""


@pydwimmer.compiler.dwim
def compare(x,y):
    """which of [x] and [y] is larger, or are they equal?"""
    x
    with pydwimmer.builtin.ints.zero():
        y
        with pydwimmer.builtin.ints.zero():
            raise are_equal()
    with pydwimmer.builtin.ints.double(x2):
        y
        with pydwimmer.builtin.ints.double_inc(x3):
            compare_within_one(x2, x3)
            with pydwimmer.builtin.ints.first_one_larger():
                raise first_larger()
    with pydwimmer.builtin.ints.double_inc(x2):
        y
        with pydwimmer.builtin.ints.double_inc(x3):
            compare(x2, x3)
            with pydwimmer.builtin.ints.first_larger():
                raise first_larger()
            with pydwimmer.builtin.ints.are_equal():
                raise are_equal()
        with pydwimmer.builtin.ints.zero():
            compare_within_one(x2, 0)
            with pydwimmer.builtin.ints.are_equal():
                raise first_larger()


@pydwimmer.terms.template
class quotient_and_remainder:
    """the quotient is [q] and the remainder is [r]"""


@pydwimmer.compiler.dwim
def at_least(x,y):
    """is [x] at least [y]?"""
    compare(x,y)
    with pydwimmer.builtin.ints.first_larger():
        return yes()
    with pydwimmer.builtin.ints.are_equal():
        return yes()


@pydwimmer.terms.template
class first_one_larger:
    """the first argument is one larger"""


@pydwimmer.terms.template
class first_larger:
    """the first argument is larger than the second"""

