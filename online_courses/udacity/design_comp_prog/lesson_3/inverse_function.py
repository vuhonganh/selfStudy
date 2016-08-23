def slow_inverse(f, delta=1 / 128.):
    """Given a function y = f(x) that is a monotonically increasing function on
    non-negatve numbers, return the function x = f_1(y) that is an approximate
    inverse, picking the closest value to the inverse, within delta."""

    def f_1(y):
        x = 0
        while f(x) < y:
            x += delta
        # Now x is too big, x-delta is too small; pick the closest to y
        return x if (f(x) - y < y - f(x - delta)) else x - delta
    return f_1


def inverse(f, delta=1 / 128.):
    """Given a function y = f(x) that is a monotonically increasing function on
    non-negatve numbers, return the function x = f_1(y) that is an approximate
    inverse, picking the closest value to the inverse, within delta."""
    def f_1(y):
        # find upper bound x_upper that f(x_upper) > y:
        x_upper = 1.0
        x_lower = 0.0
        while f(x_upper) < y:
            x_upper *= 2
        if abs(f(x_upper) - y) < delta:
            return x_upper
        if abs(f(x_lower) - y) < delta:
            return x_lower

        # binary search
        x = (x_upper + x_lower) / 2.0
        while abs(f(x) - y) > delta:
            if f(x) < y:
                x_lower = x
            else:
                x_upper = x
            x = (x_upper + x_lower) / 2.0
        return x
    return f_1




def square(x): return x * x


# sqrt = slow_inverse(square)
sqrt = inverse(square)

print sqrt(1000000000)
print sqrt(0)
