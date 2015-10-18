import data
#TODO refactoring needed, to put data next to where it is used
from data import *
from compiler import dwim
from terms import template
from ipdb import set_trace as debug

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
    with double_inc(z):
        y
        with double(w):
            return double_inc(z+w)
        with double_inc(w):
            return double(inc(z+w))
        with zero():
            return x
    with zero():
        return y

@dwim
def inc(x):
    """what is one more than [x]?"""
    x + 1
    with answer(z):
        return z

@template
class probably:
    """the answer is probably {}"""

@dwim
def eq(x, y):
    """is [x] equal to [y]?"""
    x
    with double(z):
        y
        with double(w):
            return z == w
        with double_inc(w):
            raise probably(no())
        with zero():
            return z == 0
    with double_inc(z):
        y
        with double(w):
            raise probably(no())
        with double_inc(w):
            return z == w
        with zero():
            return probably(no())
    with zero():
        y
        with zero():
            return yes()
        with double(z):
            return z == 0
        with double_inc(z):
            raise probably(no())

@template
class concatenation:
    """the concatenation of {} and {}"""

@template
class singleton:
    """the list with only element {}"""

@dwim
def reverse(l):
    """what is the result of reversing [l]?"""
    l
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
