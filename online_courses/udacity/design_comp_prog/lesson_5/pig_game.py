"""
Game called pig: 2 (or more) players roll the dice to accumulate their score to a goal.
They can hold or keep rolling (see each function's def.)
"""

# States are represented as a tuple of (p, me, you, pending) where
# p:       an int, 0 or 1, indicating which player's turn it is.
# me:      an int, the player-to-move's current score
# you:     an int, the other player's current score.
# pending: an int, the number of points accumulated on current turn, not yet scored
import random
goal = 50
possible_moves = ['roll', 'hold']


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


def play_pig(A, B):
    """Play a game of pig between two players, represented by their strategies (i.e. function)
    Each time through the main loop we ask the current player for one decision,
    which must be 'hold' or 'roll', and we update the state accordingly.
    When one player's score exceeds the goal, return that player."""
    cur_state = (0, 0, 0, 0)  # start state
    while True:
        if cur_state[1] >= goal:
            return A
        elif cur_state[2] >= goal:
            return B
        this_move = A(cur_state) if cur_state[0] == 0 else B(cur_state)
        if this_move == 'hold':
            cur_state = hold(cur_state)
        else:
            d = random.randint(1, 6)
            cur_state = roll(cur_state, d)


def always_roll(state):
    return 'roll'


def always_hold(state):
    return 'hold'


def test():
    assert hold((1, 10, 20, 7)) == (0, 20, 17, 0)
    assert hold((0, 5, 15, 10)) == (1, 15, 15, 0)
    assert roll((1, 10, 20, 7), 1) == (0, 20, 11, 0)
    assert roll((0, 5, 15, 10), 5) == (0, 5, 15, 15)
    assert hold_at(30)((1, 29, 15, 20)) == 'roll'
    assert hold_at(30)((1, 29, 15, 21)) == 'hold'
    assert hold_at(15)((0, 2, 30, 10)) == 'roll'
    assert hold_at(15)((0, 2, 30, 15)) == 'hold'
    for _ in range(10):
        winner = play_pig(always_hold, always_roll)
        assert winner.__name__ == 'always_roll'

    return 'tests pass'


print test()

def generator_simple():
    yield 1
    yield 2
    yield 3

def test_pass_gen(a_generator_simple):
    ora = a_generator_simple
    print next(ora)
    print next(ora)
    print next(ora)

test_pass_gen(generator_simple())