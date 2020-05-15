from collections import Counter


def detect_anagrams(word, candidates):
	return [w for w in candidates if are_anagrams(word, w)]


def are_anagrams(word_a, word_b):
    word_a = word_a.lower()
    word_b = word_b.lower()
    if word_a == word_b:
        return False
    return Counter(word_a) == Counter(word_b)