"""
UNIT 3: Functions and APIs: Polynomials

A polynomial is a mathematical formula like:

    30 * x**2 + 20 * x + 10

More formally, it involves a single variable (here 'x'), and the sum of one
or more terms, where each term is a real number multiplied by the variable
raised to a non-negative integer power. (Remember that x**0 is 1 and x**1 is x,
so 'x' is short for '1 * x**1' and '10' is short for '10 * x**0'.)

We will represent a polynomial as a Python function which computes the formula
when applied to a numeric value x.  The function will be created with the call:

    p1 = poly((10, 20, 30))

where the nth element of the input tuple is the coefficient of the nth power of x.
(Note the order of coefficients has the x**n coefficient neatly in position n of
the list, but this is the reversed order from how we usually write polynomials.)
poly returns a function, so we can now apply p1 to some value of x:

    p1(0) == 10

Our representation of a polynomial is as a callable function, but in addition,
we will store the coefficients in the .coefs attribute of the function, so we have:

    p1.coefs == (10, 20, 30)

And finally, the name of the function will be the formula given above, so you should
have something like this:

    >>> p1
    <function 30 * x**2 + 20 * x + 10 at 0x100d71c08>

    >>> p1.__name__
    '30 * x**2 + 20 * x + 10'

Make sure the formula used for function names is simplified properly.
No '0 * x**n' terms; just drop these. Simplify '1 * x**n' to 'x**n'.
Simplify '5 * x**0' to '5'.  Similarly, simplify 'x**1' to 'x'.
For negative coefficients, like -5, you can use '... + -5 * ...' or
'... - 5 * ...'; your choice. I'd recommend no spaces around '**'
and spaces around '+' and '*', but you are free to use your preferences.

Your task is to write the function poly and the following additional functions:

    is_poly, add, sub, mul, power, deriv, integral

They are described below; see the test_poly function for examples.
"""
import operator


def poly(coefs):
    """Return a function that represents the polynomial with these coefficients.
    For example, if coefs=(10, 20, 30), return the function of x that computes
    '30 * x**2 + 20 * x + 10'.  Also store the coefs on the .coefs attribute of
    the function, and the str of the formula on the .__name__ attribute.'"""
    def f(x):
        res = 0
        for i in range(len(coefs) - 1, -1, -1):
            res += coefs[i] * (x ** i)

        return res

    f.__name__ = get_name(coefs)
    f.coefs = coefs
    return f


def get_name(coefs):
    func_name = ''
    for i in range(len(coefs) - 1, -1, -1):
        if coefs[i] != 0:
            if i == 0:
                func_name += str(coefs[i]) if func_name == '' else ' + ' + str(coefs[i])
            elif i == 1:
                if coefs[i] == 1:
                    func_name += 'x' if func_name == '' else ' + x'
                else:
                    func_name += str(coefs[i]) + ' * x' if func_name == '' else ' + ' + str(coefs[i]) + ' * x'
            else:
                if coefs[i] == 1:
                    func_name += 'x**' + str(i) if func_name == '' else ' + ' + 'x**' + str(i)
                else:
                    func_name += str(coefs[i]) + ' * x**' + str(i) if func_name == '' else ' + ' + str(coefs[i]) + ' * x**' + str(i)
    return func_name


def test_poly():
    global p1, p2, p3, p4, p5, p9  # global to ease debugging in an interactive session

    p1 = poly((10, 20, 30))
    assert p1(0) == 10
    for x in (1, 2, 3, 4, 5, 1234.5):
        assert p1(x) == 30 * x ** 2 + 20 * x + 10
    assert same_name(p1.__name__, '30 * x**2 + 20 * x + 10')

    assert is_poly(p1)
    assert not is_poly(abs) and not is_poly(42) and not is_poly('cracker')

    p3 = poly((0, 0, 0, 1))
    print p3.__name__
    assert p3.__name__ == 'x**3'
    p9 = mul(p3, mul(p3, p3))
    assert p9(2) == 512
    p4 = add(p1, p3)
    assert same_name(p4.__name__, 'x**3 + 30 * x**2 + 20 * x + 10')

    assert same_name(poly((1, 1)).__name__, 'x + 1')
    assert same_name(power(poly((1, 1)), 10).__name__,
                     'x**10 + 10 * x**9 + 45 * x**8 + 120 * x**7 + 210 * x**6 + 252 * x**5 + 210' +
                     ' * x**4 + 120 * x**3 + 45 * x**2 + 10 * x + 1')
    assert add(poly((10, 20, 30)), poly((1, 2, 3))).coefs == (11, 22, 33)
    assert sub(poly((10, 20, 30)), poly((1, 2, 3))).coefs == (9, 18, 27)
    assert mul(poly((10, 20, 30)), poly((1, 2, 3))).coefs == (10, 40, 100, 120, 90)
    assert power(poly((1, 1)), 2).coefs == (1, 2, 1)
    assert power(poly((1, 1)), 10).coefs == (1, 10, 45, 120, 210, 252, 210, 120, 45, 10, 1)

    assert deriv(p1).coefs == (20, 60)
    assert integral(poly((20, 60))).coefs == (0, 20, 30)
    p5 = poly((0, 1, 2, 3, 4, 5))
    assert same_name(p5.__name__, '5 * x**5 + 4 * x**4 + 3 * x**3 + 2 * x**2 + x')
    assert p5(1) == 15
    assert p5(2) == 258
    assert same_name(deriv(p5).__name__, '25 * x**4 + 16 * x**3 + 9 * x**2 + 4 * x + 1')
    assert deriv(p5)(1) == 55
    assert deriv(p5)(2) == 573
    # Additional Test Case:
    p6 = poly((1,))
    assert integral(p6)(10) == 10
    return 'test_poly passes'


def same_name(name1, name2):
    """I define this function rather than doing name1 == name2 to allow for some
    variation in naming conventions."""

    def canonical_name(name): return name.replace(' ', '').replace('+-', '-')

    return canonical_name(name1) == canonical_name(name2)


def is_poly(x):
    "Return true if x is a poly (polynomial)."
    return callable(x) and hasattr(x, 'coefs')


def add(p1, p2):
    "Return a new polynomial which is the sum of polynomials p1 and p2."
    coef1 = p1.coefs
    coef2 = p2.coefs
    max_len = max(len(coef1), len(coef2))
    res = [0] * max_len
    for (i, val) in enumerate(coef1):
        res[i] += val
    for (i, val) in enumerate(coef2):
        res[i] += val

    return poly(tuple(res))


def sub(p1, p2):
    "Return a new polynomial which is the difference of polynomials p1 and p2."
    zero = [0] * len(p2.coefs)
    minus_p2 = poly(tuple(map(operator.sub, zero, list(p2.coefs))))
    return add(p1, minus_p2)


def mul(p1, p2):
    "Return a new polynomial which is the product of polynomials p1 and p2."
    coefs1 = p1.coefs
    coefs2 = p2.coefs
    len1 = len(coefs1)
    len2 = len(coefs2)
    res = [0] * (len1 + len2 - 1)
    for (i1, val1) in enumerate(coefs1):
        for (i2, val2) in enumerate(coefs2):
            res[i1 + i2] += val1 * val2
    return poly(tuple(res))


def power(p, n):
    "Return a new polynomial which is p to the nth power (n a non-negative integer)."
    if n == 0:  # 0-th power is always 1
        return poly((1, 0))
    res = p
    for i in range(n - 1):
        res = mul(res, p)

    return res





"""
If your calculus is rusty (or non-existant), here is a refresher:
The deriviative of a polynomial term (c * x**n) is (c*n * x**(n-1)).
The derivative of a sum is the sum of the derivatives.
So the derivative of (30 * x**2 + 20 * x + 10) is (60 * x + 20).

The integral is the anti-derivative:
The integral of 60 * x + 20 is  30 * x**2 + 20 * x + C, for any constant C.
Any value of C is an equally good anti-derivative.  We allow C as an argument
to the function integral (withh default C=0).
"""


def deriv(p):
    "Return the derivative of a function p (with respect to its argument)."
    coefs = p.coefs
    lenres = len(coefs) - 1
    res = [0] * lenres
    for i in range(0, lenres):  # (c * x**n) --> (c*n x**(n-1))
        res[i] = coefs[i + 1] * (i + 1)
    return poly(tuple(res))


def integral(p, C=0):
    "Return the integral of a function p (with respect to its argument)."
    # (c * x**n) --> (c/(n+1) * x**(n+1))
    coefs = p.coefs
    lenp = len(coefs)
    lenres = lenp + 1
    res = [0] * lenres
    res[0] = C
    for i in range(0, lenp):
        res[i + 1] = coefs[i] / (1. * (i + 1))

    return poly(tuple(res))


# """
# Now for an extra credit challenge: arrange to describe polynomials with an
# expression like '3 * x**2 + 5 * x + 9' rather than (9, 5, 3).  You can do this
# in one (or both) of two ways:
#
# (1) By defining poly as a class rather than a function, and overloading the
# __add__, __sub__, __mul__, and __pow__ operators, etc.  If you choose this,
# call the function test_poly1().  Make sure that poly objects can still be called.
#
# (2) Using the grammar parsing techniques we learned in Unit 5. For this
# approach, define a new function, Poly, which takes one argument, a string,
# as in Poly('30 * x**2 + 20 * x + 10').  Call test_poly2().
# """
#
#
# def test_poly1():
#     # I define x as the polynomial 1*x + 0.
#     x = poly((0, 1))
#     # From here on I can create polynomials by + and * operations on x.
#     newp1 = 30 * x ** 2 + 20 * x + 10  # This is a poly object, not a number!
#     assert p1(100) == newp1(100)  # The new poly objects are still callable.
#     assert same_name(p1.__name__, newp1.__name__)
#     assert (x + 1) * (x - 1) == x ** 2 - 1 == poly((-1, 0, 1))
#
#
# def test_poly2():
#     newp1 = Poly('30 * x**2 + 20 * x + 10')
#     assert p1(100) == newp1(100)
#     assert same_name(p1.__name__, newp1.__name__)

print test_poly()

