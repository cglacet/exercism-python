"""Exercise from https://exercism.io/my/solutions/8ce1bcff16bd4e0c9dbecea5c367003d
It is supposed to be an easy problem but really struggled to find this solution.
"""

from collections import defaultdict
from itertools import combinations


def count(ascii_diagram):
    """Returns the total number of rectangles found in the diagram."""
    all_corners = defaultdict(set)
    for (x, y) in retrieve_corners(ascii_diagram):
        all_corners[y].add(x)
    reactangle_count = 0
    for (y_1, y_2) in combinations(all_corners, 2):
        corners_match = all_corners[y_1] & all_corners[y_2]
        n = len(corners_match)
        reactangle_count += (n*(n-1))//2
        reactangle_count -= nb_uncomplet_rectangles(ascii_diagram, y_1, y_2, corners_match)
    return reactangle_count


def retrieve_corners(ascii_diagram):
    """Returns all reactangle corners found in the diagram."""
    for (y, row) in enumerate(ascii_diagram):
        for (x, cell) in enumerate(row):
            if cell == "+":
                yield (x, y)


# Really uneficient for now (top and bottom borders sections that lies on K rectangles
# are checked K times).
def nb_uncomplet_rectangles(ascii_diagram, top, bottom, columns):
    """Giving `top` and `bottom` row togther with an iterable containing all `columns`
    this function returns the total number of incomplete rectangles for all combinations of
        (left, `top`, right, `bottom`) rectangles
    such that left < right and both are in `columns`.
    """
    incomplete_count = 0
    for left, right in combinations(columns, 2):
        top_row = ascii_diagram[top][left+1:right]
        bottom_row = ascii_diagram[bottom][left+1:right]
        rows = ascii_diagram[top+1:bottom]
        left_col = [row[left] for row in rows]
        right_col = [row[right] for row in rows]
        row_breach = row_has_breach(top_row) or row_has_breach(bottom_row)
        col_breach = col_has_breach(left_col) or col_has_breach(right_col)
        if row_breach or col_breach:
            incomplete_count += 1
    return incomplete_count


def row_has_breach(row):
    return ' ' in row or '|' in row


def col_has_breach(col):
    return ' ' in col or '-' in col
