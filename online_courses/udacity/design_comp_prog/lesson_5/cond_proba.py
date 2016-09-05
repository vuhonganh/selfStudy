"""Use computer to calculate some conditional probability"""

import itertools
from fractions import Fraction


# PROBLEM 1: calculate the probability of having 2 boys in a family having at least 1 boy and 2 children in total
sex = 'BG'
def product(*args):
    """Return the cartesian products of all arg from args"""
    return map(''.join, itertools.product(*args))

two_kids = product(sex, sex)
one_boy_over_two = [s for s in two_kids if 'B' in s]

def condP(predicate, event):
    """Conditional Probability: P (predicate(s) | s in event)
    i.e. the proportion of state s in event for which predicate is true"""
    pred = [s for s in event if predicate(s)]
    return Fraction(len(pred), len(event))

def two_boys(s):
    return s.count('B') == 2

print condP(two_boys, one_boy_over_two)

# PROBLEM 2: Out of all families with 2 kids with at least 1 boy born on Tuesday, what is the probability of having 2 boys?
days = 'SMTWtFs'
two_kids_days = product(sex, days, sex, days)
boy_tuesday = [s for s in two_kids_days if 'BT' in s]
print condP(two_boys, boy_tuesday)