from collections import Counter
from itertools import product
import re

VALUES = "2 3 4 5 6 7 8 9 10 J Q K A".split()
VALUES_INDEXES = {v: i for i, v in enumerate()}
print(VALUES)
COLORS = "C S D H".split()
DECK = product(VALUES, COLORS)


class Card:
    def __init__(self, representation):
        self.value, self.color = self.split(representation)
        self.value_index = VALUES_INDEXES[self.value]

    def __repr__(self):
        return "{}{}".format(self.value, self.color)

    def __gt__(self, other):
        return self.value_index > other.value_index

    def __add__(self, other):
        self.value_index + other
        return Card()...

    @staticmethod
    def split(representation):
        m = re.match(r"(10|[2-9]|[JQKA])([CSDH])", representation)
        if m is None:
            raise ValueError("Card {} is not valid.".format(representation))
        return m.group(1), m.group(2)


class Hand:
    def __init__(self, representation):
        self.cards = sorted([Card(r) for r in representation.split()])
        self.value_count = Counter(card.value for card in self.cards)

    def __repr__(self):
        return ' '.join([str(c) for c in self.cards])

    def is_max_count_greater(self, value):
        return self.value_count.most_common(1)[0][1] == value

    def is_straight(self):
        return all(c_1+1 == c_2 for (c_1, c_2) in zip(self.cards[:-1], self.cards[1:]))


def best_hands(hands):
    pass

h = Hand("4D 5S 2S 6D 3C")
print(h)
print(h.is_straight())
c = Card("4C")
print(c+1)
