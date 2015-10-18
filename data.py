import terms
from terms import Template as T

empty = T("the empty list")
cons = T("the list with first element {} and following elements in {}")


def list_to_term(xs):
    result = empty()
    for x in reversed(xs):
        result = cons(x, result)
    return result


empty_dict = T("the dictionary that doesn't map anything to anything")
dict_cons = T("the dictionary that maps {} to {} and other keys according to {}")

def dict_to_term(x):
    result = empty_dict()
    for k, v in x.items():
        result = dict_cons(k, v, empty_dict)
    return result


double = T("two times {}")
double_inc = T("two times {} plus one")
zero = T("the number zero")
negative = T("the additive inverse of {}")

def int_to_term(n):
    if n == 0:
        return zero()
    if n < 0:
        return negative(-n)
    if n % 2 == 0:
        return double(n / 2)
    if n % 2 == 1:
        return double_inc(n / 2)

yes = T("yes")
no = T("no")

def bool_to_term(b):
    return yes() if b else no()

string = T("the string with list of characters {}")

def string_to_term(s):
    return string([char_to_term(c) for c in s])


char = T("the character with ASCII code {}")

def char_to_term(c):
    return char(ord(c))


meta = terms.Template("what action should be taken in the setting with template {}?")
answer = terms.Template("the answer is {}")
