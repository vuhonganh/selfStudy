"""
Game called pig: 2 (or more) players roll the dice to accumulate their score to a goal.
They can hold or keep rolling (see each function's def.)
"""

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


# States are represented as a tuple of (p, me, you, pending) where
# p:       an int, 0 or 1, indicating which player's turn it is.
# me:      an int, the player-to-move's current score
# you:     an int, the other player's current score.
# pending: an int, the number of points accumulated on current turn, not yet scored
import random

goal = 50
possible_moves = ['roll', 'hold']
other = {1: 0, 0: 1}


def hold(state):
    """Apply the hold action to a state to yield a new state:
    Reap the 'pending' points and it becomes the other player's turn."""
    # once hold: turn changes and next player 's pending = 0
    return 1 - state[0], state[2], state[1] + state[3], 0


def roll(state, d):
    """Apply the roll action to a state (and a die roll d) to yield a new state:
    If d is 1, get 1 point (losing any accumulated 'pending' points),
    and it is the other player's turn. If d > 1, add d to 'pending' points."""
    if d == 1:
        return 1 - state[0], state[2], state[1] + 1, 0
    else:
        return state[0], state[1], state[2], state[3] + d


def hold_at(x):
    """Return a strategy that holds if and only if
    pending >= x or player reaches goal."""

    def strategy(state):
        (p, me, you, pending) = state
        if me + pending >= goal or pending >= x:
            return 'hold'
        return 'roll'

    strategy.__name__ = 'hold_at(%d)' % x
    return strategy


def clueless(state):
    "A strategy that ignores the state and chooses at random from possible moves."
    return random.choice(possible_moves)


def dice_rand():
    while True:
        yield random.randint(1, 6)


def play_pig(A, B, dice_rolls=dice_rand()):
    """Play a game of pig between two players, represented by their strategies (i.e. function)
    Each time through the main loop we ask the current player for one decision,
    which must be 'hold' or 'roll', and we update the state accordingly.
    When one player's score exceeds the goal, return that player."""
    cur_state = (0, 0, 0, 0)  # start state
    strategies = [A, B]
    while True:
        (p, me, you, pending) = cur_state
        if me >= goal:
            return strategies[p]
        elif you >= goal:
            return strategies[other[p]]
        elif strategies[p](cur_state) == 'hold':
            cur_state = hold(cur_state)
        elif strategies[p](cur_state) == 'roll':
            d = next(dice_rolls)
            cur_state = roll(cur_state, d)
        else:   # me doing an illegal action -> loses the game immediately
            return strategies[other[p]]


def always_roll(state):
    return 'roll'


def always_hold(state):
    return 'hold'


def Q_pig(state, action, utility_func):
    "The expected value of choosing action in state."
    if action == 'hold':    # if we hold, the quality is 1 - the chance to win of the opponent in the next state
        return 1 - utility_func(hold(state))
    if action == 'roll':    # if we rold, the quality is 1 - the chance to win of the opponent if dice is 1, otherwise
        # it's the chance for us to win with dice from 2 to 6. Overall, we need to take the average cause dice is fair
        return (1 - utility_func(roll(state, 1))
                + sum(utility_func(roll(state, d)) for d in (2, 3, 4, 5, 6))) / 6.
    raise ValueError


def best_action(state, actions, Q, U):
    """Return the optimal action for a state, given U."""

    def EU(action): return Q(state, action, U)  # EU = expected utility
    print 'max(actions(state)) = %s' %(max(actions(state), key=EU))
    return max(actions(state), key=EU)


def pig_actions(state):
    """The legal actions from a state."""
    _, _, _, pending = state
    return ['roll', 'hold'] if pending else ['roll']


@memo
def Pwin_utility(state):    # Probability of Winning
    """The utility of a state; here just the probability that an optimal player
    whose turn it is to move can win from the current state."""
    # Assumes opponent also plays with optimal strategy.
    (p, me, you, pending) = state
    if me + pending >= goal:
        return 1
    elif you >= goal:
        return 0
    else:
        return max(Q_pig(state, action, Pwin_utility)
                   for action in pig_actions(state))


def max_wins(state):
    """The optimal pig strategy chooses an action with the highest win probability."""
    return best_action(state, pig_actions, Q_pig, Pwin_utility)


@memo
def win_diff_utility(state):
    "The utility of a state: here the winning differential (pos or neg)."
    (p, me, you, pending) = state
    if me + pending >= goal or you >= goal:
        return me + pending - you
    else:
        return max(Q_pig(state, action, win_diff_utility)
                   for action in pig_actions(state))


def max_diffs(state):
    """A strategy that maximizes the expected difference between my final score
    and my opponent's."""
    return best_action(state, pig_actions, Q_pig, win_diff_utility)


def bad_strategy(state):
    "A strategy that could never win, unless a player makes an illegal move"
    return 'hold'


def illegal_strategy(state):
    return 'I want to win pig please.'


def Pwin_utility_ver2(state):
    """The utility of a state that a player having turn can make to obtain optimal utility"""
    _, me, you, pending = state
    return Pwin_utility_ver3(me, you, pending)


@memo
def Pwin_utility_ver3(me, you, pending):
    """Return the probability of winning"""
    if me + pending >= goal:
        return 1
    elif you >= goal:
        return 0
    else:
        Proll = (1 - Pwin_utility_ver3(you, me + 1, 0) +
                 sum(Pwin_utility_ver3(me, you, pending + d) for d in range(2, 7))) / 6.0
        if not pending:  # pending = 0 -> need to roll
            return Proll
        else:
            return max(Proll, 1 - Pwin_utility_ver3(you, me + pending, 0))


def test():
    assert hold((1, 10, 20, 7)) == (0, 20, 17, 0)
    assert hold((0, 5, 15, 10)) == (1, 15, 15, 0)
    assert roll((1, 10, 20, 7), 1) == (0, 20, 11, 0)
    assert roll((0, 5, 15, 10), 5) == (0, 5, 15, 15)
    assert hold_at(30)((1, 29, 15, 20)) == 'roll'
    assert hold_at(30)((1, 29, 15, 21)) == 'hold'
    assert hold_at(15)((0, 2, 30, 10)) == 'roll'
    assert hold_at(15)((0, 2, 30, 15)) == 'hold'

    A, B = hold_at(50), clueless
    rolls = iter([6, 6, 6, 6, 6, 6, 6, 6, 2])
    assert play_pig(A, B, rolls) == A

    # change to 40 for the following tests
    global goal
    goal = 40

    assert (max_wins((1, 18, 27, 8))) == "roll"
    assert (max_wins((0, 23, 8, 8))) == "roll"
    assert (max_wins((0, 31, 22, 9))) == "hold"
    assert (max_wins((1, 11, 13, 21))) == "roll"
    assert (max_wins((1, 33, 16, 6))) == "roll"
    assert (max_wins((1, 12, 17, 27))) == "roll"
    assert (max_wins((1, 9, 32, 5))) == "roll"
    assert (max_wins((0, 28, 27, 5))) == "roll"
    assert (max_wins((1, 7, 26, 34))) == "hold"
    assert (max_wins((1, 20, 29, 17))) == "roll"
    assert (max_wins((0, 34, 23, 7))) == "hold"
    assert (max_wins((0, 30, 23, 11))) == "hold"
    assert (max_wins((0, 22, 36, 6))) == "roll"
    assert (max_wins((0, 21, 38, 12))) == "roll"
    assert (max_wins((0, 1, 13, 21))) == "roll"
    assert (max_wins((0, 11, 25, 14))) == "roll"
    assert (max_wins((0, 22, 4, 7))) == "roll"
    assert (max_wins((1, 28, 3, 2))) == "roll"
    assert (max_wins((0, 11, 0, 24))) == "roll"
    assert (max_wins((1, 5, 34, 4))) == "roll"

    # The first three test cases are examples where max_wins and
    # max_diffs return the same action.
    assert(max_diffs((1, 26, 21, 15))) == "hold"
    assert(max_diffs((1, 23, 36, 7)))  == "roll"
    assert(max_diffs((0, 29, 4, 3)))   == "roll"
    # The remaining test cases are examples where max_wins and
    # max_diffs return different actions.
    assert(max_diffs((0, 36, 32, 5)))  == "roll"
    assert(max_diffs((1, 37, 16, 3)))  == "roll"
    assert(max_diffs((1, 33, 39, 7)))  == "roll"
    assert(max_diffs((0, 7, 9, 18)))   == "hold"
    assert(max_diffs((1, 0, 35, 35)))  == "hold"
    assert(max_diffs((0, 36, 7, 4)))   == "roll"
    assert(max_diffs((1, 5, 12, 21)))  == "hold"
    assert(max_diffs((0, 3, 13, 27)))  == "hold"
    assert(max_diffs((0, 0, 39, 37)))  == "hold"
    winner = play_pig(bad_strategy, illegal_strategy)
    assert winner.__name__ == 'bad_strategy'
    epsilon = 0.0001  # used to make sure that floating point errors don't cause test() to fail
    assert goal == 40
    assert len(Pwin_utility_ver3.cache) <= 50000
    assert Pwin_utility_ver2((0, 42, 25, 0)) == 1
    assert Pwin_utility_ver2((1, 12, 43, 0)) == 0
    assert Pwin_utility_ver2((0, 34, 42, 1)) == 0
    print Pwin_utility_ver2((0, 25, 32, 8))
    assert abs(Pwin_utility_ver2((0, 25, 32, 8)) - 0.736357188272) <= epsilon
    assert abs(Pwin_utility_ver2((0, 19, 35, 4)) - 0.493173612834) <= epsilon
    print len(Pwin_utility.cache)
    print len(Pwin_utility_ver3.cache)
    return 'tests pass'

print test()