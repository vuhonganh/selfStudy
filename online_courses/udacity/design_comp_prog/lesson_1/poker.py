# poker.py

# hand: representing cards (5 best cards) of a player in a round
# rank: the number(s) of a card, or a tuple of values of a hand


def poker(hands):
    """
    Return a list of winning hand(s): poker([hand, ...]) => [max_hand_1, ...]
    """
    return allmax(hands, key=hand_rank)

def allmax(iterable, key=None):
    "Return a list of all items equal to the max of the iterable" 
    max_list, max_elem = [], None
    # tetmplate style
    key = key or (lambda x:x) 
    max_elem = max(iterable, key=key)
    for elem in iterable:
        if key(max_elem) == key(elem):
            max_list.append(elem)
    return max_list

def card_ranks(hand):
    "Return a list of the ranks, sorted with higher first."
    ranks = ["--23456789TJQKA".index(r) for r,s in hand]
    ranks.sort(reverse=True)
    if ranks == [14, 5, 4, 3, 2]:
        return [5, 4, 3, 2, 1]
    else:
        return ranks

def straight(ranks):
    "Return True if the ordered ranks form a 5-card straight."
    high = max(ranks)
    return ranks == [high, high - 1, high - 2, high - 3, high - 4]    


def flush(hand):
    "Return True if all the cards have the same suit."
    suits = [s for r,s in hand]
    for i in range(len(suits) - 1):
        if suits[-1] != suits[i]:
            return False
    return True

def kind_ver1(n, ranks):
    """Return the first rank that this hand has exactly n of.
    Return None if there is no n-of-a-kind in the hand."""
    nb_occur = [0 for r in ranks]
    courser = 0
    posi = 0
    for i in range(len(ranks)):
        if ranks[courser] != ranks[i]:
            courser += 1
        nb_occur[courser] += 1
    for i in range(len(nb_occur)):
        posi += nb_occur[i]
        if nb_occur[i] == n :
            return ranks[posi - 1]
    return None

def kind(n, ranks):
    """Return the first rank that this hand has exactly n of.
    Return None if there is no n-of-a-kind in the hand."""
    for r in ranks:
        if ranks.count(r) == n: return r
    return None

def two_pair(ranks):
    """If there are two pair, return the two ranks as a
    tuple: (highest, lowest); otherwise return None."""
    highest = 0
    lowest  = 0
    for r in set(ranks):
        if ranks.count(r) == 2:
            if highest == 0: 
                highest = r
            else: 
                lowest = r
    if highest != 0 and lowest != 0:
        return (highest, lowest)
    else:
        return None


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
    # "Test cases for the function in poker program"
    sf = "6C 7C 8C 9C TC".split() #Straight Flush
    fk = "9D 9H 9S 9C 7D".split() #Four of a Kind
    fh = "TD TC TH 7C 7D".split() #Full House
    assert poker([sf, fk, fh]) == [sf]
    assert poker([fk, fh]) == [fk]
    assert poker([fh, fh]) == [fh, fh]

    #extreme values
    assert poker([fh]) == [fh] #only one element
    assert poker([sf] + 99*[fk]) == [sf] #concatenating hand to a list 100 hands
    
    #test hand_rank
    assert hand_rank(sf) == (8, 10)
    assert hand_rank(fk) == (7, 9, 7)
    assert hand_rank(fh) == (6, 10, 7)

    #test card_ranks
    assert card_ranks(sf) == [10, 9, 8, 7, 6]
    assert card_ranks(fk) == [9, 9, 9, 9, 7]
    assert card_ranks(fh) == [10, 10, 10, 7, 7]

    assert card_ranks(['AC', '3D', '4S', 'KH']) == [14, 13, 4, 3]

    tp = "5S 5D 9H 9C 6S".split() # Two pairs
    fkranks = card_ranks(fk)
    tpranks = card_ranks(tp)
    assert kind(4, fkranks) == 9
    assert kind(3, fkranks) == None
    assert kind(2, fkranks) == None
    assert kind(1, fkranks) == 7
    assert two_pair(tpranks) == (9, 5)

    sf1 = "6C 7C 8C 9C TC".split() # Straight Flush
    sf2 = "6D 7D 8D 9D TD".split() # Straight Flush

    assert poker([sf1, sf2, fk, fh]) == [sf1, sf2] 

    return "test pass"

print test()