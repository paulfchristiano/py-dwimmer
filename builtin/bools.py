from pydwimmer.terms import template
from pydwimmer.compiler import dwim

@template
class yes:
    """yes"""
@template
class no:
    """no"""

def to_term(b):
    if type(b) is not bool:
        raise ValueError("cannot convert non-bool")
    return yes() if b else no()

@dwim
def both(a, b):
    """are [a] and [b] both affirmative?"""
    if a:
        return b
    else:
        return no()

@dwim
def either(a, b):
    """is one of [a] and [b] affirmative?"""
    if a:
        return yes()
    else:
        return no()

@dwim
def eq(a, b):
    """is [a] equal to [b]?"""
    a
    with yes():
        b
        with yes():
            return yes()
        with no():
            return no()
    with no():
        b
        with yes():
            return no()
        with no():
            return yes()
