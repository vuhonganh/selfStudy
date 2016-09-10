# -----------------
# User Instructions
#
# In this problem, you will define a function, boggle_words(),
# that takes a board as input and returns a set of words that
# can be made from the board according to the rules of Boggle.
from copy import deepcopy


def boggle_words(board, minlength=3):
    "Find all the words on this Boggle board; return as a set of words."
    result = set()
    for idx in range(len(board)):
        boggle_from_idx(board, minlength, idx, result)

    return result


def boggle_from_idx(board, minlength, idx_start, result):
    """board is represented by a string (with borders)
    idx represent a square in board
    return: a set of words that we can form from idx"""

    if board[idx_start] in BORDER or board[idx_start] not in PREFIXES:
        return

    visited = set()
    boogle_from_idx_loop(board, minlength, idx_start, '', visited, result)

    return result


def boogle_from_idx_loop(board, minlength, idx_start, pre, visited, results):

    pre = pre + board[idx_start]
    visited.add(idx_start)

    if pre in WORDS and len(pre) >= minlength:
        results.add(pre)
    if pre in PREFIXES:  # continue only if it's a prefix
        len_board = len(board)
        size_board = size(board)
        all_idx_neighbors = [i for i in neighbors(idx_start, size_board) if 0 <= i < len_board]
        # line above is unnecessary because we don't start the process at border -> idx always in range
        for k in all_idx_neighbors:
            if board[k] not in BORDER and k not in visited:
                each_one_path = deepcopy(visited)
                boogle_from_idx_loop(board, minlength, k, pre, each_one_path, results)

    return


def boggle_word_ver2(board, minlength=3):
    """Solution of prof."""
    result = set()
    N = size(board)

    # use nested func because it's compact and not so long
    def extend_path(prefix, path):
        if prefix in WORDS and len(prefix) >= minlength:
            result.add(prefix)
        if prefix in PREFIXES:
            for j in neighbors(path[-1], N):
                if j not in path and board[j] != BORDER:  # because we don't process at border so no 'idx out of range'
                    extend_path(prefix + board[j], path + [j])

    for (i, L) in enumerate(board):
        if L != BORDER:
            extend_path(L, [i])
    return result


def test():
    b = Board('XXXX TEST XXXX XXXX')
    assert b == '|||||||XXXX||TEST||XXXX||XXXX|||||||'
    assert display(b) == """
||||||
|XXXX|
|TEST|
|XXXX|
|XXXX|
||||||""".strip()
    assert boggle_words(b) == set(['SET', 'SEX', 'TEST'])
    assert neighbors(20, 6) == (13, 14, 15, 19, 21, 25, 26, 27)
    assert len(boggle_words(Board('TPLER ORAIS METND DASEU NOWRB'))) == 317
    assert boggle_words(Board('PLAY THIS WORD GAME')) == set([
        'LID', 'SIR', 'OAR', 'LIS', 'RAG', 'SAL', 'RAM', 'RAW', 'SAY', 'RID',
        'RIA', 'THO', 'HAY', 'MAR', 'HAS', 'AYS', 'PHI', 'OIL', 'MAW', 'THIS',
        'LAY', 'RHO', 'PHT', 'PLAYS', 'ASIDE', 'ROM', 'RIDE', 'ROT', 'ROW', 'MAG',
        'THIRD', 'WOT', 'MORE', 'WOG', 'WORE', 'SAID', 'MOR', 'SAIL', 'MOW', 'MOT',
        'LAID', 'MOA', 'LAS', 'MOG', 'AGO', 'IDS', 'HAIR', 'GAME', 'REM', 'HOME',
        'RED', 'WORD', 'WHA', 'WHO', 'WHOM', 'YID', 'DRAW', 'WAG', 'SRI', 'TOW',
        'DRAG', 'YAH', 'WAR', 'MED', 'HIRE', 'TOWARDS', 'ORS', 'ALT', 'ORE', 'SIDE',
        'ALP', 'ORA', 'TWA', 'ERS', 'TOR', 'TWO', 'AIS', 'AIR', 'AIL', 'ERA', 'TOM',
        'AID', 'TOG', 'DIS', 'HIS', 'GAR', 'GAM', 'HID', 'HOG', 'PLAY', 'GOA', 'HOW',
        'HOT', 'WARM', 'GOT', 'IRE', 'GOR', 'ARS', 'ARM', 'ARE', 'TOWARD', 'THROW'])

    assert boggle_word_ver2(b) == set(['SET', 'SEX', 'TEST'])
    assert neighbors(20, 6) == (13, 14, 15, 19, 21, 25, 26, 27)
    assert len(boggle_word_ver2(Board('TPLER ORAIS METND DASEU NOWRB'))) == 317
    assert boggle_word_ver2(Board('PLAY THIS WORD GAME')) == set([
        'LID', 'SIR', 'OAR', 'LIS', 'RAG', 'SAL', 'RAM', 'RAW', 'SAY', 'RID',
        'RIA', 'THO', 'HAY', 'MAR', 'HAS', 'AYS', 'PHI', 'OIL', 'MAW', 'THIS',
        'LAY', 'RHO', 'PHT', 'PLAYS', 'ASIDE', 'ROM', 'RIDE', 'ROT', 'ROW', 'MAG',
        'THIRD', 'WOT', 'MORE', 'WOG', 'WORE', 'SAID', 'MOR', 'SAIL', 'MOW', 'MOT',
        'LAID', 'MOA', 'LAS', 'MOG', 'AGO', 'IDS', 'HAIR', 'GAME', 'REM', 'HOME',
        'RED', 'WORD', 'WHA', 'WHO', 'WHOM', 'YID', 'DRAW', 'WAG', 'SRI', 'TOW',
        'DRAG', 'YAH', 'WAR', 'MED', 'HIRE', 'TOWARDS', 'ORS', 'ALT', 'ORE', 'SIDE',
        'ALP', 'ORA', 'TWA', 'ERS', 'TOR', 'TWO', 'AIS', 'AIR', 'AIL', 'ERA', 'TOM',
        'AID', 'TOG', 'DIS', 'HIS', 'GAR', 'GAM', 'HID', 'HOG', 'PLAY', 'GOA', 'HOW',
        'HOT', 'WARM', 'GOT', 'IRE', 'GOR', 'ARS', 'ARM', 'ARE', 'TOWARD', 'THROW'])
    return 'tests pass'


def Board(text):
    """Input is a string of space-separated rows of N letters each;
    result is a string of size (N+2)**2 with borders all around."""
    rows = text.split()
    N = len(rows)
    rows = [BORDER * N] + rows + [BORDER * N]
    return ''.join(BORDER + row + BORDER for row in rows)


def size(board): return int(len(board) ** 0.5)


def neighbors(i, N):
    return (i - N - 1, i - N, i - N + 1, i - 1, i + 1, i + N - 1, i + N, i + N + 1)


BORDER = '|'


def display(board):
    "Return a string representation of board, suitable for printing."
    N = size(board)
    return '\n'.join(board[i:i + N] for i in range(0, N ** 2, N))


# ------------
# Helpful functions
#
# You may find the following functions useful. These functions
# are identical to those we defined in lecture.

def prefixes(word):
    "A list of the initial sequences of a word, not including the complete word."
    return [word[:i] for i in range(len(word))]


def readwordlist(filename):
    "Return a pair of sets: all the words in a file, and all the prefixes. (Uppercased.)"
    wordset = set(open(filename).read().upper().split())
    prefixset = set(p for word in wordset for p in prefixes(word))
    return wordset, prefixset


WORDS, PREFIXES = readwordlist('words4k.txt')

print test()
print neighbors(20, 6)
a_board = Board('XXXX TEST XXXX XXXX')
print a_board
print size(a_board)
print boggle_words(a_board) == set(['SET', 'SEX', 'TEST'])