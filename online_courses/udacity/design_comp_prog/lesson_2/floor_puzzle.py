#------------------
# User Instructions
#
# Hopper, Kay, Liskov, Perlis, and Ritchie live on 
# different floors of a five-floor apartment building. 
#
# Hopper does not live on the top floor. 
# Kay does not live on the bottom floor. 
# Liskov does not live on either the top or the bottom floor. 
# Perlis lives on a higher floor than does Kay. 
# Ritchie does not live on a floor adjacent to Liskov's. 
# Liskov does not live on a floor adjacent to Kay's. 
# 
# Where does everyone live?  
# 
# Write a function floor_puzzle() that returns a list of
# five floor numbers denoting the floor of Hopper, Kay, 
# Liskov, Perlis, and Ritchie.

import itertools

floors = bottom, _ , _ , _ , top = [1, 2, 3, 4, 5]

orderings = list(itertools.permutations(floors))


def not_adjacent(fa, fb):
	return abs(fa - fb) > 1

def floor_puzzle():
    for (Hopper, Kay, Liskov, Perlis, Ritchie) in orderings:
    	if Hopper != top:
    		if Kay != bottom:
    			if Liskov != top and Liskov != bottom:
    				if Perlis > Kay:
    					if not_adjacent(Ritchie, Liskov):
    						if not_adjacent(Liskov, Kay):
    							return [Hopper, Kay, Liskov, Perlis, Ritchie]

print floor_puzzle()