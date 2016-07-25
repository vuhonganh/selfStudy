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

def matchset(pattern, text):
	"Match pattern at start of text, return a set of remainders of text"
	op, x, y = components(pattern)
	if 'lit' == op: # there is only one component x
		return set([text[len(x):]]) if text.startswith(x) else null
	elif 'dot' == op:
		return set([text[1:]]) if text else null
	elif 'oneof' == op:
		if not text: return null
		else: 
			for p in set(pattern):
				if text.startswith(p):
					return set([text[1:]])  
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




def components(pattern):
    "Return the op, x, and y arguments; x and y are None if missing."
    x = pattern[1] if len(pattern) > 1 else None
    y = pattern[2] if len(pattern) > 2 else None
    return pattern[0], x, y


def test():
    assert matchset(('lit', 'abc'), 'abcdef')            == set(['def'])
    assert matchset(('seq', ('lit', 'hi '),
                     ('lit', 'there ')), 
                   'hi there nice to meet you')          == set(['nice to meet you'])
    assert matchset(('alt', ('lit', 'dog'), 
                    ('lit', 'cat')), 'dog and cat')      == set([' and cat'])
    assert matchset(('dot',), 'am i missing something?') == set(['m i missing something?'])
    assert matchset(('oneof', 'a'), 'aabc123')           == set(['abc123'])
    assert matchset(('eol',),'')                         == set([''])
    assert matchset(('eol',),'not end of line')          == frozenset([])
    assert matchset(('star', ('lit', 'hey')), 'heyhey!') == set(['!', 'heyhey!', 'hey!'])
    
    return 'tests pass'

print test()

