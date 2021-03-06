# This homework deals with anagrams. An anagram is a rearrangement
# of the letters in a word to form one or more new words.
#
# Your job is to write a function anagrams(), which takes as input
# a phrase and an optional argument, shortest, which is an integer
# that specifies the shortest acceptable word. Your function should
# return a set of all the possible combinations of anagrams.
#
# Your function should not return every permutation of a multi word
# anagram: only the permutation where the words are in alphabetical
# order. For example, for the input string 'ANAGRAMS' the set that
# your function returns should include 'AN ARM SAG', but should NOT
# include 'ARM SAG AN', or 'SAG AN ARM', etc...


def anagrams_ver2(phrase, shortest=2):
    """better version: shorter and more efficient"""
    return find_anagrams_ver2(phrase.replace(' ', ''), '', shortest)


def find_anagrams_ver2(letters, previous_word, shortest):
    """Using letters, form anagrams using words > previous_word and not shorter than shortest"""
    result = set()
    for w in find_words_ver2(letters):
        if len(w) >= shortest and w >= previous_word:
            remainder = removed(letters, w)
            if remainder:
                for rest in find_anagrams_ver2(remainder, w, shortest):
                    result.add(w + ' ' + rest)
            else:
                result.add(w)
    return result


def find_words_ver2(letters):
    return extend_prefix_ver2('', letters, set())


def extend_prefix_ver2(pre, letters, results):
    if pre in WORDS:
        results.add(pre)
    if pre in PREFIXES:
        for L in letters:
            extend_prefix_ver2(pre + L, letters.replace(L, '', 1), results)
    return results


def anagrams(phrase, shortest=2):
    """Return a set of phrases with words from WORDS that form anagram
    of phrase. Spaces can be anywhere in phrase or anagram. All words
    have length >= shortest. Phrases in answer must have words in
    lexicographic order (not all permutations)."""
    # first need to remove space in phrase for easy processing later:
    phrase_no_space = phrase.replace(' ', '')

    # case where are several words form an anagram
    result_in_tuple = set()
    find_anagrams(phrase_no_space, shortest, result_in_tuple)
    result = set()
    for elem in result_in_tuple:
        s = ' '.join(w for w in elem)
        result.add(s)

    # case where a whole word form an anagram
    whole_words = find_words(phrase_no_space, len(phrase_no_space))
    for s in whole_words:
        if s != phrase_no_space:
            result.add(s)

    return result


def find_anagrams(letters, shortest, results):
    """return a set of anagrams with all words longer than shortest"""
    if len(letters) < shortest:
        return

    part_1 = find_words(letters, shortest)  # part_1 is the possible first words in results anagrams
    for word in part_1:
        subtracted_letters = removed(letters, word)
        the_rest = find_words(subtracted_letters, len(subtracted_letters))  # find exact the rest which forms a word
        for word2 in the_rest:
            cur_anagram = (word, word2) if word < word2 else (word2, word)
            results.add(cur_anagram)
        subset = set()
        find_anagrams(subtracted_letters, shortest, subset)
        for _, elem in enumerate(subset):
            another_anagram = ((word, elem[0], elem[1]) if word < elem[0] else
                               (elem[0], word, elem[1]) if word < elem[1] else
                               (elem[0], elem[1], word))

            results.add(another_anagram)
    return


# ------------
# Helpful functions
#
# You may find the following functions useful. These functions
# are identical to those we defined in lecture.
def removed(letters, remove):
    """Return a str of letters, but with each letter in remove removed once."""
    for L in remove:
        letters = letters.replace(L, '', 1)
    return letters


def find_words(letters, shortest):
    """return a set of words in WORDS that is composed from a sub set of these letters
    min length of word is shortest"""
    if len(letters) < shortest:
        return None
    return sorted(extend_prefix('', letters, shortest, set()))


def extend_prefix(pre, letters, shortest, results):
    """Helper function of find_words()"""
    if pre in WORDS and len(pre) >= shortest:
        results.add(pre)
    if pre in PREFIXES:
        for L in letters:
            extend_prefix(pre + L, letters.replace(L, '', 1), shortest, results)

    return results


def prefixes(word):
    """A list of the initial sequences of a word, not including the complete word."""
    return [word[:i] for i in range(len(word))]


def readwordlist(filename):
    """Return a pair of sets: all the words in a file, and all the prefixes. (Uppercased.)"""
    wordset = set(open(filename).read().upper().split())
    prefixset = set(p for word in wordset for p in prefixes(word))
    return wordset, prefixset


WORDS, PREFIXES = readwordlist('words4k.txt')


# ------------
# Testing
#
# Run the function test() to see if your function behaves as expected.

def test():
    print 'File: anagrams.py'
    assert 'DOCTOR WHO' in anagrams('TORCHWOOD')
    assert 'BOOK SEC TRY' in anagrams('OCTOBER SKY')
    assert 'SEE THEY' in anagrams('THE EYES')
    assert 'LIVES' in anagrams('ELVIS')
    assert anagrams('PYTHONIC') == {'NTH PIC YO', 'NTH OY PIC', 'ON PIC THY', 'NO PIC THY', 'COY IN PHT', 'ICY NO PHT',
                                    'ICY ON PHT', 'ICY NTH OP', 'COP IN THY', 'HYP ON TIC', 'CON PI THY', 'HYP NO TIC',
                                    'COY NTH PI', 'CON HYP IT', 'COT HYP IN', 'CON HYP TI'}

    assert 'DOCTOR WHO' in anagrams_ver2('TORCHWOOD')
    assert 'BOOK SEC TRY' in anagrams_ver2('OCTOBER SKY')
    assert 'SEE THEY' in anagrams_ver2('THE EYES')
    assert 'LIVES' in anagrams_ver2('ELVIS')
    assert anagrams_ver2('PYTHONIC') == {'NTH PIC YO', 'NTH OY PIC', 'ON PIC THY', 'NO PIC THY', 'COY IN PHT', 'ICY NO PHT',
                                    'ICY ON PHT', 'ICY NTH OP', 'COP IN THY', 'HYP ON TIC', 'CON PI THY', 'HYP NO TIC',
                                    'COY NTH PI', 'CON HYP IT', 'COT HYP IN', 'CON HYP TI'}

    return 'tests pass'


print test()
