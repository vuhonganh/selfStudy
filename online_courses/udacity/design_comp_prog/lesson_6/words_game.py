# -----------------
# User Instructions
#
# Write a function, readwordlist, that takes a filename as input and returns
# a set of all the words and a set of all the prefixes in that file, in
# uppercase. For testing, you can assume that you have access to a file
# called 'words4k.txt'

import time


def timedcall(fn, *args):
    "Call function with args; return the time in seconds and result."
    t0 = time.time()
    result = fn(*args)
    t1 = time.time()
    return t1-t0, result

def prefixes(word):
    "A list of the initial sequences of a word, not including the complete word."
    return [word[:i] for i in range(1, len(word))]


def readwordlist(filename):
    """Read the words from a file and return a set of the words
    and a set of the prefixes in UPPERCASE."""
    file = open(filename)  # opens file
    text = file.read().upper()  # gets file into string upper
    wordset = set(text.split())
    prefixset = set(p for word in wordset for p in prefixes(word))
    prefixset.add('')  # add empty string to prefix set
    return wordset, prefixset


WORDS, PREFIXES = readwordlist('words4k.txt')


def removed(letters, remove):
    "Return a str of letters, but with each letter in remove removed once."
    for L in remove:
        letters = letters.replace(L, '', 1)
    return letters


def find_words(letters, pre='', results=None):
    """Return a set of words that can be formed by a subset of characters from input letters.
    Note that the formed word must belong to the set WORDS"""
    if results is None:
        results = set()
    if pre in WORDS:
        results.add(pre)
    if pre in PREFIXES:  # only continue if pre in PREFIXES
        for L in letters:
            find_words(letters.replace(L, '', 1), pre + L, results)
    return results


def word_plays(hand, board_letters):
    "Find all word plays from hand that can be made to abut with a letter on board."
    # Find prefix + L + suffix; L from board_letters, rest from hand
    results = set()
    for pre in find_prefixes(hand, '', set()):
        for L in board_letters:
            add_suffixes(removed(hand, pre), pre+L, results)
    return results


def find_prefixes(hand, pre='', results=None):
    "Find all prefixes (of words) that can be made from letters in hand."
    if results is None:
        results = set()
    if pre in PREFIXES:
        results.add(pre)
        for L in hand:
            find_prefixes(hand.replace(L, '', 1), pre+L, results)
    return results


def add_suffixes(hand, pre, results):
    """Return the set of words that can be formed by extending pre with letters in hand."""
    if results is None:
        results = set()
    if pre in WORDS:  # if pre is already a word: add it
        results.add(pre)
    if pre in PREFIXES:  # if pre is a prefix: continue the loop
        for L in hand:
            add_suffixes(hand.replace(L, '', 1), pre + L, results)
    return results


def longest_words(hand, board_letters):
    "Return all word plays, longest first."
    # The line of code below will return None because list.sort() is an in-place function (i.e. procedure).
    # It returns NOTHING. That's why we need to assign a list explicitly
    # return list(word_plays(hand, board_letters)).sort(key=len, reverse=True)
    # explicit_list_words = list(word_plays(hand, board_letters))
    # explicit_list_words.sort(key=len, reverse=True)
    # return explicit_list_words  # NOTE to return the list itself, not the result of a function list.sort

    # ALTERNATIVE
    return sorted(word_plays(hand, board_letters), key=len, reverse=True)


POINTS = dict(A=1, B=3, C=3, D=2, E=1, F=4, G=2, H=4, I=1, J=8, K=5, L=1, M=3, N=1, O=1, P=3, Q=10, R=1, S=1, T=1, U=1, V=4, W=4, X=8, Y=4, Z=10, _=0)

def word_score(word):
    """The sum of the individual letter point scores for this word."""
    return sum(POINTS[L] for L in word)


def topn(hand, board_letters, n=10):
    """Return a list of the top n words that hand can play, sorted by word score."""
    return sorted(word_plays(hand, board_letters), key=word_score, reverse=True)[:n]


def test():
    assert len(WORDS) == 3892
    assert len(PREFIXES) == 6475
    assert 'UMIAQS' in WORDS
    assert 'MOVING' in WORDS
    assert 'UNDERSTANDIN' in PREFIXES
    assert 'ZOMB' in PREFIXES
    assert find_words('BEEN') == {'BE', 'BEE', 'BEEN', 'BEN', 'EN', 'NE', 'NEB', 'NEE'}
    assert find_words('EEN', pre='B') == {'BE', 'BEE', 'BEEN', 'BEN'}
    assert (word_plays('ADEQUAT', set('IRE')) ==
            set(['DIE', 'ATE', 'READ', 'AIT', 'DE', 'IDEA', 'RET', 'QUID', 'DATE', 'RATE',
                 'ETA', 'QUIET', 'ERA', 'TIE', 'DEAR', 'AID', 'TRADE', 'TRUE', 'DEE',
                 'RED', 'RAD', 'TAR', 'TAE', 'TEAR', 'TEA', 'TED', 'TEE', 'QUITE', 'RE',
                 'RAT', 'QUADRATE', 'EAR', 'EAU', 'EAT', 'QAID', 'URD', 'DUI', 'DIT', 'AE',
                 'AI', 'ED', 'TI', 'IT', 'DUE', 'AQUAE', 'AR', 'ET', 'ID', 'ER', 'QUIT',
                 'ART', 'AREA', 'EQUID', 'RUE', 'TUI', 'ARE', 'QI', 'ADEQUATE', 'RUT']))
    # print longest_words('ADEQUAT', set('IRE'))
    return 'tests pass'
print test()