import pydwimmer.builtin.bools
import pydwimmer.builtin.core
import pydwimmer.builtin.ints
import pydwimmer.builtin.dicts
import pydwimmer.compiler
import pydwimmer.terms
terms = pydwimmer.terms
from pydwimmer.terms import template
from pydwimmer.compiler import dwim
from pydwimmer.builtin import core

@template
class empty_dict:
    "the dictionary that doesn't map anything to anything"

@template
class dict_cons:
    "the dictionary that maps [k] to [v] and other keys according to [other]"

def to_term(x):
    result = empty_dict()
    for k, v in x.items():
        A = insert(result, k, v)
        if isinstance(A, terms.CompoundTerm):
            if A.head == result_is:
                result = A.args[0]
                continue
        elif A is None:
            return None
        raise ValueError("not sure what to do with return value {}".format(A))
    return result

@template
class no_image:
    """that key is not mapped by that dictionary"""

@dwim
def lookup(key, d):
    """what is the image of [key] in the dictionary [d]?"""
    d
    with empty_dict():
        raise no_image()
    with dict_cons(k, v, other):
        if core.eq(k, key):
            return key
        else:
            lookup(key, other)
            with core.answer(z):
                return z
            with no_image():
                raise no_image()
    with by_parity(evens, odds):
        parity(key)
        with odd_and_half_is(x):
            lookup(x, odds)
            with pydwimmer.builtin.core.answer(A):
                return A
        with even_and_half_is(x):
            pydwimmer.builtin.dicts.lookup(x, evens)
            with no_image():
                raise pydwimmer.builtin.dicts.no_image()
    with dict_only(k, v):
        core.eq(k, key)
        with pydwimmer.builtin.core.answer(A):
            A
            with pydwimmer.builtin.bools.yes():
                return v

@pydwimmer.compiler.dwim
def insert(dict,k,v):
    """what is the dictionary obtained by updating [dict] so that [k] is mapped to [v]?"""
    dict
    with pydwimmer.builtin.dicts.empty_dict():
        raise result_is(dict_only(k, v))
    with pydwimmer.builtin.dicts.dict_only(k2, v2):
        types(k, k2)
        with pydwimmer.builtin.dicts.both_probably_type(t):
            new_dict(t)
            with pydwimmer.builtin.core.answer(A):
                insert(A, k2, v2)
                with pydwimmer.builtin.dicts.result_is(out):
                    insert(out, k, v)
                    with pydwimmer.builtin.dicts.result_is(out2):
                        raise result_is(out2)
    with pydwimmer.builtin.dicts.by_parity(evens, odds):
        k
        with pydwimmer.builtin.ints.double_inc(x):
            insert(odds, x, v)
            with pydwimmer.builtin.dicts.result_is(out):
                raise result_is(by_parity(evens, out))
        with pydwimmer.builtin.ints.zero():
            insert(evens, 0, v)
            with pydwimmer.builtin.dicts.result_is(out):
                raise result_is(by_parity(out, odds))
        with pydwimmer.builtin.ints.double(x):
            insert(evens, x, v)
            with result_is(out):
                raise result_is(by_parity(out, odds))
            

@pydwimmer.terms.template
class dict_only:
    """the dictionary that maps [k] to [v]"""


@pydwimmer.terms.template
class result_is:
    """the result is [out]"""


@pydwimmer.compiler.dwim
def new_dict(k,v):
    """what is the dictionary that maps [k] to [v]?"""


@pydwimmer.terms.template
class by_parity:
    """the dictionary that maps even integers to the image of half of them in [evens] and maps odd integers to the image of the floor of half of them in [odds]"""


@pydwimmer.compiler.dwim
def dict_both(k,v,k2,v2):
    """what is a dictionary that maps [k] to [v] and [k2] to [v2]?"""
    insert(dict_only(k, v), k2, v2)


@pydwimmer.compiler.dwim
def types(a,b):
    """what are the types of [a] and [b]?"""
    type(a)
    with pydwimmer.builtin.core.probably(A):
        type(b)
        with pydwimmer.builtin.core.probably(A2):
            core.eq(A, A2)
            with pydwimmer.builtin.core.answer(A3):
                A3
                with pydwimmer.builtin.bools.yes():
                    raise both_probably_type(A2)
        with pydwimmer.builtin.core.answer(A2):
            core.eq(A, A2)
            with pydwimmer.builtin.core.answer(A3):
                A3
                with pydwimmer.builtin.bools.yes():
                    raise both_probably_type(A2)
    with pydwimmer.builtin.core.answer(A):
        type(b)
        with pydwimmer.builtin.core.probably(A2):
            core.eq(A, A2)
            with pydwimmer.builtin.core.answer(A3):
                A3
                with pydwimmer.builtin.bools.yes():
                    raise both_probably_type(A2)
        with pydwimmer.builtin.core.answer(A2):
            core.eq(A, A2)
            with pydwimmer.builtin.core.answer(A3):
                A3
                with pydwimmer.builtin.bools.yes():
                    raise both_probably_type(A2)


@pydwimmer.compiler.dwim
def type(a):
    """what is the type of [a]?"""
    a
    with pydwimmer.builtin.ints.double_inc(x):
        raise core.probably(int_type())
    with pydwimmer.builtin.ints.zero():
        return int_type()
    with pydwimmer.builtin.ints.double(x):
        raise core.probably(int_type())
        

@pydwimmer.terms.template
class int_type:
    """the type of integers"""


@pydwimmer.terms.template
class both_probably_type:
    """both are probably of type [t]"""


@pydwimmer.compiler.dwim
def new_dict(t):
    """what is an empty dictionary in a representation suitable for mapping items of type [t]?"""
    t
    with pydwimmer.builtin.dicts.int_type():
        return by_parity(empty_dict(), empty_dict())


@pydwimmer.compiler.dwim
def parity(x):
    """is [x] even or odd, and what is the floor of half of it?"""
    x
    with pydwimmer.builtin.ints.double_inc(xx):
        raise odd_and_half_is(xx)
    with pydwimmer.builtin.ints.double(xx):
        raise even_and_half_is(xx)

@pydwimmer.terms.template
class odd_and_half_is:
    """it is odd, and the floor of half of it is [x]"""


@pydwimmer.terms.template
class even_and_half_is:
    """it is even, and half of it is [x]"""

