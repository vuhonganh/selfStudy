"""
API		

Grammar		Example					Language			Regex
lit(s)		lit('a')				{a}					a
seq(x,y)	seq(lit('a'), lit('b'))	{ab}				ab
alt(x,y)	alt(lit('a'),lit('b'))	{a,b}				a|b
star(x)		star(lit('a'))			{'',a,aa,aaa,...}	*a
oneof(c)	oneof('abc')			{a,b,c}
eol			eol						{''}
			seq(lit('a'), eol)		{a}
dot			dot						{a,b,c,....}

eg: 'a*b+' => represent by seq(star(lit(a)), plus(lit(b)))

Remainder definition: if we want to match 'a*b+' to 'aaab'. The only possible choice is to match 'a*' to 'aaa' and 'b+' to 'b'.
So remainder is defined as: what left if we match each possible pattern to a specific part of text:

For example: 
1) match 'a*' to empty string, the remainder is 'aaab'
2) match 'a*' to 'a', the remainder is 'aab'
3) match 'a*' to 'aa', the remainder is 'ab'
4) match 'a*' to 'aaa', the remainder is 'b' (which is the correct way of matching)
This helps us to define an auxilary function called matchset(pattern, text) who will return a set of remainders.
For example, matchset('a*', 'aaab') will return ['aaab', 'aab', 'ab', 'b']
"""

null = frozenset()

def components(pattern):
	"Return the op, x, and y arguments; x and y are None if missing."
	x = pattern[1] if len(pattern) > 1 else None
	y = pattern[2] if len(pattern) > 2 else None
	return pattern[0], x, y


def matchset(pattern, text):
	"Match pattern at start of text, return a set of remainders of text"
	op, x, y = components(pattern)
	if 'lit' == op: # there is only one component x
		return set([text[len(x):]]) if text.startswith(x) else null
	elif 'dot' == op:
		return set([text[1:]]) if text else null
	elif 'oneof' == op:	# oneof takes only one component x and match each character in this component to text	
		return set([text[1:]]) if any(text.startswith(c) for c in x) else null
	elif 'eol' == op:
		return set(['']) if text == '' else null
	elif 'alt' == op:
		return matchset(x, text) | matchset(y, text) # union of two sets
	elif 'seq' == op: 
		# first we get the remainders after matching first part x to text
		# second we continue to get the final remainders after matching second part y to the remainders in first step
		return set(remain2 for remain1 in matchset(x, text) for remain2 in matchset(y, remain1))
	elif 'star' == op:
		return (set([text]) | 
				set(remain2 for remain1 in matchset(x, text) for remain2 in matchset(pattern, remain1) if remain1 != text))
	else:
		raise ValueError('unknown pattern: %s' %pattern )

# Turn these patterns into function. This is called compiler. The functions return matchset accordingly 
def lit(x): return lambda text : set([text[len(x):]]) if text.startswith(x) else null

def seq(x, y): return lambda text : set().union(*map(y, x(text)))

def alt(x, y): return lambda text : x(text) | y(text)

def oneof(chars): return lambda text : set([text[1:]]) if any(text.startswith(c) for c in chars) else null

dot = lambda text : set([text[1:]]) if text else null

eol = lambda text : set(['']) if text == '' else null

def star(x) : return lambda text : ( set([text]) | set(rem2 for rem1 in x(text) for rem2 in star(x)(rem1) if rem1  != text))


def search(pattern, text):
	"Match pattern anywhere in text; return longest earliest match or None"
	for i in range(len(text)):
		m = match(pattern, text[i:])
		if m: 
			return m
	return None

def match(pattern, text):
	"Match pattern against the start of text, return longest match or None"
	remainders = pattern(text)
	if remainders:
		shortest = min(remainders, key=len)
		return text[:(len(text) - len(shortest))]
	else:
		return None


def test():
    assert match(star(lit('a')), 'aaaaabbbaa') == 'aaaaa'
    assert match(lit('hello'), 'hello how are you?') == 'hello'
    assert match(lit('x'), 'hello how are you?') == None
    assert match(oneof('xyz'), 'x**2 + y**2 = r**2') == 'x'
    assert match(oneof('xyz'), '   x is here!') == None
    return 'tests pass'

print test()
