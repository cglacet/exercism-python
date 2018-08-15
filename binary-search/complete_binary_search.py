import random


def main():
    for _ in range(1000):
        list_of_numbers = sorted([random.randint(1, 30) for _ in range(random.randint(10, 30))])
        number = random.choice(list_of_numbers)
        position = binary_search(list_of_numbers, number, debug=True)
        assert list_of_numbers[position] == number

def state_repr(list_of_numbers, left, middle, right):
    text = ""
    for i, number in enumerate(list_of_numbers):
        number_text = str(number)
        if i == middle:
            number_text = "(" + number_text + ")"
        left_text = "[" if left == i else " "
        right_text = "]" if right == i else " "
        text += left_text + number_text + right_text
    return text


def binary_search(list_of_numbers, number, debug=False):
    if debug:
        print("Looking for {} in {}".format(number, list_of_numbers))
    left, right = 0, len(list_of_numbers)-1
    while right-left >= 0:
        middle = left + (right-left)//2
        middle_number = list_of_numbers[middle]
        if debug:
            print(state_repr(list_of_numbers, left, middle, right))
        if middle_number == number:
            return middle
        if middle_number < number:
            left = middle + 1
        else:
            right = middle - 1

    return None


if __name__ == "__main__":
    main()
