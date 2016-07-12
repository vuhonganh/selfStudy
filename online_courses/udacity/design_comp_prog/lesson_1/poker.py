# poker.py

# hand: representing cards (5 best cards) of a player in a round
# rank: the number(s) of a card, or a tuple of values of a hand


def poker(hands):
	"""
	Return the best hand: poker([hand, ...]) => the max hand
	"""
	return max(hands, key=hand_rank)


def hand_rank(hand):
	"""
	Given a hand, return its rank in form of a tuple to break ties
	"""	
    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand):            # straight flush
        return (8, max(ranks))
    elif kind(4, ranks):                           # 4 of a kind
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):        # full house
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):                              # flush: same suit -> need all cards to break tie
        return (5, ranks)
    elif straight(ranks):                          # straight: consecutive sequences
        return (4, max(ranks))						
    elif kind(3, ranks):                           # 3 of a kind
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks):                          # 2 pair
        return (2, two_pair(ranks), ranks)
    elif kind(2, ranks):                           # kind
        return (1, kind(2, ranks), ranks)
    else:                                          # high card
        return (0, ranks)

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
	
	#test hand_rank
	assert hand_rank(sf) == (8, 10)
    assert hand_rank(fk) == (7, 9, 7)
    assert hand_rank(fh) == (6, 10, 7)

    #test card_ranks
    assert card_ranks(sf) == [10, 9, 8, 7, 6]
    assert card_ranks(fk) == [9, 9, 9, 9, 7]
    assert card_ranks(fh) == [10, 10, 10, 7, 7]
	return "test pass"

print test()