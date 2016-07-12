# poker.py

def poker(hands):
	"""
	Return the best hand: poker([hand, ...]) => the max hand
	"""
	return max(hands, key=hand_rank)


def hand_rank():
	"""
	TO DO
	"""

def test():
	"Test cases for the function in poker program"
	sf = "6C 7C 8C 9C TC".split() #Straight Flush
	fk = "9D 9H 9S 9C 7D".split() #Four of a Kind
	fh = "TD TC TH 7C 7D".split() #Full House
	assert poker([sf, fk, fh]) == sf
	assert poker([fk, fh]) == fk
	assert poker([fh, fh]) == fh

	#extreme values
	assert poker([fh]) == fh #only one element
	assert poker([sf] + 99*[fk]) == sf #concatenating hand to a list 100 hands
	
	return "test pass"

print test()