"""
Statement:
A group of people attempt to crossing a bridge from left side to the right side at night.
There is only one lamp and they need the lamp to cross the bridge.
The maximum of people on the bridge is 2. Every one need a different time to cross the bridge.
Find the minimum time for them to all cross the bridge.

Solution:
People can be represented by their (distinct) time needed to cross the bridge

A state can be presented by: (left, right, t)
where left, right are frozenset (to be hashable) of format {people, light}
t is elapsed time

An action is a tuple (person1, person2, arrow), where arrow is
'->' for left to right or '<-' for right to left. When only one
person crosses, person2 will be the same as person1, so the
action (2, 2, '->') means that the person with a travel time of
2 crossed from left to right alone.
"""


def bsuccessors(state):
    """
    :param state: the current state
    :return: a dict of {state:action} indicating all possible states that can be reached
    """
    left, right, t = state
    # only the side having the lamp can go to the other side:
    res_dict = {}
    if 'light' in left:
        for a in left:
            if a is not 'light':
                for b in left:
                    if b is not 'light':
                        next_state = (left - frozenset({a, b, 'light'}),
                                      right | frozenset({a, b, 'light'}),
                                      t + max(a, b))
                        res_dict[next_state] = (a, b, '->')
    else:
        for a in right:
            if a is not 'light':
                for b in right:
                    if b is not 'light':
                        next_state = (left | frozenset({a, b, 'light'}),
                                      right - frozenset({a, b, 'light'}),
                                      t + max(a, b))
                        res_dict[next_state] = (a, b, '<-')
    return res_dict


# a path is a list of [state, action, state, action, ... ]
# path_states should return a list of the states in a path, and
# path_actions should return a list of the actions.

def path_states(path):
    """Return a list of states in this path."""
    # return [path[k] for k in range(len(path)) if not k % 2] # long version, inefficient
    return path[0::2]


def path_actions(path):
    """Return a list of actions in this path."""
    # return [path[k] for k in range(len(path)) if k % 2] # long version, inefficient
    return path[1::2]


def elapsed_time(path):
    """Return the elapsed time of a given path"""
    # This should be the time of last element in a path
    # Note that the last element in a path is always a state
    if not path:
        return 0
    return path[-1][2]


def bridge_problem(left):
    left = frozenset(left) | frozenset({'light'})
    explored = set()    # set of explored state
    # original state (at t = 0) is: all people are in the left
    original_state = (left, frozenset(), 0)
    # at the beginning there is only one path containing original state
    frontier = [ [original_state] ]  # frontier is an ordered list of path
    explored.add(original_state)
    while frontier:
        cur_path = frontier.pop(0)
        cur_state = cur_path[-1]
        if not cur_state[0]:    # all people are not in the left
            return cur_path
        else:
            for (next_state, action) in bsuccessors(cur_state).items():
                if next_state not in explored:
                    explored.add(next_state)
                    next_path = cur_path + [action, next_state]
                    frontier.append(next_path)
            frontier.sort(key=elapsed_time)
    # print 'no sol'
    return []


def test_paths():
    testpath = [(frozenset([1, 10]), frozenset(['light', 2, 5]), 5), # state 1
                (5, 2, '->'),                                        # action 1
                (frozenset([10, 5]), frozenset([1, 2, 'light']), 2), # state 2
                (2, 1, '->'),                                        # action 2
                (frozenset([1, 2, 10]), frozenset(['light', 5]), 5),
                (5, 5, '->'),
                (frozenset([1, 2]), frozenset(['light', 10, 5]), 10),
                (5, 10, '->'),
                (frozenset([1, 10, 5]), frozenset(['light', 2]), 2),
                (2, 2, '->'),
                (frozenset([2, 5]), frozenset([1, 10, 'light']), 10),
                (10, 1, '->'),
                (frozenset([1, 2, 5]), frozenset(['light', 10]), 10),
                (10, 10, '->'),
                (frozenset([1, 5]), frozenset(['light', 2, 10]), 10),
                (10, 2, '->'),
                (frozenset([2, 10]), frozenset([1, 5, 'light']), 5),
                (5, 1, '->'),
                (frozenset([2, 10, 5]), frozenset([1, 'light']), 1),
                (1, 1, '->')]
    assert path_states(testpath) == [(frozenset([1, 10]), frozenset(['light', 2, 5]), 5), # state 1
                (frozenset([10, 5]), frozenset([1, 2, 'light']), 2), # state 2
                (frozenset([1, 2, 10]), frozenset(['light', 5]), 5),
                (frozenset([1, 2]), frozenset(['light', 10, 5]), 10),
                (frozenset([1, 10, 5]), frozenset(['light', 2]), 2),
                (frozenset([2, 5]), frozenset([1, 10, 'light']), 10),
                (frozenset([1, 2, 5]), frozenset(['light', 10]), 10),
                (frozenset([1, 5]), frozenset(['light', 2, 10]), 10),
                (frozenset([2, 10]), frozenset([1, 5, 'light']), 5),
                (frozenset([2, 10, 5]), frozenset([1, 'light']), 1)]
    assert path_actions(testpath) == [(5, 2, '->'), # action 1
                                      (2, 1, '->'), # action 2
                                      (5, 5, '->'),
                                      (5, 10, '->'),
                                      (2, 2, '->'),
                                      (10, 1, '->'),
                                      (10, 10, '->'),
                                      (10, 2, '->'),
                                      (5, 1, '->'),
                                      (1, 1, '->')]
    return 'test_paths pass'


def test():
    assert bsuccessors((frozenset([1, 'light']), frozenset([]), 3)) == {
        (frozenset([]), frozenset([1, 'light']), 4): (1, 1, '->')}

    assert bsuccessors((frozenset([]), frozenset([2, 'light']), 0)) == {
        (frozenset([2, 'light']), frozenset([]), 2): (2, 2, '<-')}
    assert bridge_problem(frozenset((1, 2),))[-1][-1] == 2 # the [-1][-1] grabs the total elapsed time
    assert bridge_problem(frozenset((1, 2, 5, 10),))[-1][-1] == 17

    print [elapsed_time(bridge_problem([1,2,4,8,16][:N])) for N in range(6)]
    # print [bridge_problem([1, 2, 4, 8, 16][:N]) for N in range(6)]
    return 'tests pass'


print test_paths()
print test()

# ADD MORE TESTS
import doctest
class TestBridge: """
>>> elapsed_time(bridge_problem([1,2,5,10]))
17

## There are two equally good solutions
>>> S1 = [(2, 1, '->'), (1, 1, '<-'), (5, 10, '->'), (2, 2, '<-'), (2, 1, '->')]
>>> S2 = [(2, 1, '->'), (2, 2, '<-'), (5, 10, '->'), (1, 1, '<-'), (2, 1, '->')]
>>> path_actions(bridge_problem([1,2,5,10])) in (S1, S2)
True

## Try some other problems
>>> path_actions(bridge_problem([1,2,5,10,15,20]))
[(2, 1, '->'), (1, 1, '<-'), (10, 5, '->'), (2, 2, '<-'), (2, 1, '->'), (1, 1, '<-'), (15, 20, '->'), (2, 2, '<-'), (2, 1, '->')]

>>> path_actions(bridge_problem([1,2,4,8,16,32]))
[(2, 1, '->'), (1, 1, '<-'), (8, 4, '->'), (2, 2, '<-'), (1, 2, '->'), (1, 1, '<-'), (16, 32, '->'), (2, 2, '<-'), (2, 1, '->')]

>>> [elapsed_time(bridge_problem([1,2,4,8,16][:N])) for N in range(6)]
[0, 1, 2, 7, 15, 28]

>>> [elapsed_time(bridge_problem([1,1,2,3,5,8,13,21][:N])) for N in range(8)]
[0, 1, 1, 2, 6, 12, 19, 30]

"""


print elapsed_time(bridge_problem([]))
print doctest.testmod()
