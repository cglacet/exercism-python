"""Exercise from https://exercism.io/my/tracks/python."""
import sys


def flatten(iterable):
    """Returns a flattened list of non-list-like objects from `iterable` in DFS
    traversal order.
    """
    return list(elements_of(iterable))


def elements_of(iterable):
    """Genertor that yields every non-list-like objects from `iterable` in DFS
    traversal order.
    """
    # The base idea is to mimic the python stack with `cursors`. This function
    # iterate in DFS order starting from the root's (`iterable`) left-most item (``iterable[0]``).
    # 1) When the traversal gets to a sub-iterable (a subtree), a new cursor is
    #    pused to the `cursors` stack.
    # 2) When a sub-iterable is consumed (the subtree has completely traversed),
    #    the cursor goes back to the root of the corresponding subtree.
    #
    #       iterable = [0, [1,2], 3, 4]
    #                    |
    #           -------------------
    #           |     |     |     |
    #           0   --o--   3     4
    #               |   |
    #               1   2
    #
    cursors = [[iterable, 0]]
    while len(cursors) > 0:
        cursor = cursors[-1]
        item, i = cursor
        if i >= len(item):
            cursors.pop()
            continue
        if is_list_like(item[i]):
            cursors.append([item[i], 0])
        else:
            if item[i] is not None:
                yield item[i]
        cursor[1] += 1


def is_list_like(item):
    """Returns `True` if `item` is considered list-like (non-string iterable)"""
    try:
        iter(item)
        return not isinstance(item, str)
    except TypeError:
        return False


def build_deep_list(depth):
    """Returns a list of the form $l_{depth} = [depth-1, l_{depth-1}]$
    with $depth > 1$ and $l_0 = [0].
    """
    sub_list = [0]
    for d in range(1, depth):
        sub_list = [d, sub_list]
    return sub_list


if __name__ == "__main__":
    # Default python maximum stack size is around 10**3.
    depth = int(sys.argv[1]) if len(sys.argv) > 1 else 10**4
    deep_list = build_deep_list(depth)
    try:
        print(deep_list)  # Will fail if depth > max stack size.
    except RecursionError as error:
        print(error)
    flat_list = flatten(deep_list)  # Will not fail because of stack limitation.
    if depth > 10:
        str_begining = str(flat_list[:5])[1:-1]
        str_end = str(flat_list[-5:])[1:-1]
        print("[{}, ..., {}]".format(str_begining, str_end))
    else:
        print(flat_list)
