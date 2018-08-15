SUBLIST, SUPERLIST, EQUAL, UNEQUAL = "lt", "gt", "eq", "neq"


def are_equal(first_list, second_list):
    if len(first_list) != len(second_list):
        return False
    return all(a == b for a, b in zip(first_list, second_list))


def is_sub_list(first_list, second_list):
    i_first = 0
    i_second = 0
    while i_first < len(first_list) and i_second < len(second_list):
        if first_list[i_first] == second_list[i_second]:
            i_first += 1
        else:
            i_first = 1 if first_list[0] == second_list[i_second] else 0
        i_second += 1
    return i_first == len(first_list)


def check_lists(first_list, second_list):
    if are_equal(first_list, second_list):
        return EQUAL
    if is_sub_list(first_list, second_list):
        return SUBLIST
    if is_sub_list(second_list, first_list):
        return SUPERLIST
    return UNEQUAL


if __name__ == "__main__":
    print(check_lists([1, 1, 2], [0, 1, 1, 1, 2, 1, 2]))
