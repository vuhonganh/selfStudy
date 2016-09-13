# -----------------
# User Instructions
#
# In this problem, we introduce doubling to the game of pig.
# At any point in the game, a player (let's say player A) can
# offer to 'double' the game. Player B then has to decide to
# 'accept', in which case the game is played through as normal,
# but it is now worth two points, or 'decline,' in which case
# player B immediately loses and player A wins one point.
#
# Your job is to write two functions. The first, pig_actions_d,
# takes a state (p, me, you, pending, double), as input and
# returns all of the legal actions.
#
# The second, strategy_d, is a strategy function which takes a
# state as input and returns one of the possible actions. This
# strategy needs to beat hold_20_d in order for you to be
# marked correct. Happy pigging!

import random
from functools import update_wrapper


def decorator(d):
    "Make function d a decorator: d wraps a function fn."

    def _d(fn):
        return update_wrapper(d(fn), fn)

    update_wrapper(_d, d)
    return _d


@decorator
def memo(f):
    """Decorator that caches the return value for each call to f(args).
    Then when called again with same args, we can just look it up."""
    cache = {}

    def _f(*args):
        try:
            return cache[args]
        except KeyError:
            cache[args] = result = f(*args)
            return result
        except TypeError:
            # some element of args can't be a dict key
            return f(args)

    _f.cache = cache
    return _f


def pig_actions_d(state):
    """The legal actions from a state. Usually, ["roll", "hold"].
    Exceptions: If double is "double", can only "accept" or "decline".
    Can't "hold" if pending is 0.
    If double is 1, can "double" (in addition to other moves).
    (If double > 1, cannot "double").
    """
    # state is like before, but with one more component, double,
    # which is 1 or 2 to denote the value of the game, or 'double'
    # for the moment at which one player has doubled and is waiting
    # for the other to accept or decline
    (p, me, you, pending, double) = state
    if double == "double":
        return ["accept", "decline"]
    elif double == 1:
        return ["roll", "hold", "double"] if pending else ["roll", "double"]
    elif double == 2:
        return ["roll", "hold"] if pending else ["roll"]
    else:
        raise ValueError


threshold = 0.8  # probability of winning needs to be bigger than this value to call 'double'


def strategy_d(state):
    """Given a state, need to return an action i.e. 'roll' or 'hold' or 'double' """
    (_, me, you, pending, double) = state
    if double == 'double':
        return 'accept'
    if pending == 0:    # avoid illegal move
        return 'roll'
    # Now need to consider among: 'roll', 'hold' and 'double'
    # the strategy is: only double if the probability of winning from this state is high (bigger then a threshold)
    proba_win, move_is_hold = p_win_utility(me, you, pending)
    if proba_win > threshold and double != 2:
        return 'double'
    if move_is_hold:
        return 'hold'
    else:
        return 'roll'


@memo
def p_win_utility(me, you, pending):
    """Input: reduced state
    Output: max probability of winning from this state and boolean move_is_hold"""
    if me + pending >= goal:
        return (1, True)
    elif you >= goal:
        return (0, False)
    else:
        # probability of winning if roll from this state
        p_roll = (1 - p_win_utility(you, me + 1, 0)[0] + sum(p_win_utility(me, you, pending + d)[0] for d in range(2, 7))) / 6.
        if pending == 0:
            return (p_roll, False)
        # probability of winning if hold from this state
        p_hold = 1 - p_win_utility(you, me + pending, 0)[0]
        return (p_roll, False) if p_roll > p_hold else (p_hold, True)


def hold_20_d(state):
    "Hold at 20 pending.  Always accept; never double."
    (p, me, you, pending, double) = state
    return ('accept' if double == 'double' else
            'hold' if (pending >= 20 or me + pending >= goal) else
            'roll')


def clueless_d(state):
    return random.choice(pig_actions_d(state))


def dicerolls():
    """Generate die rolls."""
    while True:
        yield random.randint(1, 6)


def play_pig_d(A, B, dicerolls=dicerolls()):
    """Play a game of pig between two players, represented by their strategies.
    Each time through the main loop we ask the current player for one decision,
    which must be 'hold' or 'roll', and we update the state accordingly.
    When one player's score exceeds the goal, return that player."""
    strategies = [A, B]
    state = (0, 0, 0, 0, 1)
    while True:
        (p, me, you, pending, double) = state
        if me >= goal:
            return strategies[p], double
        elif you >= goal:
            return strategies[other[p]], double
        else:
            action = strategies[p](state)
            state = do(action, state, dicerolls)


## No more roll() and hold(); instead, do:

def do(action, state, dicerolls):
    """Return the state that results from doing action in state.
    Can use dicerolls if needed."""
    (p, me, you, pending, double) = state

    if action not in pig_actions_d(state):  # If action is not legal, return a state where the opponent wins.
        return (other[p], goal, 0, 0, double)
    elif action == 'roll':
        d = next(dicerolls)
        if d == 1:
            return (other[p], you, me + 1, 0, double)  # pig out; other player's turn
        else:
            return (p, me, you, pending + d, double)  # accumulate dice in pending
    elif action == 'hold':
        return (other[p], you, me + pending, 0, double)
    elif action == 'double':
        return (other[p], you, me, pending, 'double')
    elif action == 'decline':
        return (other[p], goal, 0, 0, 1)
    elif action == 'accept':
        return (other[p], you, me, pending, 2)


goal = 40
other = {1: 0, 0: 1}


def strategy_compare(A, B, N=1000):
    """Takes two strategies, A and B, as input and returns the percentage
    of points won by strategy A."""
    A_points, B_points = 0, 0
    for i in range(N):
        if i % 2 == 0:  # take turns with who goes first
            winner, points = play_pig_d(A, B)
        else:
            winner, points = play_pig_d(B, A)
        if winner.__name__ == A.__name__:
            A_points += points
        else:
            B_points += points
    A_percent = 100 * A_points / float(A_points + B_points)
    print 'In %s games of pig, strategy %s took %s percent of the points against %s.' % (
    N, A.__name__, A_percent, B.__name__)
    return A_percent


def test():
    assert set(pig_actions_d((0, 2, 3, 0, 1))) == set(['roll', 'double'])
    assert set(pig_actions_d((1, 20, 30, 5, 2))) == set(['hold', 'roll'])
    assert set(pig_actions_d((0, 5, 5, 5, 1))) == set(['roll', 'hold', 'double'])
    assert set(pig_actions_d((1, 10, 15, 6, 'double'))) == set(['accept', 'decline'])
    print strategy_compare(strategy_d, hold_20_d)
    # assert strategy_compare(strategy_d, hold_20_d) > 60  # must win 60% of the points
    return 'test passes'


print test()



