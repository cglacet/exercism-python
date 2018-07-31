from collections import defaultdict

def detect_anagrams(word, candidates):
    word_char_count = char_count(word)
    return [ c for c in candidates if is_anagram(c, word, word_char_count) ]

def is_anagram(test_word, ref_word, ref_char_count):
    if len(test_word) != len(ref_word):
        return False
    if (test_word.lower() == ref_word.lower()):
        return False
    return same_char_count(test_word, ref_char_count)

def same_char_count(test_word, ref_char_count):
    count = defaultdict(int)
    for char in test_word.lower():
        count[char] += 1
        if count[char] > ref_char_count[char]:
            return False
    for k in ref_char_count.keys():
        if ref_char_count[k] != ref_char_count[k]:
            return False
    return True

def char_count(word):
    count = defaultdict(int)
    for char in word.lower():
        count[char] += 1
    return count
