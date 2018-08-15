"""This is an exercise from https://exercism.io/my/tracks/python."""
from typing import List, NewType
from collections import Counter


Book = NewType('Book', int)

DISCOUNTS = [0, 0, 5/100, 10/100, 20/100, 25/100]
BOOK_PRICE = 800


# Premilinary computations to determine what group size are the most favorable
# for the customers. This is done by determining which group sizes offer the best
# reduction compared to the next one.
def group_size_ranks(discounts: List[float]) -> List[int]:
    """Returns book groups size rankings, the lower the value, the most favorable
    it is for the customer to add a book in a group of the given size."""
    def invert_list_indexes(list_indexes: List[int]) -> List[int]:
        result = [0]*len(list_indexes)
        for i, j in enumerate(list_indexes):
            result[j] = i
        return result

    # The percentage of a book that is offered for a given group size:
    total_discount = [discount*qte for qte, discount in enumerate(discounts)]
    # What is the reduction obtained when adding one more book?
    next_offer_increase = [total_discount[i+1]-total_discount[i] for i in range(len(total_discount)-1)]
    # Using this we now know which group sizes are the bests:
    best_group_sizes = sorted(range(len(next_offer_increase)), key=lambda i: next_offer_increase[i], reverse=True)
    # The ranks are what we are interested in:
    return invert_list_indexes(best_group_sizes)


GROUP_PRICE = [(BOOK_PRICE-(BOOK_PRICE*discount))*i for i, discount in enumerate(DISCOUNTS)]
GROUP_SIZE_RANKS = group_size_ranks(DISCOUNTS)


def group_rank(book_group: List[Book]) -> int:
    """Returns the rank of a group, the lower the group rank is, the more favorable
    for the customer it is to add a book in this group."""
    return GROUP_SIZE_RANKS[len(book_group)]
# End of precomputations


def calculate_total(books: List[Book]) -> float:  # O(n log n)
    """Returns the best price for the given list of `books`."""
    if not books:
        return 0
    return sum(group_price(book_group) for book_group in group_books(books))


def group_price(book_group: List[Book]) -> float:  # O(1)
    """Return the price of a group of (unique) books."""
    return GROUP_PRICE[len(book_group)]


def group_books(books: List[Book]) -> List[List[Book]]:      # O(n log n)
    """Return books grouped in such a way that they will minimize the total cost."""
    # NOTE: O(n) could be achieved by keeping track of group sizes insted of sorting
    book_counts = Counter(books)
    most_common_book, most_common_book_qte = book_counts.most_common(1)[0]
    book_groups = [[most_common_book] for _ in range(most_common_book_qte)]
    del book_counts[most_common_book]
    for book, count in book_counts.most_common(len(book_counts)):
        book_groups.sort(key=group_rank)
        for i in range(count):
            book_groups[i].append(book)
    return book_groups
