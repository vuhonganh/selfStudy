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

generator definition: generate all possible string from a pattern. Such as alt(a,b) will return {a,b}. We will provide
a list of numbers Ns for cases like 'star' or 'plus' to avoid having an infinite set. The return value will be a set of 
generated strings so that its length equal exactly the number in Ns. 
"""

null = frozenset()

def lit(s):         return lambda Ns: set([s]) if len(s) in Ns else null
def alt(x, y):      return lambda Ns: x(Ns) | y(Ns)
def star(x):        return lambda Ns: opt(plus(x))(Ns)
def plus(x):        return lambda Ns: genseq(x, star(x), Ns, startx=1) #Tricky
def oneof(chars):   return lambda Ns: set(chars) if 1 in Ns else null
def seq(x, y):      return lambda Ns: genseq(x, y, Ns)
def opt(x):         return alt(epsilon, x)
dot = oneof('?')    # You could expand the alphabet to more chars.
epsilon = lit('')   # The pattern that matches the empty string.

def test():
    
    f = lit('hello')
    assert f(set([1, 2, 3, 4, 5])) == set(['hello'])
    assert f(set([1, 2, 3, 4]))    == null 
    
    
    h = oneof('theseletters')
    assert h(set([1, 2, 3])) == set(['t', 'h', 'e', 's', 'l', 'r'])
    assert h(set([2, 3, 4])) == null

    g = alt(lit('hi'), lit('bye'))
    assert g(set([1, 2, 3, 4, 5, 6])) == set(['bye', 'hi'])
    assert g(set([1, 3, 5])) == set(['bye'])   
    return 'tests pass'

print test()
