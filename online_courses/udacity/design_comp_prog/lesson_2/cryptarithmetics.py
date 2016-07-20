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


def compile_word_ver2(word):
    """Compile a word of uppercase letters as numeric digits.
    E.g., compile_word('YOU') => '(1*U+10*O+100*Y)'
    Non-uppercase words unchanged: compile_word('+') => '+'"""
    # reverse a word: word[::-1]
    # extract a word into (index_character, correspond_character): use enumerate
    if word.isupper():
        term = [ ('%d*%s' % (10**i, d)) for (i, d) in enumerate(word[::-1])]        
        # note the way we use string.join()
        result = '(' + '+'.join(term) + ')'        
        return result
    else:
        return word

def compile_formula(formula, verbose=False):
    """Compile formula into a function. Also return letters found
    as a str, in same order as parameters of function. The first digit of a multi-digit number
    can not be 0.
    Ex: 'YOU == ME ** 2' returns
    (lambda Y,M,E,U,O: (U + 10*O + 100*Y)  == (E + 10*M)**2), 'YMEUO' """
    # all letters in the formula:
    letters = ''.join(set(re.findall('[A-Z]', formula)))
    # extract words in the formula: NOTE that the parentheses are IMPORTANT (it keeps the delimiters)
    words = re.split('([A-Z]+)', formula)
    tokens = map(compile_word, words)
    
    parameters = ','.join(letters)
    body = ''.join(tokens)

    f = 'lambda %s : %s' %(parameters, body)
    if verbose: print f

    # f is a string, to make it a function, need to do eval(f)
    return eval(f), letters
    

def solve_faster_ver(formula):
    """Given a formula like 'ODD + ODD == EVEN', fill in digits to solve it.
    Input formula is a string; output is a digit-filled-in string or None.
    This version precompiles the formula so it uses eval() only once per formula"""
    func, letters = compile_formula(formula, True)
    for digits in itertools.permutations((1,2,3,4,5,6,7,8,9,0), len(letters)):
        try:
            if func(*digits) is True:
                # map(str, digits) is important to map each int in the array digits to string, then we can use string.join()
                table = string.maketrans(letters, ''.join(map(str,digits))) 
                return formula.translate(table)
        except ArithmeticError:
            pass 


def test():
    assert faster_solve('A + B == BA') == None # should NOT return '1 + 0 == 01'
    assert faster_solve('YOU == ME**2') == ('289 == 17**2' or '576 == 24**2' or '841 == 29**2')
    assert faster_solve('X / X == X') == '1 / 1 == 1'
    return 'tests pass'
test()