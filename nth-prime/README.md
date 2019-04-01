# Computing the Nth-Prime

## Description from Exercism.io

Given a number n, determine what the nth prime is.

By listing the first six prime numbers: 2, 3, 5, 7, 11, and 13, we can see that
the 6th prime is 13.

If your language provides methods in the standard library to deal with prime
numbers, pretend they don't exist and implement them yourself.

## Remarks on the implementation

I tried my best to have something as optimal as I could, any comment is welcome :).

I focused on speed and sacrificed memory (memoization of previously computed primes).
This solution works well even for incremental requests, for example both: `[nth_prime(n) for n in range(1, 1001)]`
and `nth_prime(1000)` have very similar executions as they will both call `has_factor_in` the same
number of times. Execution times for these two on my machine are the following:

```python
def test():
    nth_prime = prime_finder()
    nth_prime(1000)

%timeit test()
# 9.72 ms ± 84.3 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
```

```python
def test():
    nth_prime = prime_finder()
    [nth_prime(n) for n in range(1, 1001)]

%timeit test()
#10.5 ms ± 124 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
```

Any subsequent request for a smaller `n` would be served in constant time (reading in the `primes` dictionary).

The inner algorithm for finding one prime, is actually quite simple, it iterates through the
odd numbers until enough primes are found.

For each odd number `x` it checks if `x` has any factor amongst the smaller primes, if it
doesn't have one, then by definition `x` prime number: every non-prime (composite) number
can be decomposed in prime factors.

I simply use the fact that one of these factors is necessarily smaller than the number itself.
More precisely, inside `has_factor_in` there is one optimization (lines 27-28) that uses the
fact that at least one prime factor of `x` is smaller than `sqrt(x)`.

**Proof** Suppose that `x` is a composite number for which the smallest prime factor is `p1 > sqrt(x)`.
Since `x` has several factors, it has at least one factor `p2 > p1`. Since both `p1` and `p2` are
greater than `sqrt(x)` the factorisation `p1*p2*...` is greater than `x`, a contradiction. QED.

As always the code is [here](nth_prime.py).

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

- Python 2.7: `py.test nth_prime_test.py`
- Python 3.4+: `pytest nth_prime_test.py`

Alternatively, you can tell Python to run the pytest module (allowing the same command to be used regardless of Python version):
`python -m pytest nth_prime_test.py`

### Common `pytest` options

- `-v` : enable verbose output
- `-x` : stop running tests on first failure
- `--ff` : run failures from previous test before running other test cases

For other options, see `python -m pytest -h`

## Submitting Exercises

Note that, when trying to submit an exercise, make sure the solution is in the `$EXERCISM_WORKSPACE/python/nth-prime` directory.

You can find your Exercism workspace by running `exercism debug` and looking for the line that starts with `Workspace`.

For more detailed information about running tests, code style and linting,
please see [Running the Tests](http://exercism.io/tracks/python/tests).

## Source

A variation on Problem 7 at Project Euler [http://projecteuler.net/problem=7](http://projecteuler.net/problem=7)

## Submitting Incomplete Solutions

It's possible to submit an incomplete solution so you can see how others have completed the exercise.
