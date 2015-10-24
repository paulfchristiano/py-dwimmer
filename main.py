def debug():
    import ipdb
    ipdb.set_trace()

from pydwimmer.builtin import *
from pydwimmer.builtin.ints import *
from pydwimmer.builtin.lists import *
from pydwimmer.builtin.dicts import *
from pydwimmer.builtin.bools import *
from pydwimmer.builtin.core import *
from pydwimmer.terms import to_term
import pydwimmer.compiler as compiler
import pydwimmer.builtin as builtin

compiler.learn_from_all()

if __name__ == '__main__':
    A = builtin.lists.reverse([0, 1, 2])
    print(A.full_repr())
