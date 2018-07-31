from collections import defaultdict

# Score categories
# Change the values as you see fit
YACHT = "Yatch"
ONES = "Ones"
TWOS = "Twos"
THREES = "Threes"
FOURS = "Fours"
FIVES = "Fives"
SIXES = "Sixes"
FULL_HOUSE = "Full house"
FOUR_OF_A_KIND = "Four of a kind"
LITTLE_STRAIGHT = "Little straight"
BIG_STRAIGHT = "Big straight"
CHOICE = "Choice"

def singles(category):
    def single(dice):
        number = single_category_numeral_values[category]
        return dice.count(number)*number
    return single

single_categories = [ONES, TWOS, THREES, FOURS, FIVES,  SIXES]
single_category_numeral_values = { single_categories[i]:i+1 for i in range(len(single_categories)) }
single_score_rules = { category:singles(category) for category in single_categories }

def get_values_count(dice):
    values_count = defaultdict(int)
    for d in dice:
        values_count[d] += 1
    return values_count

def full_house(dice):
    trio = None
    duo = None
    for value, count in get_values_count(dice).items():
        if count == 3:
            trio = value
        if count == 2:
            duo = value
    if duo is not None and trio is not None:
        return sum(dice)

def four_of_a_kind(dice):
    for value, count in get_values_count(dice).items():
        if count >= 4:
            return value*4

def little_straight(dice):
    if sorted(dice) == [1,2,3,4,5]:
        return 30

def big_straight(dice):
    if sorted(dice) == [2,3,4,5,6]:
        return 30

def yacht(dice):
    if max(get_values_count(dice).values()) == 5:
        return 50

score_rules = {
    **single_score_rules,
    FULL_HOUSE: full_house,
    FOUR_OF_A_KIND: four_of_a_kind,
    LITTLE_STRAIGHT: little_straight,
    BIG_STRAIGHT: big_straight,
    CHOICE: sum,
    YACHT: yacht
}

def score(dice, category):
    if category in score_rules:
        get_category_score = score_rules[category]
        score = get_category_score(dice)
        if score is None:
            return 0
        else:
            return score
