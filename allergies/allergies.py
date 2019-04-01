""" Let `n` be the number of allergens and k (<= n) be the number of allergies.

I created this version to demonstrate how O(k) time complexity can be achieved
for all methods.
"""
import math


class Allergies:
    """Defines a sublist of allergies from a predefined list of `allergens`."""

    allergens = ['eggs', 'peanuts', 'shellfish', 'strawberries',
                 'tomatoes', 'chocolate', 'pollen', 'cats']

    nb_allergens = len(allergens)
    allergen_index = {allergen: i for (i, allergen) in enumerate(allergens)}

    def __init__(self, score):  # O(k)
        self.allergies = list(self._allergens_in_score(score))
        self.score = score

    @staticmethod
    def _allergens_in_score(score):  # O(k)
        while score >= 1:
            item_score = math.floor(math.log(score, 2))
            score -= 2**item_score
            try:
                yield Allergies.allergens[item_score]
            except IndexError:
                pass

    def is_allergic_to(self, item):  # O(1)
        """Returns true if `item` is in the allergies list."""
        return (self.score & 2**Allergies.allergen_index[item]) > 0

    @property
    def lst(self):  # O(k)
        """Returns the list of allergies."""
        return self.allergies
