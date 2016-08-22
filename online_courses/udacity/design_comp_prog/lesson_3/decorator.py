# DECORATOR functions

def n_ary(f):
    """Given a binary function f(x, y), return an n_ary function such that
    n_ary_f(x, y, z) = f(x, f(y, z)), etc. Also alow f(x) = x"""
    def n_ary_f(x, *args):
        return x if not args else f(x, n_ary_f(*args))
    return n_ary_f

#decorator

@n_ary
def seq(x, y): return ('seq', x, y)   # only the first function below sign @n_ary will be affected
def seq2(x, y): return ('seq2', x, y) # this will not be affected by n_ary

a_func = seq('x1', 'y1')
print a_func

b_func = seq('x2', 'y2', 'z2')
print b_func
