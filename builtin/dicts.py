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
        result = dict_cons(k, v, result)
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
