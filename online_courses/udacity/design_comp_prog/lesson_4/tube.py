# Write a function, subway, that takes lines as input (read more about
# the **lines notation in the instructor comments box below) and returns
# a dictionary of the form {station:{neighbor:line, ...}, ... }
#
# For example, when calling subway(boston), one of the entries in the
# resulting dictionary should be 'foresthills': {'backbay': 'orange'}.
# This means that foresthills only has one neighbor ('backbay') and
# that neighbor is on the orange line. Other stations have more neighbors:
# 'state', for example, has 4 neighbors.


def subway(**lines):
    """Define a subway map. Input is subway(linename='station1 station2...'...).
    Convert that and return a dict of the form: {station:{neighbor:line,...},...}"""
    resDict = {}
    if lines is not None:
        for linename, allStations in lines.iteritems():
            stations_one_line = allStations.split()
            for i in range(len(stations_one_line)):
                if stations_one_line[i] not in resDict:
                    resDict[stations_one_line[i]] = {}
                if i == 0:
                    resDict[stations_one_line[i]].update({stations_one_line[i + 1]: linename})
                elif i == len(stations_one_line) - 1:
                    resDict[stations_one_line[i]].update({stations_one_line[i - 1]: linename})
                else:
                    resDict[stations_one_line[i]].update({stations_one_line[i + 1]: linename})
                    resDict[stations_one_line[i]].update({stations_one_line[i - 1]: linename})
    return resDict


boston = subway(
    blue='bowdoin government state aquarium maverick airport suffolk revere wonderland',
    orange='oakgrove sullivan haymarket state downtown chinatown tufts backbay foresthills',
    green='lechmere science north haymarket government park copley kenmore newton riverside',
    red='alewife davis porter harvard central mit charles park downtown south umass mattapan')


def ride(here, there, system=boston):
    """Return a path on the subway system from here to there.
    here, there: a station (in string) in the system"""
    # trivial tests
    assert here in system
    assert there in system

    # need to define a state, a goal and successors

    def is_goal(state):
        return state == there

    def successors(state):  # return a dict of form: {next_state1 : action1, next_state2 : action2, ...}
        return system[state]  # this is a dict {nei1 : line1, nei2 : line2,...}

    return shortest_path_search(here, successors, is_goal)


def longest_ride(system):
    """"Return the longest possible 'shortest path'
    ride between any two stops in the system."""
    ## your code here


def shortest_path_search(start, successors, is_goal):
    """Find the shortest path from start state to a state
    such that is_goal(state) is true."""
    if is_goal(start):
        return [start]
    explored = set()  # set of states we have visited
    frontier = [[start]]  # ordered list of paths we have blazed
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
    return []


def path_states(path):
    "Return a list of states in this path."
    return path[0::2]


def path_actions(path):
    "Return a list of actions in this path."
    return path[1::2]


def test_ride():
    assert ride('mit', 'government') == [
        'mit', 'red', 'charles', 'red', 'park', 'green', 'government']
    assert ride('mattapan', 'foresthills') == [
        'mattapan', 'red', 'umass', 'red', 'south', 'red', 'downtown',
        'orange', 'chinatown', 'orange', 'tufts', 'orange', 'backbay', 'orange', 'foresthills']
    assert ride('newton', 'alewife') == [
        'newton', 'green', 'kenmore', 'green', 'copley', 'green', 'park', 'red', 'charles', 'red',
        'mit', 'red', 'central', 'red', 'harvard', 'red', 'porter', 'red', 'davis', 'red', 'alewife']
    # assert (path_states(longest_ride(boston)) == [
    #     'wonderland', 'revere', 'suffolk', 'airport', 'maverick', 'aquarium', 'state', 'downtown', 'park',
    #     'charles', 'mit', 'central', 'harvard', 'porter', 'davis', 'alewife'] or
    #         path_states(longest_ride(boston)) == [
    #             'alewife', 'davis', 'porter', 'harvard', 'central', 'mit', 'charles',
    #             'park', 'downtown', 'state', 'aquarium', 'maverick', 'airport', 'suffolk', 'revere', 'wonderland'])
    # assert len(path_states(longest_ride(boston))) == 16
    return 'test_ride passes'


print 'File: tube.py'
print test_ride()
    # subway(boston)
