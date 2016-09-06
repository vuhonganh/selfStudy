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


def test():
    assert len(WORDS) == 3892
    assert len(PREFIXES) == 6475
    assert 'UMIAQS' in WORDS
    assert 'MOVING' in WORDS
    assert 'UNDERSTANDIN' in PREFIXES
    assert 'ZOMB' in PREFIXES
    assert find_words('BEEN') == {'BE', 'BEE', 'BEEN', 'BEN', 'EN', 'NE', 'NEB', 'NEE'}
    assert find_words('EEN', pre='B') == {'BE', 'BEE', 'BEEN', 'BEN'}
    return 'tests pass'
print test()