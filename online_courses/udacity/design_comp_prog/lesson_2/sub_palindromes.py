# --------------
# User Instructions
#
# Write a function, longest_subpalindrome_slice(text) that takes 
# a string as input and returns the i and j indices that 
# correspond to the beginning and end indices of the longest 
# palindrome in the string. 
#
# Grading Notes:
# 
# You will only be marked correct if your function runs 
# efficiently enough. We will be measuring efficency by counting
# the number of times you access each string. That count must be
# below a certain threshold to be marked correct.
#
# Please do not use regular expressions to solve this quiz!

def longest_subpalindrome_slice(text):
    "Return (i, j) such that text[i:j] is the longest palindrome in text."
    # memo will record the longest palindrome seen in that index range
    text_length = len(text)
    memo = [ [False for x in range(text_length)] for y in range(text_length)]
    max_palin_length = 0
    iBegin = 0
    for i in range(text_length):
        memo[i][i] = True # every single word is a palindrome 1
        max_palin_length = 1

        
    # palindrome length 2
    for i in range(text_length - 1):
        if text[i].lower() == text[i + 1].lower() :
            memo[i][i + 1] = True
            max_palin_length = 2
            iBegin = i

    # palindrome length >= 3: fill memo by length increasing
    for palin_length in range(3, text_length + 1):
        for i in range(text_length - palin_length + 1):
            j = i + palin_length - 1            
            if text[i].lower() == text[j].lower() and memo[i + 1][j - 1]:
                # note that memo is filled by length increasing
                memo[i][j] = True # update memo
                max_palin_length = palin_length
                iBegin = i
    return (iBegin, iBegin + max_palin_length)



def isPalindrome(text):
    "Return True if text is palindrome, False otherwise"
    text_lowercase = text.lower()
    return text_lowercase[::-1] == text_lowercase
    
def test():
    L = longest_subpalindrome_slice
    assert L('racecar') == (0, 7)
    assert L('Racecar') == (0, 7)
    assert L('RacecarX') == (0, 7)
    assert L('Race carr') == (7, 9)
    assert L('') == (0, 0)
    assert L('something rac e car going') == (8,21)
    assert L('xxxxx') == (0, 5)
    assert L('Mad am I ma dam.') == (0, 15)
    return 'tests pass'

print test()
# print longest_subpalindrome_slice('')