"""This is an exercise from https://exercism.io/my/tracks/python."""
from typing import List, NewType
from collections import Counter


Book = NewType('Book', int)
BOOK_PRICE = 800
DISCOUNTS = [0, 0, 5/100, 10/100, 20/100, 25/100]
GROUP_PRICE = [(BOOK_PRICE-(BOOK_PRICE*discount))*i for i, discount in enumerate(DISCOUNTS)]


def main():
    import random
    import time
    nb_books = 800
    books = [random.randint(1, 5) for _ in range(nb_books)]
    t_0 = time.time()
    print(calculate_total(books))
    t_1 = time.time()
    print(f"Computation for {nb_books} books done in {(t_1-t_0)*1000}ms")


def calculate_total(books: List[Book]) -> float:  # O(n log n)
    """Returns the best price for the given list of `books`."""
    if not books:
        return 0
    groups = group_books(books)
    return sum(group_price(book_group) for book_group in groups)


def group_price(book_group: List[Book]) -> float:  # O(1)
    """Return the price of a group of (unique) books."""
    return GROUP_PRICE[len(book_group)]


def group_books(books: List[Book]) -> List[List[Book]]:      # O(|B|n log n)
    """Return books grouped in such a way that they will minimize the total cost."""
    # NOTE: O(n) could be achieved by keeping track of group sizes insted of sorting
    book_counts = Counter(books)
    most_common_book, most_common_book_qte = book_counts.most_common(1)[0]
    del book_counts[most_common_book]
    book_groups = [[most_common_book] for _ in range(most_common_book_qte)]
    for book, nb_copies in book_counts.most_common():  # 'most_common' order does matter here!*
        book_groups.sort(key=group_rank)
        for i in range(nb_copies):
            book_groups[i].append(book)
    return book_groups


# Preliminary computations to determine what group sizes are the most favorable
# for the customers. This is done by determining which group sizes would offer the best
# reduction when adding one more book.

_group_rank = None
def group_rank(book_group: List[Book]) -> int:
    """Returns the rank of a group, the lower the group rank is, the more favorable
    for the customer it is to add a book in this group."""
    global _group_rank
    if _group_rank is None:
        _group_rank = compute_group_size_ranks(DISCOUNTS)
    return _group_rank[len(book_group)]


def compute_group_size_ranks(discounts: List[float]) -> List[int]:
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
    group_size_ranks = invert_list_indexes(best_group_sizes)
    return group_size_ranks


if __name__ == "__main__":
    main()


# Here is why "order does matter":
#   ----------------------------------------------------------------------------
#   for book, nb_copies in book_counts.most_common():
#         [1, 1, 1, 1]
#         [2, 2, 2, 2]
#         [3, 3, 3, 3]
#         [4, 4, 3, 3]
#         [4, 4, 4, 4]
#    -> [[1, 2, 3, 5], [1, 2, 3, 5], [1, 2, 3, 4], [1, 2, 3, 4]]
#   ----------------------------------------------------------------------------
#   for book, nb_copies in book_counts.most_common()[::-1]:
#         [1, 1, 1, 1]
#         [2, 2, 1, 1]
#         [3, 3, 1, 1] # care about local minimum
#         [4, 4, 2, 2] # Hmmm...
#         [5, 5, 3, 3] # woops
#   -> [[1, 5, 4, 3, 2], [1, 5, 4, 3, 2], [1, 3, 2], [1, 3, 2]]
#   ----------------------------------------------------------------------------
