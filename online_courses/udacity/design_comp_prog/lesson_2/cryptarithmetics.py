import string, re, itertools


# in shell: python -m cProfile script.py to get the profile

def solve(formula):
    """Given a formula like 'ODD + ODD == EVEN', fill in digits to solve it.
    Input formula is a string; output is a digit-filled-in string or None."""    
    #print next(formula_filled for formula_filled in fill_in(formula) if valid(formula_filled))
    for formula_filled in fill_in(formula):
        if valid(formula_filled):
            print formula_filled


def fill_in(formula):
    "Generate all possible fillings-in of letters in formula with digits."
    # Take all the distinct letters from formula: (can use re.findall() to achive the same result)
    letters = ''.join(set(re.sub('[^A-Z]', '', formula)))

    for digits in itertools.permutations('1234567890', len(letters)):
        table = string.maketrans(letters, ''.join(digits))
        yield formula.translate(table)

def valid(f):
    "Formula f is valid iff it has no number with leading zero and eval to True"
    try:
        # prefix 'r' stands for raw string
        # \b stands for word boundary
        return not re.search(r'\b0[0-9]',f) and eval(f) is True
    except ArithmeticError:
        return False


def compile_word(word):
    """Compile a word of uppercase letters as numeric digits.
    E.g., compile_word('YOU') => '(1*U+10*O+100*Y)'
    Non-uppercase words unchanged: compile_word('+') => '+'"""
    letters = re.findall('[A-Z]', word)
    n = len(letters)
    if n:
        result = ''.join('(' + letters[-1])
        for i in range(n - 1):
            result += '+%s*10**%d' %(letters[i] , n - 1 - i)
        result += ')'
        return result
    else:
        return word


a = re.search(r'\b0[0-9]', "0123")
b = re.search('\\b0[0-9]', '1')
c = re.search('abc', 'abcdef')
# d = re.split('[^a-zA-Z]', 'DEF23FGH15')
d = re.findall('[a-zA-Z]', 'DEF23FGH15')
e = re.sub('[^a-zA-Z]', '', 'DEF23FGH15')
f = set(e)
letters = ''.join(set(re.sub('[^A-Za-z]', '', 'DEF23FGH15')))
g = re.findall('[A-Z]', 'DEFFED')


print solve('A**N + B**N == C**N and N > 1')
print not a
print not b
print c
print d
print e
print len(f)
print letters, len(letters)
print g[-1]

print compile_word('ABC')