# Flatten Array

Take a nested list and return a single flattened list with all values except nil/null.

The challenge is to write a function that accepts an arbitrarily-deep nested list-like structure and returns a flattened structure without any nil/null values.

For Example

input: [1,[2,3,null,4],[null],5]

output: [1,2,3,4,5]

## My solution

Why is the naïve solution _bad_? Here is what you can do in a few lines of code:
```python
import collections

def flatten(iterable):
    return list(iterate_elements(iterable))

def iterate_elements(item):
    if item is None:
        return
    if is_list_like(item):
        for sub_item in item:
            yield from iterate_elements(sub_item)
    else:
        yield item

def is_list_like(item):
    try:
        iter(item)
        return not isinstance(item, str)
    except TypeError:
        return False
```

This of course is a valid code, it does what it is supposed to do and pass all
the tests defined in [flatten_array_test.py](flatten_array_test.py). The problem
with this code is that it will fail to flatten any list whose depth is greater than
the python call stack size (which is 10^3). This code would raise the following
error `RuntimeError: Maximum recursion depth exceeded`. It is also important to notice that
python doesn't support tail-call optimization. Which means that we would have to
implement tail recursion elimination by hand if we wanted to achieve flattening
with a recursive function.

You can find solutions for tail recursion elimination online, for example
[here](), but I made the choice to implement it with an iterative solution because
it's more fun. Also Guido himself said that [he didn't like the approach](http://neopythonic.blogspot.com/2009/04/tail-recursion-elimination.html):
> Another blog post showed decorators that can be used to implement tail recursion using magical exceptions or return values. These can be written in plain Python. [...]
> there are many caveats to the use of such a decorator, since it has to assume that any recursive call (in the decorated function) is tail-recursive and can be eliminated. [...]
> For all these reasons I think the decorator approach is doomed, at least for a general audience.

Of course we are not in the _general audience_ case. But let's see what we can do
with the iterative form.

My solution simply use a stack in which I will store cursors that indicate positions in iterable.
A cursor simply is an (address, index) pair, with the address being the currently
traversed array's address and index is the position within that array. Note that if we were
using [numpy](http://www.numpy.org/) arrays we could even just store the cursor's position as the address of the
current sublist being traversed. _Why?_ Note the difference:
```python
L = [1,2,5,4]
cursor = L[2:]
cursor[0] = 3
L
```

> [1,2,5,4]

```python
> [1,2,5,4]
L = numpy.array([1,2,5,4])
cursor = L[2:]
cursor[0] = 3
```
> array([1, 2, 3, 4])

With numpy, `cursor = L[2:]`, doesn't copy the array, it saves a reference in the
middle of the array, which in our case is exactly what we would like. But I won't
use numpy, simply because numpy already has a [flatten function](https://docs.scipy.org/doc/numpy-1.14.0/reference/generated/numpy.ndarray.flatten.html),
it would make no sense to partially use numpy.

The [final solution](flatten_array.py) redefined `flatten` as (the rest of the code is unchanged):
```python

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
        if is_list_like(item):  # pre-order
            cursor_stack.append(iter(item))
        elif item is not None:
            yield item          # in-order
```

In terms of complexity, with _n_ being the total
number of objects in the input `iterable` (note that `[[[[1]]]]` contains four
objects in total, three lists and one integer):
 - Time complexity is _O(n)_, we progress go over each object exactly once.
 - Space complexity is also _O(n)_. We store one (address, index) pair per sublist
 in `iterable`. The maximum number of sublist is _n_ in the case where `iterable`
 is only made of _n-1_ lists encapsulated in one another with a single value
 inside the last list, like so `[[[[[...[1]...]]]]]`.

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

- Python 2.7: `py.test flatten_array_test.py`
- Python 3.4+: `pytest flatten_array_test.py`

Alternatively, you can tell Python to run the pytest module (allowing the same command to be used regardless of Python version):
`python -m pytest flatten_array_test.py`

### Common `pytest` options

- `-v` : enable verbose output
- `-x` : stop running tests on first failure
- `--ff` : run failures from previous test before running other test cases

For other options, see `python -m pytest -h`

## Submitting Exercises

Note that, when trying to submit an exercise, make sure the solution is in the `$EXERCISM_WORKSPACE/python/flatten-array` directory.

You can find your Exercism workspace by running `exercism debug` and looking for the line that starts with `Workspace`.

For more detailed information about running tests, code style and linting,
please see [Running the Tests](http://exercism.io/tracks/python/tests).

## Source

Interview Question [https://reference.wolfram.com/language/ref/Flatten.html](https://reference.wolfram.com/language/ref/Flatten.html)

## Submitting Incomplete Solutions

It's possible to submit an incomplete solution so you can see how others have completed the exercise.
