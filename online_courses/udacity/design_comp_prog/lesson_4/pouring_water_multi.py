global_goal = 0
global_caps = ()

def more_pour_problem(capacities, goal, start=None):
    """The first argument is a tuple of capacities (numbers) of glasses; the
    goal is a number which we must achieve in some glass.  start is a tuple
    of starting levels for each glass; if None, that means 0 for all.
    Start at start state and follow successors until we reach the goal.
    Keep track of frontier and previously explored; fail when no frontier.
    On success return a path: a [state, action, state2, ...] list, where an
    action is one of ('fill', i), ('empty', i), ('pour', i, j), where
    i and j are indices indicating the glass number
    and ('pour', i, j) means pouring from i to j"""
    # if start is None then initialize it by 0
    if max(capacities) < goal:
        return []
    if not start:
        start = (0, ) * len(capacities)
    global global_goal
    global_goal = goal
    global global_caps
    global_caps = capacities

    return shortest_path_search(start, successors, is_goal)


def successors(state):
    res_dict = {}
    global global_caps
    n = len(global_caps)
    for i in range(n):
        for j in range(n):
            if i != j:
                new_state = list(state)
                if state[i] + state[j] <= global_caps[j]: #  pour i -> j
                    new_state[i] = 0
                    new_state[j] = state[i] + state[j]
                else:
                    new_state[i] = state[i] - (global_caps[j] - state[j])
                    new_state[j] = global_caps[j]
                res_dict[tuple(new_state)] = ('pour', i, j)

                new_state = list(state)
                if state[i] + state[j] <= global_caps[i]:  # pour j -> i
                    new_state[j] = 0
                    new_state[i] = state[i] + state[j]
                else:
                    new_state[i] = global_caps[i]
                    new_state[j] = state[j] - (global_caps[i] - state[i])
                res_dict[tuple(new_state)] = ('pour', j, i)
            else:
                new_state = list(state)
                new_state[i] = 0
                res_dict[tuple(new_state)] = ('empty', i)
                new_state[i] = global_caps[i]
                res_dict[tuple(new_state)] = ('fill', i)
    return res_dict


def is_goal(state):
    return global_goal in state


def shortest_path_search(start, successors, is_goal):
    """Find the shortest path from start state to a state
    such that is_goal(state) is true."""

    if is_goal(start):
        return [start]
    Fail = []
    explored = set()
    frontier = [[start]]
    while frontier:
        path = frontier.pop(0)
        s = path[-1]
        for (state, action) in successors(s).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if is_goal(state):
                    return path2
                else:
                    frontier.append(path2)
    return Fail


# Fail = []


def test_more_pour():
    assert more_pour_problem((1, 2, 4, 8), 4) == [
        (0, 0, 0, 0), ('fill', 2), (0, 0, 4, 0)]
    assert more_pour_problem((1, 2, 4), 3) == [
        (0, 0, 0), ('fill', 2), (0, 0, 4), ('pour', 2, 0), (1, 0, 3)]
    starbucks = (8, 12, 16, 20, 24)
    assert not any(more_pour_problem(starbucks, odd) for odd in (3, 5, 7, 9))
    assert all(more_pour_problem((1, 3, 9, 27), n) for n in range(28))
    assert more_pour_problem((1, 3, 9, 27), 28) == []
    return 'test_more_pour passes'


print test_more_pour()

print more_pour_problem((1,2),1)
print more_pour_problem((1,2,3),2)