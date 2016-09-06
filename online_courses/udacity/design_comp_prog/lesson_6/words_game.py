# -----------------
# User Instructions
#
# Write a function, readwordlist, that takes a filename as input and returns
# a set of all the words and a set of all the prefixes in that file, in
# uppercase. For testing, you can assume that you have access to a file
# called 'words4k.txt'

import time


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


def find_words(letters):
    """Return a set of words that can be formed a set of characters from input letters.
    Note that the formed word must belong to the set WORDS"""
    results = set()

    def extend_prefix(w, letters):
        if w in WORDS:
            results.add(w)
        if w not in PREFIXES: return
        for L in letters:
            extend_prefix(w + L, removed(letters, L))

    extend_prefix('', letters)
    return results


def test():
    assert len(WORDS) == 3892
    assert len(PREFIXES) == 6475
    assert 'UMIAQS' in WORDS
    assert 'MOVING' in WORDS
    assert 'UNDERSTANDIN' in PREFIXES
    assert 'ZOMB' in PREFIXES
    return 'tests pass'


print test()


def timedcall(fn, *args):
    "Call function with args; return the time in seconds and result."
    t0 = time.time()
    result = fn(*args)
    t1 = time.time()
    return t1-t0, result