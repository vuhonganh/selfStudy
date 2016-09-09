# -----------------
# User Instructions
#
# Write a function, readwordlist, that takes a filename as input and returns
# a set of all the words and a set of all the prefixes in that file, in
# uppercase. For testing, you can assume that you have access to a file
# called 'words4k.txt'

import time


def timedcall(fn, *args):
    """Call function with args; return the time in seconds and result."""
    t0 = time.time()
    result = fn(*args)
    t1 = time.time()
    return t1-t0, result

def prefixes(word):
    """A list of the initial sequences of a word, not including the complete word."""
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
    """Return a str of letters, but with each letter in remove removed once."""
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
    """Find all word plays from hand that can be made to abut with a letter on board."""
    # Find prefix + L + suffix; L from board_letters, rest from hand
    results = set()
    for pre in find_prefixes(hand, '', set()):
        for L in board_letters:
            add_suffixes(removed(hand, pre), pre+L, results)
    return results


prev_hand, prev_results = '', set() # cache for find_prefixes


def find_prefixes(hand, pre='', results=None):
    """Find all prefixes (of words) that can be made from letters in hand."""
    if results is None:
        results = set()
    global prev_hand
    global prev_results
    if prev_hand == hand:   # already calculated
        results = prev_results.copy()
        return results

    # set up prev_hand the first time or reinitialize for a different hand (full hand)
    if prev_hand == '' or (prev_hand != hand and len(prev_hand) == len(hand)):
        prev_hand = hand
        prev_results.clear()

    if pre in PREFIXES:
        results.add(pre)
        for L in hand:
            find_prefixes(hand.replace(L, '', 1), pre+L, results)

    if hand == prev_hand:
        prev_results |= results  # update new result

    return results


def find_prefixes_old(hand, pre='', results=None):
    """Find all prefixes (of words) that can be made from letters in hand."""
    if results is None:
        results = set()
    if pre in PREFIXES:
        results.add(pre)
        for L in hand:
            find_prefixes_old(hand.replace(L, '', 1), pre+L, results)
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
    """Return all word plays, longest first."""
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


class Anchor(set):
    """An Anchor is where a new word can be placed; has a set of allowable letters
    The rule is we can only put a new letter next to a letter which was already on the board"""


LETTERS = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')    # turn this string to a list of letters
ANY = Anchor(LETTERS)   # the Anchor that can be any letter


def row_plays(hand, row):
    """Return a set of legal plays in a row. A row play is an (start, 'WORD') pair
    Note that a row is added 2 borders element | at each side"""
    result = set()
    # To each allowable prefix, add all suffixes, keeping words
    # Note that we can only put new letter in an anchor (adjacent square to existing letters on the board)
    for (idx, square) in enumerate(row[1:-1], 1):
        if isinstance(square, Anchor):
            pre, maxsize = legal_prefixes(idx, row)
            if pre:  # pre is already on the board
                start = idx - len(pre)
                add_suffixes_in_row(hand, pre, start, row, result, anchored=False)
            else:  # the left of the anchor is empty
                for pre in find_prefixes(hand):
                    if len(pre) <= maxsize:
                        start = idx - len(pre)
                        add_suffixes_in_row(removed(hand, pre), pre, start, row, result, anchored=False)
    return result


def legal_prefixes(idx_anchor, row):
    """Return a tuple (pre, maxsize) that represents the prefix and its maxsize
    based on the current row and position of the anchor"""
    start = idx_anchor
    pre = ''
    while row[start - 1] in LETTERS:
        start -= 1
        pre = row[start] + pre
    if pre == '':   # while cond. above is not satisfied
        while is_empty(row[start - 1]) and not isinstance(row[start - 1], Anchor):
            start -= 1
    return (pre, idx_anchor - start)


def add_suffixes_in_row(hand, pre, start, row, result, anchored=True):
    """Add all possible suffixes, and accumulate (start, word) in result
    anchored: will be set to False in the first call to avoid adding already existing letters on the board"""
    i = start + len(pre)    # the position of the right square after fill start by pre
    right_square = row[i]
    if pre in WORDS and anchored and not is_letters(right_square):  # if this is a letter, this forms a different word
        result.add((start, pre))
    if pre in PREFIXES:
        if is_letters(right_square):
            add_suffixes_in_row(hand, pre + right_square, start, row, result)
        elif is_empty(right_square):
            # distinct Anchor square and '.' square
            possibilities = right_square if isinstance(right_square, Anchor) else ANY
            for L in hand:
                if L in possibilities:
                    add_suffixes_in_row(hand.replace(L, '', 1), pre + L, start, row, result)

    return result


def a_board():
    return map(list, ['|||||||||||||||||',
                      '|J............I.|',
                      '|A.....BE.C...D.|',
                      '|GUY....F.H...L.|',
                      '|||||||||||||||||'])


def a_board_mini():
    return map(list, ['|||||||||||||||||',
                      '|A.....BE.C...D.|',
                      '|GUY....F.H...L.|',
                      '|||||||||||||||||'])

def show(board):
    "Print the board."
    # for line in board:
    #     for elem in line:
    #         print elem,
    #     print
    for i in range(len(board)):
        for j in range(len(board[0])):
            if is_letters(board[i][j]) or board[i][j] == '|':
                print board[i][j],
            else:
                print BONUS[i][j],
        print


def transpose(matrix):
    return map(list, zip(*matrix))


def horizontal_plays(hand, board):
    "Find all horizontal plays -- ((i, j), word) pairs -- across all rows."
    results = set()
    for (i, row) in enumerate(board[1:-1], 1):
        set_anchors(row, i, board)
        for (j, word) in row_plays(hand, row):
            score = calculate_score(board, (i, j), ACROSS, word)
            results.add((score, (i, j), word))

    return results


def neighbors(board, i, j):
    """Return a list of the contents of the four neighboring squares,
    in the order N,S,E,W."""
    return [board[i - 1][j], board[i + 1][j],
            board[i][j + 1], board[i][j - 1]]


def set_anchors(row, i, board):
    """Anchors are empty squares with a neighboring letter. Some are restricted
    by cross-words to be only a subset of letters.
    set all anchors on row i of the board"""
    # find neighbors of every square in row_i
    for (j, square) in enumerate(row[1:-1], 1):
        neighbors_list = neighbors(board, i, j)
        N = neighbors_list[0]  # north neighbor and south neighbor will be treated differently
        S = neighbors_list[1]
        # Anchors are either squares adjacent to a letter or a '*' square.
        if square == '*' or (is_empty(square) and any(map(is_letters, neighbors_list))):
            if is_letters(N) or is_letters(S):
                (_, w) = find_cross_word(board, i, j)  # find letters that fit  with the cross word (vertical word)
                # w will have form '[alphabet]* . [alphabet]*'
                row[j] = Anchor(L for L in LETTERS if w.replace('.', L) in WORDS)
            else:  # unrestricted empty square: any letter will fit
                row[j] = ANY
    return None


def find_cross_word(board, i, j):
    """Find the vertical word that crosses board[i][j]. Return (i2, w),
    where i2 is the starting row, and w is the word"""
    sq = board[i][j]
    w = sq if is_letters(sq) else '.'
    # find the upper part
    for i2 in range(i, 0, -1):
        sq2 = board[i2-1][j]
        if is_letters(sq2):
            w = sq2 + w
        else:
            break
    # find the lower part
    for i3 in range(i+1, len(board)):
        sq3 = board[i3][j]
        if is_letters(sq3):
            w = w + sq3
        else:
            break
    return i2, w


DOWN, ACROSS = (1, 0), (0, 1) # Directions that words can go

def bonus_template(quadrant):
    """Make a board from the upper-left quadrant.
    A quadrant will be represented by multiple line text.
    When call .split() it will be list of line
    when call map(mirror, quadrant.split()) : it mirror each elem i.e. reflect each line
    now call mirror on the previous result (a list of reflected lines): it will reflect these lines by the mid-line"""
    return mirror(map(mirror, quadrant.split()))

def mirror(sequence): return sequence + sequence[-2::-1]

seq_test = """
|||||||||
|3..:...3
"""
print seq_test.split()
print map(mirror, seq_test.split())
print mirror(map(mirror, seq_test.split()))
SCRABBLE = bonus_template("""
|||||||||
|3..:...3
|.2...;..
|..2...:.
|:..2...:
|....2...
|.;...;..
|..:...:.
|3..:...*
""")

WWF = bonus_template("""
|||||||||
|...3..;.
|..:..2..
|.:..:...
|3..;...2
|..:...:.
|.2...;..
|;...:...
|...2...*
""")

BONUS = WWF
DW, TW, DL, TL = '23:;'


def all_plays(hand, board):
    """All plays in both directions. A play is a (score, pos, dir, word) tuple,
    where pos is an (i, j) pair, and dir is ACROSS or DOWN."""
    hplays = horizontal_plays(hand, board)            # set of ((i, j), word)
    vplays = horizontal_plays(hand, transpose(board)) # set of ((j, i), word)
    results = set()
    for (score, pos, word) in hplays:
        results.add((score, (pos[0], pos[1]), ACROSS, word))
    for (score, pos, word) in vplays:
        results.add((score, (pos[1], pos[0]), DOWN, word))
    return results


def calculate_score(board, pos, direction, word):
    """Given a board, a position on board, a direction of the word we want to place"""
    total, cross_total, word_mult = 0, 0, 1
    start_i, start_j = pos
    di, dj = direction
    other_direction = DOWN if direction == ACROSS else ACROSS
    for (n, L) in enumerate(word):
        i, j = start_i + n * di, start_j + n * dj

        square = board[i][j]
        bonus = BONUS[i][j]
        # the bonus can only get once (i.e. square is empty)
        word_mult *= (1 if is_letters(square) else
                      2 if bonus in (DW, '*') else
                      3 if bonus == TW else 1)
        letter_mult = (1 if is_letters(square) else
                       2 if bonus == DL else
                       3 if bonus == TL else 1)


        total += POINTS[L] * letter_mult

        # direction is not DOWN: to avoid infinite loop (only search for cross (vertical) word)
        if isinstance(square, Anchor) and square is not ANY and direction is not DOWN:
            cross_total += cross_word_score(board, L, (i, j), other_direction)
    return cross_total + total * word_mult


def cross_word_score(board, L, pos, direction):
    i, j = pos
    i2, word = find_cross_word(board, i, j)
    # this word contain a ., need to replace it
    return calculate_score(board, (i2, j), direction, word.replace('.', L))


def is_letters(square):
    """Return whether a square on the board is letter"""
    return square in LETTERS


def is_empty(square):
    """Return whether a square on the board is empty (but not border)"""
    return square == '.' or square == '*' or isinstance(square, Anchor)


def make_play(play, board):
    """Put the word down on the board."""
    (score, pos, direction, word) = play
    (i, j) = pos
    (di, dj) = direction
    for k in range(len(word)):
        board[i][j] = word[k]
        i += di
        j += dj
    return board


NOPLAY = None


def best_play(hand, board):
    """Return the highest-scoring play.  Or None."""
    plays = all_plays(hand, board)
    return sorted(plays)[-1] if plays else NOPLAY


def show_best(hand, board):
    best = best_play(hand, board)
    if not best:
        print 'No legal plays.'
        return
    print 'Current board is:'
    show(board)
    print 'New word %s scores %d' %(best[-1], best[0])
    make_play(best, board)
    show(board)


def test():
    assert len(WORDS) == 3892
    assert len(PREFIXES) == 6475
    assert 'UMIAQS' in WORDS
    assert 'MOVING' in WORDS
    assert 'UNDERSTANDIN' in PREFIXES
    assert 'ZOMB' in PREFIXES
    assert find_words('BEEN') == {'BE', 'BEE', 'BEEN', 'BEN', 'EN', 'NE', 'NEB', 'NEE'}
    assert find_words('EEN', pre='B') == {'BE', 'BEE', 'BEEN', 'BEN'}
    assert (
    {'DIE', 'ATE', 'READ', 'AIT', 'DE', 'IDEA', 'RET', 'QUID', 'DATE', 'RATE', 'ETA', 'QUIET', 'ERA', 'TIE', 'DEAR',
     'AID', 'TRADE', 'TRUE', 'DEE', 'RED', 'RAD', 'TAR', 'TAE', 'TEAR', 'TEA', 'TED', 'TEE', 'QUITE', 'RE', 'RAT',
     'QUADRATE', 'EAR', 'EAU', 'EAT', 'QAID', 'URD', 'DUI', 'DIT', 'AE', 'AI', 'ED', 'TI', 'IT', 'DUE', 'AQUAE', 'AR',
     'ET', 'ID', 'ER', 'QUIT', 'ART', 'AREA', 'EQUID', 'RUE', 'TUI', 'ARE', 'QI', 'ADEQUATE', 'RUT'} == word_plays('ADEQUAT', set('IRE')))
    # an example of row: (| means the border - not a square)
    # | A.....BE.C...D. |   # after A, first square can only be 'MNX', and second square 'MOAB'
    # | GUY....F.H...L. |   # because it needs to form a word in vertical dir: with U (1st square) and Y (2nd square)
    mnx = Anchor('MNX')
    moab = Anchor('MOAB')
    a_row = ['|', 'A', mnx, moab, '.', '.', ANY, 'B', 'E', ANY, 'C', ANY, '.', ANY, 'D', ANY, '|']
    a_hand = 'ABCEHKN'
    assert find_prefixes('JEBW', 'Z') == set(['Z', 'ZE', 'ZEB', 'ZW'])
    show_best(a_hand, a_board())
    return 'tests pass'


print test()

def test_speed():
    print sum([timedcall(find_prefixes, 'JEBWKAN', '')[0] for i in range(15)])
    print sum([timedcall(find_prefixes_old, 'JEBWKAN', '')[0] for i in range(15)])