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
   is_row_max = self.is_row(condition=max)
   is_col_min = self.is_col(condition=min)
   is_saddle = is_row_max & is_col_min
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
Here you can notice that the only index at which we can find a saddle point is
`(1, 0)` (_**5** > 3 > 2_ and _**5** < 6 < 9_ therefore it's a valid saddle point).
```python
Matrix(
	[9, 8, 7],
	[5, 3, 2],
	[6, 6, 7]
)
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
