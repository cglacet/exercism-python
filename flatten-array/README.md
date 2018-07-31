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
it's more fun. Also Guido himself said that he didn't like the approach:
> Another blog post showed decorators that can be used to implement tail recursion using magical exceptions or return values. These can be written in plain Python. [...]
> there are many caveats to the use of such a decorator, since it has to assume that any recursive call (in the decorated function) is tail-recursive and can be eliminated. [...]
> For all these reasons I think the decorator approach is doomed, at least for a general audience.

Of course we are not in the _general audience_ case. But let's see what we can do
with the iterative form.

My solution simply use a stack in which I will store cursors that indicate positions in iterable.
A cursor simply is an (address, index) pair, with the address being the currently
traversed array's address and index is the position within that array. Note that if we were
using [numpy](http://www.numpy.org/) arrays we could even just store the cursor position as the address of the
current sublist being traversed, note the difference:
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

With numpy `cursor = L[2:]` doesn't copy the array, it saves a reference in the
middle of the array, which in our case is exactly what we would like. But I won't
use numpy, simply because numpy has a [flatten function](https://docs.scipy.org/doc/numpy-1.14.0/reference/generated/numpy.ndarray.flatten.html),
it would make no sense to partially use numpy.

The [final solution](flatten_array.py) redefined `flatten` as (the rest of the code is unchanged):
```python
def flatten(iterable):
    return list(elements_of(iterable))

def elements_of(iterable):
    cursors = [[iterable, 0]]
    while len(cursors) > 0:
        cursor = cursors[-1]
        item, i = cursor
        # current sublist exhausted:
        if i >= len(item):
            cursors.pop()
        else:
           # entering a sublist:
           if is_list_like(item[i]):
               cursors.append([item[i], 0])
           # simple item found:
           else:
               if item[i] is not None:
                   yield item[i]
           cursor[1] += 1 # "i += 1"
```

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
