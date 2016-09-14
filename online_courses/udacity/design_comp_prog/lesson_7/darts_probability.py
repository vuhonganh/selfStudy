# Unit 5: Probability in the game of Darts

"""
In the game of darts, players throw darts at a board to score points.
The circular board has a 'bulls-eye' in the center and 20 slices
called sections, numbered 1 to 20, radiating out from the bulls-eye.
The board is also divided into concentric rings.  The bulls-eye has
two rings: an outer 'single' ring and an inner 'double' ring.  Each
section is divided into 4 rings: starting at the center we have a
thick single ring, a thin triple ring, another thick single ring, and
a thin double ring.  A ring/section combination is called a 'target';
they have names like 'S20', 'D20' and 'T20' for single, double, and
triple 20, respectively; these score 20, 40, and 60 points. The
bulls-eyes are named 'SB' and 'DB', worth 25 and 50 points
respectively. Illustration (png image): http://goo.gl/i7XJ9

There are several variants of darts play; in the game called '501',
each player throws three darts per turn, adding up points until they
total exactly 501. However, the final dart must be in a double ring.

Your first task is to write the function double_out(total), which will
output a list of 1 to 3 darts that add up to total, with the
restriction that the final dart is a double. See test_darts() for
examples. Return None if there is no list that achieves the total.

Often there are several ways to achieve a total.  You must return a
shortest possible list, but you have your choice of which one. For
example, for total=100, you can choose ['T20', 'D20'] or ['DB', 'DB']
but you cannot choose ['T20', 'D10', 'D10'].
"""
from collections import defaultdict

def test_darts():
    "Test the double_out function."
    assert double_out(170) == ['T20', 'T20', 'DB']
    assert double_out(171) == None
    assert double_out(100) in (['T20', 'D20'], ['DB', 'DB'])


"""
My strategy: I decided to choose the result that has the highest valued
target(s) first, e.g. always take T20 on the first dart if we can achieve
a solution that way.  If not, try T19 first, and so on. At first I thought
I would need three passes: first try to solve with one dart, then with two,
then with three.  But I realized that if we include 0 as a possible dart
value, and always try the 0 first, then we get the effect of having three
passes, but we only have to code one pass.  So I creted ordered_points as
a list of all possible scores that a single dart can achieve, with 0 first,
and then descending: [0, 60, 57, ..., 1].  I iterate dart1 and dart2 over
that; then dart3 must be whatever is left over to add up to total.  If
dart3 is a valid element of points, then we have a solution.  But the
solution, is a list of numbers, like [0, 60, 40]; we need to transform that
into a list of target names, like ['T20', 'D20'], we do that by defining name(d)
to get the name of a target that scores d.  When there are several choices,
we must choose a double for the last dart, but for the others I prefer the
easiest targets first: 'S' is easiest, then 'T', then 'D'.
"""
S = 1
D = 2
T = 3
B = 25
set_points = set(p for i in range(1, 21) for p in (i, i*2, i*3))
set_points.add(25)
set_points.add(50)
ordered_points = [0] + sorted(set_points, reverse=True)


def is_single(point):
    return point == 25 or point <= 20


def is_double(point):
    return point == 50 or (point <= 40 and point % 2 == 0)


def is_trible(point):
    return point % 3 == 0


def target_name(points):
    """Given a specific points, print its target_name. prefer order: S,T,D > S,D > T,D > D,D"""
    res = []
    for i in range(len(points) - 1):
        if is_single(points[i]):
            if points[i] == 25:
                res.append('SB')
            else:
                res.append('S' + str(points[i]))
        elif is_trible(points[i]):
            res.append('T' + str(points[i] / 3))
        else:
            if points[i] == 50:
                res.append('DB')
            else:
                res.append('D' + str(points[i] / 2))
    if points[-1] == 50:
        res.append('DB')
    else:
        res.append('D' + str(points[-1] / 2))
    return res


def double_out(total):
    """Return a shortest possible list of targets that add to total,
    where the length <= 3 and the final element is a double.
    If there is no solution, return None."""
    max_point = 60 + 60 + 50  # max_point for one turn (3 throws) in double out
    if total > max_point:
        return None
    for point1 in ordered_points:
        if point1 > total:
            continue
        for point2 in ordered_points[1:]:
            if point2 >= total - point1:
                continue
            else:
                point3 = total - point1 - point2
                if point3 % 2 == 0 and (point3 == 50 or point3 / 2 <= 20):
                    res = [point1, point2, point3] if point1 != 0 else [point2, point3]
                    return target_name(res)
    return None


print double_out(100)
print double_out(170)
print double_out(60)



"""
It is easy enough to say "170 points? Easy! Just hit T20, T20, DB."
But, at least for me, it is much harder to actually execute the plan
and hit each target.  In this second half of the question, we
investigate what happens if the dart-thrower is not 100% accurate.

We will use a wrong (but still useful) model of inaccuracy. A player
has a single number from 0 to 1 that characterizes his/her miss rate.
If miss=0.0, that means the player hits the target every time.
But if miss is, say, 0.1, then the player misses the section s/he
is aiming at 10% of the time, and also (independently) misses the thin
double or triple ring 10% of the time. Where do the misses go?
Here's the model:

First, for ring accuracy.  If you aim for the triple ring, all the
misses go to a single ring (some to the inner one, some to the outer
one, but the model doesn't distinguish between these). If you aim for
the double ring (at the edge of the board), half the misses (e.g. 0.05
if miss=0.1) go to the single ring, and half off the board. (We will
agree to call the off-the-board 'target' by the name 'OFF'.) If you
aim for a thick single ring, it is about 5 times thicker than the thin
rings, so your miss ratio is reduced to 1/5th, and of these, half go to
the double ring and half to the triple.  So with miss=0.1, 0.01 will go
to each of the double and triple ring.  Finally, for the bulls-eyes. If
you aim for the single bull, 1/4 of your misses go to the double bull and
3/4 to the single ring.  If you aim for the double bull, it is tiny, so
your miss rate is tripled; of that, 2/3 goes to the single ring and 1/3
to the single bull ring.

Now, for section accuracy.  Half your miss rate goes one section clockwise
and half one section counter-clockwise from your target. The clockwise
order of sections is:

    20 1 18 4 13 6 10 15 2 17 3 19 7 16 8 11 14 9 12 5

If you aim for the bull (single or double) and miss on rings, then the
section you end up on is equally possible among all 20 sections.  But
independent of that you can also miss on sections; again such a miss
is equally likely to go to any section and should be recorded as being
in the single ring.

You will need to build a model for these probabilities, and define the
function outcome(target, miss), which takes a target (like 'T20') and
a miss ration (like 0.1) and returns a dict of {target: probability}
pairs indicating the possible outcomes.  You will also define
best_target(miss) which, for a given miss ratio, returns the target
with the highest expected score.

If you are very ambitious, you can try to find the optimal strategy for
accuracy-limited darts: given a state defined by your total score
needed and the number of darts remaining in your 3-dart turn, return
the target that minimizes the expected number of total 3-dart turns
(not the number of darts) required to reach the total.  This is harder
than Pig for several reasons: there are many outcomes, so the search space
is large; also, it is always possible to miss a double, and thus there is
no guarantee that the game will end in a finite number of moves.
"""
sections = (20, 1, 18, 4, 13, 6, 10, 15, 2, 17, 3, 19, 7, 16, 8, 11, 14, 9, 12, 5)


'''
First, for ring accuracy.  If you aim for the triple ring, all the
misses go to a single ring (some to the inner one, some to the outer
one, but the model doesn't distinguish between these). If you aim for
the double ring (at the edge of the board), half the misses (e.g. 0.05
if miss=0.1) go to the single ring, and half off the board. (We will
agree to call the off-the-board 'target' by the name 'OFF'.) If you
aim for a thick single ring, it is about 5 times thicker than the thin
rings, so your miss ratio is reduced to 1/5th, and of these, half go to
the double ring and half to the triple.  So with miss=0.1, 0.01 will go
to each of the double and triple ring.  Finally, for the bulls-eyes. If
you aim for the single bull, 1/4 of your misses go to the double bull and
3/4 to the single ring.  If you aim for the double bull, it is tiny, so
your miss rate is tripled; of that, 2/3 goes to the single ring and 1/3
to the single bull ring.
'''
ring_accuracy = {'T': (0.5, 'S', 0.5, 'S'), 'D': (0.5, 'S', 0.5, 'OFF'), 'S': (0.1, 'T', 0.1, 'D'),
                 'SB': (0.25, 'DB', 0.75, 'S'), 'DB': (2, 'S', 1, 'SB')}


def ring_outcome(target, miss_rate):
    """Given a target and a miss_rate, return possibilities of rings it may fall to in dictionary type"""
    if 'T' in target:
        return {'T': 1 - miss_rate, 'S': miss_rate}
    elif target == 'SB':
        return {'SB': 1 - miss_rate, 'DB': 0.25 * miss_rate, 'S': 0.75 * miss_rate}
    elif target == 'DB':
        return {'DB': 1 - 3 * miss_rate, 'SB': miss_rate, 'S': 2 * miss_rate}
    elif 'D' in target:
        return {'S': 0.5 * miss_rate, 'D': 1 - miss_rate, 'OFF': 0.5 * miss_rate}  # 0.5 * miss_rate is OFF
    elif 'S' in target:
        return {'S': 1 - 0.2 * miss_rate, 'T': 0.5 * 0.2 * miss_rate, 'D': 0.5 * 0.2 * miss_rate}
    else:
        print 'something wrong in ring_outcome'
        raise ValueError


def section_outcome(target, miss_rate):
    res = {}
    if 'B' not in target:  # not bull
        target_section = int(target[1:])
        neighbor_sections = find_neigbors_sections(target_section)
        res[str(target_section)] = 1 - miss_rate
        for neighbor in neighbor_sections:
            res[str(neighbor)] = miss_rate / 2.0
    else:  # bull case
        res['B'] = 1 - miss_rate
        for i in range(1, 21):
            res[str(i)] = miss_rate / 20.0
    return res


def find_neigbors_sections(section):
    """Given an index in sections, return 2 neighbors of it"""
    idx = sections.index(section)
    if idx == 0:
        return sections[idx + 1], sections[-1]
    elif idx == len(sections) - 1:
        return sections[0], sections[idx - 1]
    else:
        return sections[idx - 1], sections[idx + 1]


def outcome(target, miss_rate):
    "Return a probability distribution of [(target, probability)] pairs."
    dict_ring = ring_outcome(target, miss_rate)
    dict_section = section_outcome(target, miss_rate)
    res = {}  # SHOULD USE collections.defaultdict next time to avoid checking non existed key in dict
    for ring, p_ring in dict_ring.items():
        for section, p_section in dict_section.items():
            if ring == 'OFF':
                if ring in res:
                    res[ring] += p_ring * p_section
                else:
                    res[ring] = p_ring * p_section
            elif ring == 'SB' or ring == 'DB':
                if section == 'B':
                    if ring in res:
                        res[ring] += p_ring * p_section
                    else:
                        res[ring] = p_ring * p_section
                else:  # if the ring hits bull but the section hits a thick single section,
                    # then we got probability of single section
                    rs = 'S' + section
                    if rs in res:
                        res[rs] += p_ring * p_section
                    else:
                        res[rs] = p_ring * p_section

            else:
                if section != 'B':
                    rs = ring + section
                    p_rs = p_ring * p_section
                    if rs in res:
                        res[rs] += p_rs
                    else:
                        res[rs] = p_rs
                else:
                    p_rs = p_ring * p_section / 20.
                    for s in sections:
                        rs = 'S' + str(s)
                        if rs in res:
                            res[rs] += p_rs
                        else:
                            res[rs] = p_rs
    return res



# SOLUTION of the prof: note the use of defaultdict is really handy
# def outcome(target, miss):
#     "Return a probability distribution of [(target, probability)] pairs."
#     results = defaultdict(float)
#     for (ring, ringP) in ring_outcome(target, miss):
#         for (sect, sectP) in section_outcome(target, miss):
#             if ring == 'S' and sect.endswith('B'):
#                 # If sect hits bull, but ring misses out to S ring,
#                 # then spread the results over all sections.
#                 print 'ring = ', ring, ', p_ring = ', ringP
#                 print 'sect = ', sect, ', p_sect = ', sectP
#                 for s in sections:
#                     print Target(ring, s), ' will be added',  (ringP * sectP) / 20
#                     results[Target(ring, s)] += (ringP * sectP) / 20.
#             else:
#                 print 'ring = ', ring, ', p_ring = ', ringP
#                 print 'sect = ', sect, ', p_sect = ', sectP
#                 print Target(ring, sect), ' will be added', ringP * sectP
#                 results[Target(ring, sect)] += (ringP * sectP)
#     return dict(results)
#
# def ring_outcome(target, miss):
#     "Return a probability distribution of [(ring, probability)] pairs."
#     hit = 1.0 - miss
#     r = target[0]
#     if target == 'DB': # misses tripled; can miss to SB or to S
#         miss = min(3*miss, 1.)
#         hit = 1. - miss
#         return [('DB', hit), ('SB', miss/3.), ('S', 2./3.*miss)]
#     elif target == 'SB': # Bull can miss in either S or DB direction
#         return [('SB', hit), ('DB', miss/4.), ('S', 3/4.*miss)]
#     elif r == 'S': # miss ratio cut to miss/5
#         return [(r, 1.0 - miss/5.), ('D', miss/10.), ('T', miss/10.)]
#     elif r == 'D': # Double can miss either on board or off
#         return [(r, hit), ('S', miss/2), ('OFF', miss/2)]
#     elif r == 'T': # Triple can miss in either direction, but both are S
#         return [(r, hit), ('S', miss)]
#
# def section_outcome(target, miss):
#     "Return a probability distribution of [(section, probability)] pairs."
#     hit = 1.0 - miss
#     if target in ('SB', 'DB'):
#         misses = [(s, miss/20.) for s in sections]
#     else:
#         i = sections.index(target[1:])
#         misses = [(sections[i-1], miss/2), (sections[(i+1)%20], miss/2)]
#     return  [(target[1:], hit)] + misses
#
# def Target(ring, section):
#     "Construct a target name from a ring and section."
#     if ring == 'OFF':
#         return 'OFF'
#     elif ring in ('SB', 'DB'):
#         return ring if (section == 'B') else ('S' + section)
#     else:
#         return ring + section

# sections = "20 1 18 4 13 6 10 15 2 17 3 19 7 16 8 11 14 9 12 5".split()
# targets = set(r+s for r in 'SDT' for s in sections) | set(['SB', 'DB'])

all_targets = set(r + str(s) for r in 'SDT' for s in sections) | set(['SB', 'DB'])
real_val = {'OFF': 0, }

def read_val(target):
    global real_val
    if target in real_val:
        return real_val[target]
    else:
        if target[0] == 'S':
            # print 'target = ', target
            real_val[target] = 25 if target[1] == 'B' else int(target[1:])
        elif target[0] == 'D':
            real_val[target] = 50 if target[1] == 'B' else 2 * int(target[1:])
        elif target[0] == 'T':
            real_val[target] = 3 * int(target[1:])
        else:
            raise ValueError
        return real_val[target]

def best_target(miss):
    "Return the target that maximizes the expected score."
    return max(all_targets, key=lambda t: expected_val(t, miss))


def expected_val(target, miss):
    return sum(read_val(v) * p for (v, p) in (outcome(target, miss)).items())

print expected_val('SB', 0.2)

def same_outcome(dict1, dict2):
    "Two states are the same if all corresponding sets of locs are the same."
    return all(abs(dict1.get(key, 0) - dict2.get(key, 0)) <= 0.0001
               for key in set(dict1) | set(dict2))


def test_darts2():
    assert best_target(0.0) == 'T20'
    assert best_target(0.1) == 'T20'
    assert best_target(0.4) == 'T19'
    assert same_outcome(outcome('T20', 0.0), {'T20': 1.0})
    assert same_outcome(outcome('T20', 0.1),
                        {'T20': 0.81, 'S1': 0.005, 'T5': 0.045,
                         'S5': 0.005, 'T1': 0.045, 'S20': 0.09})
    assert (same_outcome(
        outcome('SB', 0.2),
        {'S9': 0.016, 'S8': 0.016, 'S3': 0.016, 'S2': 0.016, 'S1': 0.016,
         'DB': 0.04, 'S6': 0.016, 'S5': 0.016, 'S4': 0.016, 'S20': 0.016,
         'S19': 0.016, 'S18': 0.016, 'S13': 0.016, 'S12': 0.016, 'S11': 0.016,
         'S10': 0.016, 'S17': 0.016, 'S16': 0.016, 'S15': 0.016, 'S14': 0.016,
         'S7': 0.016, 'SB': 0.64}))


# print outcome('T20', .1)
print outcome('SB', .2)
print section_outcome('SB', 0.2)
print ring_outcome('SB', 0.2)
print best_target(0.0)