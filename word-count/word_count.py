import re
from collections import Counter

WORD_REGEX = r"[a-zA-Z\d]+(?:\'t)?"

def word_count(phrase):
  words = re.findall(WORD_REGEX, phrase)
  return Counter(map(str.lower, words))