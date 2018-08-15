"""Exercise from https://exercism.io/my/tracks/python."""
import sys
import time


def flatten(iterable):
    """Returns a flattened list of non-list-like objects from `iterable` in DFS
    traversal order.
    """
    return list(items_from(iterable))


def items_from(iterable):
    """Genertor that yields every non-list-like objects from `iterable` in DFS
    traversal order.
    """
    # The base idea is to mimic the python stack with `cursors`. This function
    # iterate the inpute `iterable` in DFS order starting from the root
    # (`iterable`) and going from the left-most item (``iterable[0]``) to the right-most
    # item (``iterable[-1]``). During traversal, two kinds of node will be met,
    # list-like (`sub_iterable`) objects and simple `item`s.
    #
    # PRE   When the traversal gets to a sub-iterable (a subtree), a new cursor is
    #       pused to `cursor_stack`.
    # IN    When a simple `item` is traversed it's yield.
    # POST  When a sub-iterable is consumed (the subtree has completely traversed),
    #       the cursor goes back to the root of the corresponding subtree.
    #
    #       iterable = [0, [1,2], 3, 4]
    #
    #                    I
    #                    |
    #           -------------------
    #           |     |     |     |
    #           0   --I--   3     4
    #               |   |
    #               1   2
    #
    # This tree contains two `sub_iterables` ('I') and five items ('0', '1', '2', '3', '4').
    cursor_stack = [iter(iterable)]
    while cursor_stack:
        sub_iterable = cursor_stack[-1]
        try:
            item = next(sub_iterable)
        except StopIteration:   # post-order
            cursor_stack.pop()
            continue
        try:                    # pre-order
            cursor_stack.append(list_like_iter(item))
        except TypeError:
            if item is not None:
                yield item      # in-order


def list_like_iter(item):
    """Returns an iterator of `item` if `item` is considered list-like (non-string iterable)"""
    if isinstance(item, str):
        raise TypeError("String are not iterable considered list-like objects.")
    return iter(item)


def build_deep_list(depth):
    """Returns a list of the form $l_{depth} = [depth-1, l_{depth-1}]$
    with $depth > 1$ and $l_0 = [0]$.
    """
    sub_list = [0]
    for d in range(1, depth):
        sub_list = [d, sub_list]
    return sub_list

def repr_long_list(_list):
    if depth > 10:
        str_begining = str(_list[:5])[1:-1]
        str_end = str(_list[-5:])[1:-1]
        return "[{}, ..., {}]".format(str_begining, str_end)
    else:
        return str(_list)

def flatten_str(lst):
    return eval('[' + str(lst).replace('[', '').replace(']', '') + ']')

if __name__ == "__main__":
    # Default python maximum stack size is around 10**3.
    depth = int(sys.argv[1]) if len(sys.argv) > 1 else 10**4
    deep_list = build_deep_list(depth)
    try:
        print(deep_list)  # Will fail if depth > max stack size.
    except RecursionError as error:
        print(error)

    flat_list = flatten(deep_list)  # Will not fail because of stack limitation.
    print(repr_long_list(flat_list))
