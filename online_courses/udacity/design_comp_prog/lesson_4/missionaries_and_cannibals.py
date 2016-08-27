"""
Statement:
On one side of a river: a group of missionaries and cannibals are trying to cross the river
They have only one boat. The requirement is: on both side the missionaries have to be more than
the cannibals. Otherwise they will be eaten. Max. 2 on the boath and min. 1 to ride the boat

State representation:
M1, C1, B1, M2, C2, B2: where M1 is the number of missionaries on the left side

Action is one of the following string:
'M->', 'C->', '<-M','<-C','MM->', 'MC->', 'CC->', 'MM-<', 'MC-<', 'CC-<'
We should generate successor states that include more cannibals than
missionaries, but such a state should generate no successors.
"""

debug = 0

def csuccessors(state):
    """Find successors (including those that result in dining) to this
    state. But a state where the cannibals can dine has no successors.
    Successors is a dict{state:action}"""
    M1, C1, B1, M2, C2, B2 = state
    res = {}
    if 0 <= C1 <= M1 and 0 <= C2 <= M2:
        if B1 == 1:
            if M1 >= 1:
                res[(M1 - 1, C1, 1 - B1, M2 + 1, C2, B1)] = 'M->'
                if C1 >= 1:
                    res[(M1 - 1, C1 - 1, 1 - B1, M2 + 1, C2 + 1, B1)] = 'MC->'
            if C1 >= 1:
                res[(M1, C1 - 1, 1 - B1, M2, C2 + 1, B1)] = 'C->'
            if M1 >= 2:
                res[(M1 - 2, C1, 1 - B1, M2 + 2, C2, B1)] = 'MM->'
            if C1 >= 2:
                res[(M1, C1 - 2, 1 - B1, M2, C2 + 2, B1)] = 'CC->'
        else:
            if M2 >= 1:
                res[(M1 + 1, C1, B2, M2 - 1, C2, 1 - B2)] = '<-M'
                if C2 >= 1:
                    res[(M1 + 1, C1 + 1, B2, M2 - 1, C2 - 1, 1 - B2)] = '<-MC'
            if C2 >= 1:
                res[(M1, C1 + 1, B2, M2, C2 - 1, 1 - B2)] = '<-C'
            if M2 >= 2:
                res[(M1 + 2, C1, B2, M2 - 2, C2, 1 - B2)] = '<-MM'
            if C2 >= 2:
                res[(M1, C1 + 2, B2, M2, C2 - 2, 1 - B2)] = '<-CC'

    return res


def mc_problem(start_state=(3,3,1,0,0,0), goal=None):
    """
    Solve the missionaries and cannibals problem.
    :param start_state: by default it's number of m, c and where the boat is
    :param goal: by default it's reverse of start_state (all are on the other side of river)
    :return: a shortest path from start_state to goal (least number of steps)
    algo: let's try BFS approach
    """
    if start_state == goal or (start_state[0] == 0 and start_state[1] == 0):
        return
    explored = set()
    frontier = [[start_state]]  # a list of paths so far
    while frontier:
        cur_path = frontier.pop(0)  # pop first
        cur_state = cur_path[-1]
        if debug:
            print "cur_path = %s" % str(cur_path)
        # check if we reach specified goal or all people are on the other side
        if cur_state == goal or (cur_state[0] == 0 and cur_state[1] == 0):
            return cur_path
        for (state, action) in csuccessors(cur_state).items():
            if state not in explored:
                explored.add(state)
                path = cur_path + [action, state]
                if debug:
                    print "path = %s" % str(path)
                frontier.append(path)  # add to last
                if debug:
                    print "frontier = %s\n" % str(frontier)
    return []

def test():
    print "File: missionaries_and_cannibals.py"
    assert csuccessors((2, 2, 1, 0, 0, 0)) == {(2, 1, 0, 0, 1, 1): 'C->',
                                               (1, 2, 0, 1, 0, 1): 'M->',
                                               (0, 2, 0, 2, 0, 1): 'MM->',
                                               (1, 1, 0, 1, 1, 1): 'MC->',
                                               (2, 0, 0, 0, 2, 1): 'CC->'}
    assert csuccessors((1, 1, 0, 4, 3, 1)) == {(1, 2, 1, 4, 2, 0): '<-C',
                                               (2, 1, 1, 3, 3, 0): '<-M',
                                               (3, 1, 1, 2, 3, 0): '<-MM',
                                               (1, 3, 1, 4, 1, 0): '<-CC',
                                               (2, 2, 1, 3, 2, 0): '<-MC'}
    assert csuccessors((1, 4, 1, 2, 2, 0)) == {}
    print mc_problem((3,3,1,0,0,0))

    return 'tests pass'

print test()
