# zebra_puzzle.py

""" Statement: Zebra Puzzle
1 There are five houses.
2 The Englishman lives in the red house.
3 The Spaniard owns the dog.
4 Coffee is drunk in the green house.
5 The Ukrainian drinks tea.
6 The green house is immediately to the right of the ivory house.
7 The Old Gold smoker owns snails.
8 Kools are smoked in the yellow house.
9 Milk is drunk in the middle house.
10 The Norwegian lives in the first house.
11 The man who smokes Chesterfields lives in the house next to the man with the fox.
12 Kools are smoked in a house next to the house where the horse is kept.
13 The Lucky Strike smoker drinks orange juice.
14 The Japanese smokes Parliaments.
15 The Norwegian lives next to the blue house.

Who drinks water? Who owns the zebra?

Each house is painted a different color, and their inhabitants are of different nationalities, 
own different pets, drink different beverages and smoke different brands of American cigarettes.
"""

import itertools

def imright(h1, h2):
    "House h1 is immediately right of h2 if h1-h2 == 1."
    return h1-h2 == 1

def nextto(h1, h2):
    "Two houses are next to each other if they differ by 1."
    return abs(h1-h2) == 1

def zebra_puzzle():
    "Return a tuple (WATER, ZEBRA indicating their house numbers."
    houses = first, _, middle, _, _ = [1, 2, 3, 4, 5]
    orderings = list(itertools.permutations(houses)) # 1
    # use next to return the first feasible solution found (see more abt generator expression below)
    return next((WATER, ZEBRA)
                for (red, green, ivory, yellow, blue) in orderings
                if imright(green, ivory) # 6
                for (Englishman, Spaniard, Ukranian, Japanese, Norwegian) in orderings
                if Englishman is red  # 2
                if Norwegian is first # 10
                if nextto(Norwegian, blue) # 15
                for (coffee, tea, milk, oj, WATER) in orderings
                if coffee is green # 4
                if Ukranian is tea # 5
                if milk is middle # 9
                for (OldGold, Kools, Chesterfields, LuckyStrike, Parliaments) in orderings
                if Kools is yellow # 8
                if LuckyStrike is oj # 13
                if Japanese is Parliaments # 14
                for (dog, snails, fox, horse, ZEBRA) in orderings
                if Spaniard is dog # 3
                if OldGold is snails # 7
                if nextto(Chesterfields, fox) # 11
                if nextto(Kools, horse) # 12
                )

print zebra_puzzle()

"""
Explain about generator expression: 
a generator expression g is defined like this: g = ( term  for-clauses  options(for,ifs...) )
note that it uses parentheses instead of square brackets and to retrive the value, call: next(g)
if you ask again next(g) if will go through all the conditions and give you the second value
Ex: g = (sq(x) for x in range(10) if x%2 == 0)
"""

import time

def timedcall(fn, *args):
    "Call function with args; return the time in seconds and result."
    t0 = time.clock()
    result = fn(*args)
    t1 = time.clock()
    return t1-t0, result

def average(numbers):
    "Return the average (arithmetic mean) of a sequence of numbers."
    return sum(numbers) / float(len(numbers)) 

def timedcalls(n, fn, *args):
    """Call fn(*args) repeatedly: n times if n is an int, or up to
    n seconds if n is a float; return the min, avg, and max time"""
    # Your code here.
    if isinstance(n, int):
        times = [timedcall(fn, *args)[0] for _ in range(n)] # variable _ represents a throwaway variable
    else:
    	times = []
    	time_left = n
    	while time_left >= 0:
    		one_time = timedcall(fn, *args)[0]
    		times.append(one_time)
    		time_left -= one_time
    return min(times), average(times), max(times)

#print timedcalls(1.0, zebra_puzzle) 

#generator function
def ints(start, end = None):
    i = start
    while i <= end or end is None:
        yield i
        i = i + 1
    

def all_ints():
    "Generate integers in the order 0, +1, -1, +2, -2, +3, -3, ..."
    yield 0
    i = 1
    while True:
    	yield i
    	yield -i
    	i += 1


g = all_ints()
for i in range(10):
	print next(g)