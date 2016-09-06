# -----------------
# User Instructions
#
# This problem deals with the one-player game foxes_and_hens. This
# game is played with a deck of cards in which each card is labelled
# as a hen 'H', or a fox 'F'.
#
# A player will flip over a random card. If that card is a hen, it is
# added to the yard. If it is a fox, all of the hens currently in the
# yard are removed.
#
# Before drawing a card, the player has the choice of two actions,
# 'gather' or 'wait'. If the player gathers, she collects all the hens
# in the yard and adds them to her score. The drawn card is discarded.
# If the player waits, she sees the next card.
#
# Your job is to define two functions. The first is do(action, state),
# where action is either 'gather' or 'wait' and state is a tuple of
# (score, yard, cards). This function should return a new state with
# one less card and the yard and score properly updated.
#
# The second function you define, strategy(state), should return an
# action based on the state. This strategy should average at least
# 1.5 more points than the take5 strategy.

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


def foxes_and_hens(strategy, foxes=7, hens=45):
    """Play the game of foxes and hens."""
    # A state is a tuple of (score-so-far, number-of-hens-in-yard, deck-of-cards)
    state = (score, yard, cards) = (0, 0, 'F' * foxes + 'H' * hens)
    while cards:
        action = strategy(state)
        state = (score, yard, cards) = do(action, state)
    return score + yard


def do(action, state):
    "Apply action to state, returning a new state."
    # Make sure you always use up one card.
    score, yard, cards = state
    nb_foxes = cards.count('F')
    nb_hens = cards.count('H')
    if nb_foxes <= 0 and nb_hens <= 0:
        print 'No card left to draw'
        raise ValueError
    random_pick = random.randint(1, nb_foxes + nb_hens)
    hen_is_drawn = random_pick > nb_foxes

    if action == 'gather':
        if hen_is_drawn:
            return (score + yard, 0, 'F' * nb_foxes + 'H' * (nb_hens - 1))
        else:
            return (score + yard, 0, 'F' * (nb_foxes - 1) + 'H' * nb_hens)
    elif action == 'wait':
        if hen_is_drawn:
            return (score, yard + 1, 'F' * nb_foxes + 'H' * (nb_hens - 1))
        else:
            return (score, 0, 'F' * (nb_foxes - 1) + 'H' * nb_hens)


def take5(state):
    "A strategy that waits until there are 5 hens in yard, then gathers."
    (score, yard, cards) = state
    if yard < 5:
        return 'wait'
    else:
        return 'gather'


def average_score(strategy, N=1000):
    return sum(foxes_and_hens(strategy) for _ in range(N)) / float(N)


def superior(A, B=take5):
    """Does strategy A have a higher average score than B, by more than 1.5 point?"""
    print 'average_score(my_strategy) = %f' %average_score(A)
    print 'average_score(take5_strategy) = %f' % average_score(B)
    return average_score(A) - average_score(B) > 1.5


def strategy(state):
    (score, yard, cards) = state
    return best_score(yard, cards)[1]


@memo
def best_score(yard, cards):
    """Given a reduced state (yard, cards) return the best score can achieve from this state"""
    nb_foxes = cards.count('F')
    nb_hens = cards.count('H')
    # base cases
    if nb_foxes == 0:
        return (yard + nb_hens, 'wait')
    if nb_hens == 0:
        return (yard, 'gather')
    prob_draw_fox = nb_foxes * 1.0 / (nb_hens + nb_foxes)
    cards_foxes_drawn = 'F' * (nb_foxes - 1) + 'H' * nb_hens
    cards_hens_drawn = 'F' * nb_foxes + 'H' * (nb_hens - 1)
    score_gather = yard + prob_draw_fox * best_score(0, cards_foxes_drawn)[0] + \
                        (1 - prob_draw_fox) * best_score(0, cards_hens_drawn)[0]
    score_wait = prob_draw_fox * best_score(0, cards_foxes_drawn)[0] + \
                 (1 - prob_draw_fox) * best_score(yard + 1, cards_hens_drawn)[0]
    if score_gather > score_wait:
        return (score_gather, 'gather')
    else:
        return (score_wait, 'wait')


def test():
    gather = do('gather', (4, 5, 'F' * 4 + 'H' * 10))
    assert (gather == (9, 0, 'F' * 3 + 'H' * 10) or
            gather == (9, 0, 'F' * 4 + 'H' * 9))

    wait = do('wait', (10, 3, 'FFHH'))
    assert (wait == (10, 4, 'FFH') or
            wait == (10, 0, 'FHH'))

    assert superior(strategy)
    return 'tests pass'


print test()


