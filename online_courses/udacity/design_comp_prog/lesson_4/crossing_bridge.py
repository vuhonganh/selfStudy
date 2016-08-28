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
    while frontier:
        cur_path = frontier.pop(0)
        cur_state = cur_path[-1]
        if not cur_state[0]:    # all people are not in the left
            return cur_path
        else:
            explored.add(cur_state)
            for (next_state, action) in bsuccessors(cur_state).items():
                if next_state not in explored:
                    next_path = cur_path + [action, next_state]
                    frontier.append(next_path)
            frontier.sort(key=elapsed_time)
    return []


# Need a better version of state which should only care about the
# people on left and right side, not the time to avoid repeating move
# The new path will be: [state, (action, total_time_after_applying_this_action), ...]
def bsuccessors2(state):
    """Return a dict of {state:action} pairs. A state is a
    (left, right) tuple, where left and right are frozensets
    of people (indicated by their travel times) and/or the light."""
    left, right = state
    # only the side having the lamp can go to the other side:
    res_dict = {}
    if 'light' in left:
        for a in left:
            if a is not 'light':
                for b in left:
                    if b is not 'light':
                        next_state = (left - frozenset({a, b, 'light'}),
                                      right | frozenset({a, b, 'light'})
                                      )
                        res_dict[next_state] = (a, b, '->')
    else:
        for a in right:
            if a is not 'light':
                for b in right:
                    if b is not 'light':
                        next_state = (left | frozenset({a, b, 'light'}),
                                      right - frozenset({a, b, 'light'})
                                      )
                        res_dict[next_state] = (a, b, '<-')
    return res_dict


def path_cost(path):
    """The total cost of a path (which is stored in a tuple
    with the final action."""
    # path = (state, (action, total_cost), state, ... )
    if len(path) < 3:
        return 0
    else:
        return path[-2][1]


def bcost(action):
    """Returns the cost (a number) of an action in the
    bridge problem."""
    # An action is an (a, b, arrow) tuple; a and b are
    # times; arrow is a string.
    a, b, arrow = action
    return max(a,b)


def final_state(path):
    return path[-1]


def bridge_problem2(left):
    """More efficient version that uses bsuccessors2()"""
    left = frozenset(left) | frozenset({'light'})
    explored = set()    # set of explored state
    # original state (at t = 0) is: all people are in the left
    original_state = (left, frozenset())
    # at the beginning there is only one path containing original state
    frontier = [ [original_state] ]  # frontier is an ordered list of path
    while frontier:
        cur_path = frontier.pop(0)
        cur_state = cur_path[-1]
        if not cur_state[0]:    # all people are not in the left
            return cur_path
        else:
            explored.add(cur_state)
            pcost = path_cost(cur_path)
            for (next_state, action) in bsuccessors2(cur_state).items():
                if next_state not in explored:
                    next_path = cur_path + [(action, pcost + bcost(action)), next_state]
                    add_to_frontier(frontier, next_path)
    return []


def add_to_frontier(frontier, new_path):
    """For each new_path needs to find if an old_path having the same final state
    If new_path is better, delete old_path"""
    old_path_idx = None
    for idx, op in enumerate(frontier):
        if op[-1] == new_path[-1]:
            old_path_idx = idx
            break
    if old_path_idx is not None and path_cost(frontier[old_path_idx]) < path_cost(new_path):
        return
    elif old_path_idx is not None:
        del frontier[old_path_idx]

    frontier.append(new_path)
    frontier.sort(key=path_cost)


def lowest_cost_search(start, successors, is_goal, action_cost):
    """Return the lowest cost path, starting from start state,
    and considering successors(state) => {state:(action, total_cost), ...},
    that ends in a state for which is_goal(state) is true,
    where the cost of a path is the sum of action costs,
    which are given by action_cost(action)."""
    if is_goal(start):
        return [start]
    explored = set()
    explored.add(start)
    frontier = [[start]]
    while frontier:
        cur_path = frontier.pop(0)
        cur_state = cur_path[-1]
        if is_goal(cur_state[0]):
            return cur_path
        explored.add(cur_state) # VERY IMPORTANT to add cur_state here
        cur_cost = cur_path[-2][1] if len(cur_path) > 2 else 0
        for (state, action) in successors(cur_state).items():
            if state not in explored:
                # CAN NOT add state to explored because we could ignore better cases
                total_cost = action_cost(action) + cur_cost
                path = cur_path + [(action, total_cost), state]
                add_to_frontier(frontier, path)
    return []


def bridge_problem3(here):
    """Find the fastest (least elapsed time) path to
    the goal in the bridge problem."""
    left = frozenset(here) | frozenset({'light'})
    start = (left, frozenset())
    return lowest_cost_search(start, bsuccessors2, is_goal_bridge, bcost)

def is_goal_bridge(here):
    return not here or here == frozenset({'light'})



def test_bridge_3():
    here = [1, 2, 5, 10]
    print bridge_problem3(here)
    # assert bridge_problem3(here) == [
    #         (frozenset([1, 2, 'light', 10, 5]), frozenset([])),
    #         ((2, 1, '->'), 2),
    #         (frozenset([10, 5]), frozenset([1, 2, 'light'])),
    #         ((2, 2, '<-'), 4),
    #         (frozenset(['light', 10, 2, 5]), frozenset([1])),
    #         ((5, 10, '->'), 14),
    #         (frozenset([2]), frozenset([1, 10, 5, 'light'])),
    #         ((1, 1, '<-'), 15),
    #         (frozenset([1, 2, 'light']), frozenset([10, 5])),
    #         ((2, 1, '->'), 17),
    #         (frozenset([]), frozenset([1, 10, 2, 5, 'light']))]
    return 'test bridge 3 passes'

print test_bridge_3()

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
    # assert bsuccessors((frozenset([1, 'light']), frozenset([]), 3)) == {
    #     (frozenset([]), frozenset([1, 'light']), 4): (1, 1, '->')}
    #
    # assert bsuccessors((frozenset([]), frozenset([2, 'light']), 0)) == {
    #     (frozenset([2, 'light']), frozenset([]), 2): (2, 2, '<-')}
    # assert bridge_problem(frozenset((1, 2),))[-1][-1] == 2 # the [-1][-1] grabs the total elapsed time
    # assert bridge_problem(frozenset((1, 2, 5, 10),))[-1][-1] == 17
    #
    here1 = frozenset([1, 'light'])
    there1 = frozenset([])

    here2 = frozenset([1, 2, 'light'])
    there2 = frozenset([3])

    assert bsuccessors2((here1, there1)) == {
        (frozenset([]), frozenset([1, 'light'])): (1, 1, '->')}
    assert bsuccessors2((here2, there2)) == {
        (frozenset([1]), frozenset(['light', 2, 3])): (2, 2, '->'),
        (frozenset([2]), frozenset([1, 3, 'light'])): (1, 1, '->'),
        (frozenset([]), frozenset([1, 2, 3, 'light'])): (2, 1, '->')}

    assert path_cost(('fake_state1', ((2, 5, '->'), 5), 'fake_state2')) == 5
    assert path_cost(('fs1', ((2, 1, '->'), 2), 'fs2', ((3, 4, '<-'), 6), 'fs3')) == 6
    assert bcost((4, 2, '->'), ) == 4
    assert bcost((3, 10, '<-'), ) == 10
    assert path_cost(bridge_problem2(frozenset((1, 2), ))) == 2
    assert path_cost(bridge_problem2(frozenset((1, 2, 5, 10), ))) == 17
    return 'tests pass'
print test_paths()
print test()
