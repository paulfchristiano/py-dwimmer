import compiler
from builtins import *
from data import *
from ipdb import set_trace as debug

compiler.learn_from_all()

if __name__ == '__main__':
    A = reverse([0, 1, 2])
    debug()
