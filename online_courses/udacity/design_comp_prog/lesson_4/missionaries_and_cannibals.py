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


def csuccessors(state):
    """Find successors (including those that result in dining) to this
    state. But a state where the cannibals can dine has no successors.
    Successors is a dict{state:action}"""
    M1, C1, B1, M2, C2, B2 = state
    res = {}
    if C1 <= M1 and C2 <= M2:
        if B1 == 1:
            res[(M1 - 1, C1, 1 - B1, M2 + 1, C2, B1)] = 'M->'
            res[(M1, C1 - 1, 1 - B1, M2, C2 + 1, B1)] = 'C->'
            res[(M1 - 1, C1 - 1, 1 - B1, M2 + 1, C2 + 1, B1)] = 'MC->'
            res[(M1 - 2, C1, 1 - B1, M2 + 2, C2, B1)] = 'MM->'
            res[(M1, C1 - 2, 1 - B1, M2, C2 + 2, B1)] = 'CC->'
        else:
            res[(M1 + 1, C1, B2, M2 - 1, C2, 1 - B2)] = '<-M'
            res[(M1, C1 + 1, B2, M2, C2 - 1, 1 - B2)] = '<-C'
            res[(M1 + 2, C1, B2, M2 - 2, C2, 1 - B2)] = '<-MM'
            res[(M1 + 1, C1 + 1, B2, M2 - 1, C2 - 1, 1 - B2)] = '<-MC'
            res[(M1, C1 + 2, B2, M2, C2 - 2, 1 - B2)] = '<-CC'

    return res




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
    return 'tests pass'

print test()
