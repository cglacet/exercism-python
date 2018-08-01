# Saddle Points

Detect saddle points in a matrix.

So say you have a matrix like so:

```text
    0  1  2
  |---------
0 | 9  8  7
1 | 5  3  2     <--- saddle point at (1,0)
2 | 6  6  7
```

It has a saddle point at (1, 0).

It's called a "saddle point" because it is greater than or equal to
every element in its row and less than or equal to every element in
its column.

A matrix may have zero or more saddle points.

Your code should be able to provide the (possibly empty) list of all the
saddle points for any given matrix.

Note that you may find other definitions of matrix saddle points online,
but the tests for this exercise follow the above unambiguous definition.

## My solution


### The implementation

Here I just wanted to have something that could be used for more matrix operations.
I thus created a `Matrix` with the goal of having a `saddle_points` method as
simple as possible with the algorithm as clear as possible:
```python
def saddle_points(self):
   is_max_in_row = self.is_cell(condition=max, within=Axis.ROW)
   is_min_in_col = self.is_cell(condition=min, within=Axis.COLUMN)
   is_saddle = is_max_in_row & is_min_in_col
   saddle_indexes = set(self.index_where(is_saddle))
   return saddle_indexes
```

### What it does

For an input matrix `self`:
```python
Matrix(
	[9, 8, 7],
	[5, 3, 2],
	[6, 6, 7]
)
```
The first matrix I compute, `is_row_max` is such that if `is_row_max[i,j]` is `True`
then `self[i,j]` is (one of) the maximum(s) within its row.
```python
Matrix(
	[True, False, False],
	[True, False, False],
	[False, False, True]
)
```
The second matrix, `is_col_min` represents the same thing `min` values within columns:
```python
Matrix(
	[False, False, False],
	[True, True, True],
	[False, False, False]
)
```
Finally `is_saddle[i, j]` will be true if both `is_row_max[i,j]`
and `is_col_min[i,j]` are true (notice that you need to implement the _magic_ method `__and__`
for `is_row_max & is_col_min` to work). The matrix `is_saddle` is the following:
```python
Matrix(
	[False, False, False],
	[True, False, False],
	[False, False, False]
)
```
Here you can notice that the only index at which a saddle point has been found is
`(1, 0)` (_**5** > 3 > 2_ and _**5** < 6 < 9_ which make it a valid saddle point).
```python
Matrix(
	[9, 8, 7],
	[5, 3, 2],
	[6, 6, 7]
)
```

### Remarks on implementation details (python stuff)

#### Kind of immutable

Property "immutability" can be achieve by having a `_` property which means that
the property is not part of the public API.
```python
def __init__(self, data):
    self._data = data

@property
def data(self):
    return self._data[:]
```
I added quotes around immutability
because access to `_data` is not prevented by any mechanism, if someone just call
`m = Matrix([[1,2]])` then `m._data = [[3,4]]` then `print(m)` will print:
```python
Matrix(
	[3, 4]
)
```
On the other hand, if you call `m.data = [[3,4]]` the following error will be raised:
```python
AttributeError: can't set attribute
```
Which is exactly what we want, every modification of the `data` property should be
done internally (within a matrix object).

What do you think will be printed if you do:
```python
m = Matrix([[1,2]])
data = m.data
data = [[3,4]]
print(m)
```
<details>
<summary>
Click here once you think you have the answer.
</summary>

```python
Matrix(
	[1, 2]
)
```

Look closer at the `data` ~~method~~ property:

```python
@property
def data(self):
    return self._data[:]
```

The slice operator `[<start>:<end>]` doesn't return a reference but a copy of the input array.
Therefore `data` and `m.data` are two distinct lists.
```python
m = [0,0,0,0]
sub_m = m[:]
sub_m[0] = 1
print(m)
print("m[0] address =",hex(id(m[0])))
print("sub_m[0] address =",hex(id(sub_m[0])))
```
Prints:
```python
[0, 0, 0, 0]
m[0] address = 0x102ed4a80
sub_m[0] address = 0x102ed4a60
```

Notice that `numpy` does return a reference when slicing:
```python
m = numpy.array([0,0,0,0])
sub_m = m[:]
sub_m[0] = 1
print(m)
print("m[0] address =",hex(id(m[0])))
print("sub_m[0] address =",hex(id(sub_m[0])))
```

This would print:
```python
[1 0 0 0]
m[0] address = 0x110995ba0
sub_m[0] address = 0x110995ba0
```
</details>

If you need a true immutable property, [this solution](https://gist.github.com/microamp/9d8e3359bcadd7dca6a8#file-immutable-py-L13) looks good enough to me:
```python
class Immutable2(tuple):
    """Immutable class using tuple."""
    def __new__(cls, x, y):
        return tuple.__new__(cls, (x, y,))

    @property
    def x(self):
        return tuple.__getitem__(self, 0)

    @property
    def y(self):
        return tuple.__getitem__(self, 1)
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

- Python 2.7: `py.test saddle_points_test.py`
- Python 3.4+: `pytest saddle_points_test.py`

Alternatively, you can tell Python to run the pytest module (allowing the same command to be used regardless of Python version):
`python -m pytest saddle_points_test.py`

### Common `pytest` options

- `-v` : enable verbose output
- `-x` : stop running tests on first failure
- `--ff` : run failures from previous test before running other test cases

For other options, see `python -m pytest -h`

## Submitting Exercises

Note that, when trying to submit an exercise, make sure the solution is in the `$EXERCISM_WORKSPACE/python/saddle-points` directory.

You can find your Exercism workspace by running `exercism debug` and looking for the line that starts with `Workspace`.

For more detailed information about running tests, code style and linting,
please see [Running the Tests](http://exercism.io/tracks/python/tests).

## Source

J Dalbey's Programming Practice problems [http://users.csc.calpoly.edu/~jdalbey/103/Projects/ProgrammingPractice.html](http://users.csc.calpoly.edu/~jdalbey/103/Projects/ProgrammingPractice.html)

## Submitting Incomplete Solutions

It's possible to submit an incomplete solution so you can see how others have completed the exercise.
