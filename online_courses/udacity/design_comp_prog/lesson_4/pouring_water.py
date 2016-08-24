"""
Pouring water problem: given 2 cups with capacity X and Y (in litre) and a sink of water.
There are 6 actions that can be made:
1) pour water from X to Y
2) pour water from Y to X
3) fill X (by water from sink)
4) fill Y (by water from sink)
5) empty X
6) empty Y
Note that the cups have no precise scale, we only know its capacity.
Given a goal (in litre) find a solution (a sequence of actions) to achieve it.
This is an exploration problem:
    We can represent a state by (x, y) where x and y are the current quantity in cups.
    Main point of algorithms: use queue and set to avoid exploring old state
"""
NoSolution = []


def pouring(X, Y, goal, start=(0, 0)):
    if goal in start:
        return [start]
    explored = set()   # set of visited states
    frontier = [[start]]    # ordered list of paths:
    while frontier:
        path = frontier.pop(0)  # pop out the first path of the frontier
        # print path
        (x, y) = path[-1]   # current state of this path is stored at last element
        # (state, action) will be elem in a dictionary
        for (state, action) in successors(x, y, X, Y).items():
            if state not in explored:
                explored.add(state)
                # need to add in this order [action, state] to access state at last element
                path2 = path + [action, state]
                if goal in state:
                    return path2
                else:
                    frontier.append(path2)  # add this new_path at the back (i.e. last elem)
    return NoSolution


def successors(x, y, X, Y):
    assert (x <= X and y <= Y)
    # (state, action) stored in a dictionary
    return {
        (X, y): 'fill X',
        (x, Y): 'fill Y',
        (0, y): 'empty X',
        (x, 0): 'empty Y',
        ((0, y + x) if x + y <= Y else (x - (Y - y), Y)): 'X -> Y',
        ((x + y, 0) if x + y <= X else (X, y - (X - x))): 'Y -> X'
    }

print pouring(4, 9, 6)