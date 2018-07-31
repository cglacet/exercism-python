from collections import Counter
from string import ascii_lowercase

def is_pangram(sentence):
    letter_count = Counter(sentence.lower())
    for c in ascii_lowercase:
        if letter_count[c] < 1:
            return False
    return True
