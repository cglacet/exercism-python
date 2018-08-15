"""Exercise from https://exercism.io/my/tracks/python"""


def binary_search(list_of_numbers, number):
    """Returns the index of `number` in the sorted list `list_of_numbers`.
    Raise ``ValueError`` if `number` is not in `list_of_numbers`."""
    left, right = 0, len(list_of_numbers)-1
    while right >= left:
        middle = (left+right)//2
        middle_number = list_of_numbers[middle]
        if middle_number == number:
            return middle
        if middle_number < number:
            left = middle + 1
        else:
            right = middle - 1

    raise ValueError("Not found.")
