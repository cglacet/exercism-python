import re

possible_values = [ str(i) for i in range(10)]+['X']

def to_int(char):
    try:
        return int(char)
    except:
        return 10

def verify(isbn):
    match_with_dashes = re.match(r"^\d\-\d{3}-\d{5}-[\dX]\Z", isbn)
    match_without_dashes = re.match(r"^\d{9}[\dX]\Z", isbn)
    if not (match_with_dashes or match_without_dashes):
        return False

    character_index = 10
    isbn_total_value = 0
    for char in isbn:
        if char in possible_values:
            isbn_total_value += to_int(char)*character_index
            character_index -= 1
    return isbn_total_value%11 == 0
