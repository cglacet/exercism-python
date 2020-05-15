import re
from collections import Counter

WORD_REGEX = r"[a-zA-Z\d]+(?:\'t)?"

def word_count(phrase):
  return Counter(re.findall(WORD_REGEX, phrase.lower()))