import unittest

from anagram import detect_anagrams

# Tests adapted from `problem-specifications//canonical-data.json` @ v1.2.0

class AnagramTest(unittest.TestCase):
    def test_no_matches(self):
        candidates = ["hello", "world", "zombies", "pants"]
        self.assertEqual(detect_anagrams("diaper", candidates), [])

    def test_detects_two_anagrams(self):
        candidates = ["stream", "pigeon", "maters"]
        self.assertEqual(
            detect_anagrams("master", candidates), ["stream", "maters"])

    def test_does_not_detect_anagram_subsets(self):
        self.assertEqual(detect_anagrams("good", ["dog", "goody"]), [])

    def test_detects_anagram(self):
        candidates = ["enlists", "google", "inlets", "banana"]
        self.assertEqual(detect_anagrams("listen", candidates), ["inlets"])

    def test_detects_three_anagrams(self):
        candidates = [
            "gallery", "ballerina", "regally", "clergy", "largely", "leading"
        ]
        self.assertEqual(
            detect_anagrams("allergy", candidates),
            ["gallery", "regally", "largely"])

    def test_does_not_detect_non_anagrams_with_identical_checksum(self):
        self.assertEqual(detect_anagrams("mass", ["last"]), [])

    def test_detects_anagrams_case_insensitively(self):
        candidates = ["cashregister", "Carthorse", "radishes"]
        self.assertEqual(
            detect_anagrams("Orchestra", candidates), ["Carthorse"])

    def test_detects_anagrams_using_case_insensitive_subject(self):
        candidates = ["cashregister", "carthorse", "radishes"]
        self.assertEqual(
            detect_anagrams("Orchestra", candidates), ["carthorse"])

    def test_detects_anagrams_using_case_insensitive_possible_matches(self):
        candidates = ["cashregister", "Carthorse", "radishes"]
        self.assertEqual(
            detect_anagrams("orchestra", candidates), ["Carthorse"])

    def test_does_not_detect_a_anagram_if_the_original_word_is_repeated(self):
        self.assertEqual(detect_anagrams("go", ["go Go GO"]), [])

    def test_anagrams_must_use_all_letters_exactly_once(self):
        self.assertEqual(detect_anagrams("tapper", ["patter"]), [])

    def test_capital_word_is_not_own_anagram(self):
        self.assertEqual(detect_anagrams("BANANA", ["Banana"]), [])

    def test_speed(self):
        detect_anagrams(rand_letters(10), [ rand_letters(10) for _ in range(10**6)])


import random
from string import ascii_uppercase
alphabet_size = len(ascii_uppercase)
def rand_letters(nb_letters):
    return ''.join([ ascii_uppercase[random.randint(0,alphabet_size-1)] for _ in range(nb_letters) ])



if __name__ == '__main__':
    unittest.main()
