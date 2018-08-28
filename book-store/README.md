# Book Store

To try and encourage more sales of different books from a popular 5 book
series, a bookshop has decided to offer discounts on multiple book purchases.

One copy of any of the five books costs $8.

If, however, you buy two different books, you get a 5%
discount on those two books.

If you buy 3 different books, you get a 10% discount.

If you buy 4 different books, you get a 20% discount.

If you buy all 5, you get a 25% discount.

Note: that if you buy four books, of which 3 are
different titles, you get a 10% discount on the 3 that
form part of a set, but the fourth book still costs $8.

Your mission is to write a piece of code to calculate the
price of any conceivable shopping basket (containing only
books of the same series), giving as big a discount as
possible.

For example, how much does this basket of books cost?

- 2 copies of the first book
- 2 copies of the second book
- 2 copies of the third book
- 1 copy of the fourth book
- 1 copy of the fifth book

One way of grouping these 8 books is:

- 1 group of 5 --> 25% discount (1st,2nd,3rd,4th,5th)
- +1 group of 3 --> 10% discount (1st,2nd,3rd)

This would give a total of:

- 5 books at a 25% discount
- +3 books at a 10% discount

Resulting in:

- 5 x (8 - 2.00) == 5 x 6.00 == $30.00
- +3 x (8 - 0.80) == 3 x 7.20 == $21.60

For a total of $51.60

However, a different way to group these 8 books is:

- 1 group of 4 books --> 20% discount  (1st,2nd,3rd,4th)
- +1 group of 4 books --> 20% discount  (1st,2nd,3rd,5th)

This would give a total of:

- 4 books at a 20% discount
- +4 books at a 20% discount

Resulting in:

- 4 x (8 - 1.60) == 4 x 6.40 == $25.60
- +4 x (8 - 1.60) == 4 x 6.40 == $25.60

For a total of $51.20

And $51.20 is the price with the biggest discount.

# Solution

In this exercise you can try to battle on complexity by trying different kind of brute force algorithms. But in the end it is possible to achieve O(n) complexity (with n being the total number of book copies). Here are two observations that will help finding a O(n) solution (or a least a solution that has complexity very close to O(n)):

- The price only depend on the group size. (Most people will probably notice that and use it to build partitions for brute force)
- Some group size are better than others for the customer.

Every time you want to add a new book in existing groups you only need to ask yourself one question: "In which group should the new book be added so the number of __good groups__ is maximized?". In order to achieve that you only need to know the __ranks__ of group sizes, if the best group size is L, then you'll add the new book in groups of size L-1 (if possible). The only challenge now is to find groups with the size you are looking for (here L-1 and make sure you can add the new book, ie. there is no duplicate in the group).

__Formal description of the solution__ Lets define rank to be a function, such that

<p align="center"> rank(g) <ᵦ rank(g') ⇒ total_cost(g ∪ {β}, g') < total_cost(g, g' ∪ {β})</p>

ie., it's better to add book β to g than g' (note that rank comparison <ᵦ is only defined for groups that exclude book β). Suppose that you've already created k optimal groups for all books from B = {1,2,3} (with any number of copy of each book) and that we are now ready to add n₄ copies of book 4. To do so we will first sort existing groups by rank with respect to <₄ (all groups exclude book 4, therefore we can compare them).

<p align="center"> G = (g₁, g₂, ..., gₖ) | ∀ (u,v): u < v ⇒ rank(gᵤ) ≤₄ rank(gᵥ) </p>

Now we just need to add the n₄ copies of book 4 to group gᵢ for all i in \[1, n₄\], ie., we add books 4 to the first n₄ best groups. You can then repeat the same process for books 5.

This solution can be implemented easily with a complexity O(|B|n log n) by simply iterating through books (1,2,3,4,5) and sorting book groups according to their ranks at each step. Note that when adding some book that has n copies, the number of existing groups |G| could be smaller than n. This can be solved by simply initializing groups with a single copy of the most frequent book or by creating n-|G| new single book groups.  

Notice that of single book groups had a discount, this would force us to define rank({}), which would not really be a problem but (I think) would make the code messier.

__O(|B|n log n) implementation__

Since book ranks do not depend on their content but only on their size, we can precompute ranks:
```python
DISCOUNTS = [0, 0, 5/100, 10/100, 20/100, 25/100]
BOOK_PRICE = 800
GROUP_PRICE = [(BOOK_PRICE-(BOOK_PRICE*discount))*i for i, discount in enumerate(DISCOUNTS)]

def compute_group_size_ranks(discounts):
    """Returns book groups size rankings, the lower the value, the most favorable
    it is for the customer to add a book in a group of the given size."""
    def invert_list_indexes(list_indexes):
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

GROUP_SIZE_RANKS = compute_group_size_ranks(DISCOUNTS)

def group_rank(book_group: List[int]) -> int:
    """Returns the rank of a group, the lower the group rank is the more favorable for the customer
    for the customer it is to add a book in this group."""
    return GROUP_SIZE_RANKS[len(book_group)]
```

All precomputations are done, we now have to group books. First we initialize groups with a single copy of the most frequent book, then we add all the other book copies:
```python
def group_books(books):
    """Return books grouped in such a way that they will minimize the total cost."""
    # NOTE: O(n) could be achieved by keeping track of group sizes insted of sorting
    book_counts = Counter(books)
    most_common_book, most_common_book_qte = book_counts.most_common(1)[0]
    book_groups = [[most_common_book] for _ in range(most_common_book_qte)]
    del book_counts[most_common_book]
    for book, nb_copies in book_counts.most_common():
        book_groups.sort(key=group_rank)
        print([len(g) for g in book_groups])
        for i in range(nb_copies):
            book_groups[i].append(book)
    return book_groups
```

The others functions we need to finish the exercise:
```python
def calculate_total(books: List[int]) -> float:  # O(n log n)
    """Returns the best price for the given list of `books`."""
    if not books:
        return 0
    return sum(group_price(book_group) for book_group in group_books(books))

def group_price(book_group: List[int]) -> float:  # O(1)
    """Return the price of a group of (unique) books."""
    return GROUP_PRICE[len(book_group)]
```

Why O(|B|n log n)? Because we sort all book groups and the number of groups can be O(n) (for example (n-3)/2 copies of book 1, (n-3)/2 copies of book 2 and one copy of books 3,4 and 5). We could do O(n log n) without too much trouble by filling groups in the oposite order (from the least frequent book to the most frequent) but once again, the gain is not that important and that would make the code a bit more complex.

__O(n) implementation__ Instead of sorting for every new book (here 4 times), we could keep track of group size (using a dictionary for example) but this would add a lot of noise compared to the small gain in complexity.

## Exception messages

Sometimes it is necessary to raise an exception. When you do this, you should include a meaningful error message to
indicate what the source of the error is. This makes your code more readable and helps significantly with debugging. Not
every exercise will require you to raise an exception, but for those that do, the tests will only pass if you include
a message.

To raise a message with an exception, just write it as an argument to the exception type. For example, instead of
`raise Exception`, you should write:

```python
raise Exception("Meaningful message indicating the source of the error")
```

## Running the tests

To run the tests, run the appropriate command below ([why they are different](https://github.com/pytest-dev/pytest/issues/1629#issue-161422224)):

- Python 2.7: `py.test book_store_test.py`
- Python 3.4+: `pytest book_store_test.py`

Alternatively, you can tell Python to run the pytest module (allowing the same command to be used regardless of Python version):
`python -m pytest book_store_test.py`

### Common `pytest` options

- `-v` : enable verbose output
- `-x` : stop running tests on first failure
- `--ff` : run failures from previous test before running other test cases

For other options, see `python -m pytest -h`

## Submitting Exercises

Note that, when trying to submit an exercise, make sure the solution is in the `$EXERCISM_WORKSPACE/python/book-store` directory.

You can find your Exercism workspace by running `exercism debug` and looking for the line that starts with `Workspace`.

For more detailed information about running tests, code style and linting,
please see [Running the Tests](http://exercism.io/tracks/python/tests).

## Source

Inspired by the harry potter kata from Cyber-Dojo. [http://cyber-dojo.org](http://cyber-dojo.org)

## Submitting Incomplete Solutions

It's possible to submit an incomplete solution so you can see how others have completed the exercise.
