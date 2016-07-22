def search(pattern, text):
	"Return True if pattern appears anywhere in text"
	if pattern.startswith('^'): # because ^x will match anything starts with x
		return match(pattern[1:], text)
	else:
		# if ^ is not the first character in pattern, then pattern can be somewhere in text
		return match('.*' + pattern, text) 

def match(pattern, text):
	"Return True if pattern appears at the start of text"
	if pattern == '':
		# an empty string pattern will always match in any text
		return True
	elif pattern == '$':
		# a text need to end by empty string meaning it's empty too
		return (text == '')
	elif len(pattern) > 1 and pattern[1] in '*?':
		# break into 3 pieces: the single character p, the mask operator op, and the rest of pattern pat
		p, op, pat = pattern[0], pattern[1], pattern[2:]
		if op == '*':
			return match_star(p, pat, text)
		elif op == '?': 
			# case ? means 1 occurrence
			if match1(p, text) and match(pat, text[1:]):
				return True
			else: # case ? means no occurrence
				return match(pat, text)

	else:
		return (match1(pattern[0], text) and match(pattern[1:], text[1:]))

def match1(p, text):
	"return True if first character of text matches pattern character p"
	if not text: return False # case text is empty
	return (p == '.' or p == text[0]) # if p is a dot it will match anything or normal case


def match_star(p, pat, text):
	"return True if any number of char p, followed by pat, matches text"
	# star can be any number of occurrence of p in text (even 0 occurrence)
	return (match(pat, text) # 0 occurrence
			or (match1(p, text) and match_star(p, pat, text[1:])))


def test():
	assert search('baa*!', 'Sheep said baaaa!')
	assert search('baa*!', 'Sheep said baaaa humbug') == False
	assert match('baa*!', 'Sheep said baaaa!') == False
	assert match('baa*!', 'baaaa! said the sheep')
	assert search('def', 'abcdefg')
	assert search('def$', 'abcdef')
	assert search('def$', 'abcdefg') == False
	assert search('^start', 'not the start') == False
	assert match('a*b*c*', 'just anything')
	assert match('x?', 'text')
	assert match('text?', 'text')
	print 'test passes'

test()