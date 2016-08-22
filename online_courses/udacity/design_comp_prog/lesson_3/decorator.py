# DECORATOR:
"""
@func_1
func_2

equivalent to: func_2 = func_1(func_2)
"""

from functools import update_wrapper

def n_ary(f):
    """Given a binary function f(x, y), return an n_ary function such that
    n_ary_f(x, y, z) = f(x, f(y, z)), etc. Also alow f(x) = x"""
    def n_ary_f(x, *args):
        return x if not args else f(x, n_ary_f(*args))
    update_wrapper(n_ary_f, f)
    return n_ary_f


@n_ary
def seq(x, y): return ('seq', x, y)   # only the first function below sign @n_ary will be affected

def seq2(x, y): return ('seq2', x, y) # this will not be affected by n_ary

a_func = seq('x1', 'y1')
print a_func

b_func = seq('x2', 'y2', 'z2')
print b_func

help(seq)