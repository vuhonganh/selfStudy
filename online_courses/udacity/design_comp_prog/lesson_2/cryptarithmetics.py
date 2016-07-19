import string, re, itertools

def solve(formula):
    """Given a formula like 'ODD + ODD == EVEN', fill in digits to solve it.
    Input formula is a string; output is a digit-filled-in string or None."""    
    return next(formula_filled for formula_filled in fill_in(formula) if valid(formula_filled))


def fill_in(formula):
	"Generate all possible fillings-in of letters in formula with digits."
	# Take all the distinct letters from formula: 
	letters = ''.join(c for c in set(re.sub('[^A-Za-z]', '', formula)))
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


a = re.search(r'\b0[0-9]', "0123")
b = re.search('\\b0[0-9]', '1')
c = re.search('abc', 'abcdef')
d = re.split('[^a-zA-Z]', 'DEF23FGH15')
e = re.sub('[^a-zA-Z]', '', 'DEF23FGH15')
f = set(e)
letters = ''.join(c for c in set(re.sub('[^A-Za-z]', '', 'DEF23FGH15')))

print solve('A+A==B')
print not a
print not b
print c
print d
print e
print len(f)
print letters, len(letters)