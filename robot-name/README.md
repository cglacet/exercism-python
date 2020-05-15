# Robot Name

Manage robot factory settings.

When robots come off the factory floor, they have no name.

The first time you boot them up, a random name is generated in the format
of two uppercase letters followed by three digits, such as RX837 or BC811.

Every once in a while we need to reset a robot to its factory settings,
which means that their name gets wiped. The next time you ask, it will
respond with a new random name.

The names must be random: they should not follow a predictable sequence.
Random names means a risk of collisions. Your solution must ensure that
every existing robot has a unique name.

## Remarks on the solution

Following a discussion on Slack:

> - JP: "I'm not sure I understand the true point of this exercise yet.
> Is this really about the sample() call in the random library?
> Or do we expect solutions to keep track of every name assigned?
> I see a great many calls in the test cases, but not enough to beat
> out the odds of just picking a new name at random."
>
> - IH: "You know I had the same wonder. It seemed like the tests
> were pointing to random.seed, but that doesn't guarantee uniqueness
> so I wasn't sure what main idea I was supposed to take away.

Using random names doesn't imply relying on these names to guarantee uniqueness.
Actually finding a clean way to guarantee uniqueness with homogeneous probability
distribution in an effective way is not that easy. Depending of course on the
number of robots you have, in the case of this exercise, since the number of robot
is extremely small, the solution can be as simple as:

```python
while name in Robot.names_used:
    name = Robot.rand_name()
```

In a real example you couldn't do that as the more robots you would get, the more
collisions you would have, imagine that there only is one name left, you would
have to repeat this roughly n log n times to have a close to 100% chance of having
a unique name. Which in this case means something in the order of 7 million times.
Not the ideal algorithm to find a random name ^^. On the other hand if you don't
do this then it's a bit hard (in the sense that we probably don't expect that for this exercise)
to guarantee that all (free) names have equal probability of being given to a new robot.

While this is not part of the test, I guess that if you find someone that looks to be
good enough you can still ask a question on that matter. Thus proposing a harder version of the problem.

## Complexity analyses

> This answer is a bit contrary to the spirit of the problem, but it's more satisfactory to me than the trial-and-error approach. After initial overhead, it runs in constant time, while the other (more standard?) approach gets slower and slower as more names are selected.

I don't totally agree with that, there are basically two cases 1) the number of robots R is small compared to the number of names N, 2) the number of robots is approaching the number of names.

In case 1) the _trial-and-error approach_ is more or less in constant time, as the probability of having two collisions in a row is very small (for example R/(N+R) = O(log N/N) for R = log N, with our number this is ~2e-5). So the overall probability of having this happen R times is basically 0 (7e-64) which means that in almost all cases you will have less than 2R names to pick. (ie., the probability that you have to pick more than 2R names is 7e-64). This probability increases as N grows, which means this strategy is in O(R) for picking R names.

In this case, your strategy is in O(N).

In case 2) As R tends to N the trial and error approaches the coupon collector problems and therefore the overall number of names to produce tends toward R*H_N (basically O(R log N). THe problem of course is that names are not acquired at equal speed, and the R-th name require more or less O(N) tries.

In this case your current strategy is still O(N) but you will fail to re-allow old released names to new robot, which means that you will have to refresh your list at some point. That's not that hard to add, I think the best solution would be to put released names at some random location in `names` (which mean you won't be able to have an iterator).

But note that there is a tradeoff between memory and time, trial-and-error has a time complexity of roughly O(R log N) but memory O(1), your solution has time in O(N), but memory also is O(N).

I think in real life I would increase N and always favor solution 1.


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

- Python 2.7: `py.test robot_name_test.py`
- Python 3.4+: `pytest robot_name_test.py`

Alternatively, you can tell Python to run the pytest module (allowing the same command to be used regardless of Python version):
`python -m pytest robot_name_test.py`

### Common `pytest` options

- `-v` : enable verbose output
- `-x` : stop running tests on first failure
- `--ff` : run failures from previous test before running other test cases

For other options, see `python -m pytest -h`

## Submitting Exercises

Note that, when trying to submit an exercise, make sure the solution is in the `$EXERCISM_WORKSPACE/python/robot-name` directory.

You can find your Exercism workspace by running `exercism debug` and looking for the line that starts with `Workspace`.

For more detailed information about running tests, code style and linting,
please see [Running the Tests](http://exercism.io/tracks/python/tests).

## Source

A debugging session with Paul Blackwell at gSchool. [http://gschool.it](http://gschool.it)

## Submitting Incomplete Solutions

It's possible to submit an incomplete solution so you can see how others have completed the exercise.
