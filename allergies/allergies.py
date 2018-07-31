class Allergies(object):
    allergens = [
        'eggs',
        'peanuts',
        'shellfish',
        'strawberries',
        'tomatoes',
        'chocolate',
        'pollen',
        'cats'
    ]
    nb_allergens = len(allergens)
    allergen_index = { allergen:i for (i, allergen) in enumerate(allergens)  }

    def __init__(self, score):
        self.mask =  [ (score & 2**i > 0) for i in range(Allergies.nb_allergens) ]

    def is_allergic_to(self, item):
        return self.mask[Allergies.allergen_index[item]]

    @property
    def lst(self):
        return [ allergen for (i, allergen) in enumerate(Allergies.allergens) if self.mask[i] ]
