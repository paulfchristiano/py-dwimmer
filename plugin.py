import main
import vim
from ipdb import set_trace as debug

def run_line():
    run(vim.current.line)

def run(s):
    eval(s, main.__dict__)
