# DECORATOR:
"""
@func_1
func_2

equivalent to: func_2 = func_1(func_2)
"""

from functools import update_wrapper

# Rewrite decorator to avoid repeating update_wrapper in each decorator function
def decorator(d):
    "d a decorator: d wraps a function f. decorator of d will update automatically information from f to the new one"
    def _d(f):
        return update_wrapper(d(f), f) # update d(f) by the value of f which is previously done in each decorator function
    update_wrapper(_d, d) # update _d by value of d
    return _d

@decorator
def n_ary(f):
    """Given a binary function f(x, y), return an n_ary function such that
    n_ary_f(x, y, z) = f(x, f(y, z)), etc. Also alow f(x) = x"""
    def n_ary_f(x, *args):
        return x if not args else f(x, n_ary_f(*args))
    # update_wrapper(n_ary_f, f) --> this line is no longer needed
    return n_ary_f


@n_ary
def seq(x, y): return ('seq', x, y)   # only the first function below sign @n_ary will be affected

def seq2(x, y): return ('seq2', x, y) # this will not be affected by n_ary

a_func = seq('x1', 'y1')
print a_func

b_func = seq('x2', 'y2', 'z2')
print b_func

help(seq)

@decorator
def memo(f):
    """
    Decorator that caches the return value for each call to f(args)
    Then when called again with some args, we can just look it up
    """
    cache = {} # a dictionary

    def _f(*args):
        try:
            return cache[args]
        except KeyError: # not computed previously
            result = f(*args)
            cache[args] = result
            return result
        except TypeError: # the args has an unexpected type such as a list (mutable is not allowed)
            return f(*args)
    _f.cache = cache # WHY ???
    print("id in memo %s" %id(_f))
    return _f

@decorator
def countcalls(f):
    "Decorator that makes function count calls to it, in callcounts[f]"
    def _f(*args):
        callcounts[_f] += 1
        return f(*args)
    callcounts[_f] = 0
    print("id in countcalls %s" % id(_f))
    return _f

callcounts = {} # initialize callcounts to an empty dict


@countcalls
def fib(n):
    if n == 0 or n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

# countcalls must be followed by all other decorators because the order is reverse, i.e. it will be created at last
# this is important because the id of the object (function) changes each time a decorator is called
# so only the last one will be called and this must be initialized by countcalls previously
@countcalls
@memo
def fib_with_memo(n):
    if n == 0 or n == 1:
        return 1
    else:
        return fib_with_memo(n-1) + fib_with_memo(n-2)

print fib(20)
print callcounts[fib]

print fib_with_memo(20)
print callcounts[fib_with_memo]


@decorator
def trace(f):
    "tracer: '-->': make call to function, '<--': result found"
    indent = '    '
    def _f(*args):
        signature = '%s(%s)' % (f.__name__, ''.join(map(repr, args)))
        print '%s--> %s' %(trace.level * indent, signature)
        trace.level += 1
        try:
            # result found
            result = f(*args)
            print '%s<-- %s === %s' %((trace.level - 1) * indent, signature, result)
        finally:
            trace.level -= 1
        return result
    trace.level = 0 # initialize trace level
    return _f


def disable(f):
    return f

# The line below will disable decorator trace, the same for other decorators
# trace = disable

@trace
def fib_trace(n):
    if n == 0 or n == 1:
        return 1
    else:
        return fib_trace(n-1) + fib_trace(n-2)


print fib_trace(6)