# Zipper

Creating a zipper for a binary tree.

[Zippers](https://en.wikipedia.org/wiki/Zipper_%28data_structure%29) are
a purely functional way of navigating within a data structure and
manipulating it.  They essentially contain a data structure and a
pointer into that data structure (called the focus).

For example given a rose tree (where each node contains a value and a
list of child nodes) a zipper might support these operations:

- `from_tree` (get a zipper out of a rose tree, the focus is on the root node)
- `to_tree` (get the rose tree out of the zipper)
- `value` (get the value of the focus node)
- `prev` (move the focus to the previous child of the same parent,
  returns a new zipper)
- `next` (move the focus to the next child of the same parent, returns a
  new zipper)
- `up` (move the focus to the parent, returns a new zipper)
- `set_value` (set the value of the focus node, returns a new zipper)
- `insert_before` (insert a new subtree before the focus node, it
  becomes the `prev` of the focus node, returns a new zipper)
- `insert_after` (insert a new subtree after the focus node, it becomes
  the `next` of the focus node, returns a new zipper)
- `delete` (removes the focus node and all subtrees, focus moves to the
  `next` node if possible otherwise to the `prev` node if possible,
  otherwise to the parent node, returns a new zipper)

## Solution

References I used to implement this (I tried to stick to name notations used there in
these, but I'm new to this concept so things may have been mixed up):

- [[1] Why do we even need such a data structure? A clear starting point](http://blog.ezyang.com/2010/04/you-could-have-invented-zippers/).
- [[2] The "Zipper Binary Trees" part gives some interesting hints on implementation](https://ferd.ca/yet-another-article-on-zippers.html).
- [[3] Even more details, this time with any arity trees](https://www.youtube.com/watch?v=Xdc7NkgfIgQ)

One very important thing here is that we want a data structure that is immutable.
Otherwise this whole thing would have no sense as in place insertion/deletion in
trees work perfectly fine using only classic data structure.

If you understand why we need such a data structure ([[1]](http://blog.ezyang.com/2010/04/you-could-have-invented-zippers/)
explains it very well, I think I couldn't add anything valuable to it), here is my
(novice) definition of what a zipper (for binary tree) is and how why we will implement
it this way.

A (binary-tree)-zipper is a soft destruction of a given binary tree `T`. It's a destruction as the structure
of the tree is not directly accessible from the zipper. It's a soft destruction as `T` can be
reconstructed efficiently from the zipper. The deconstruction represents a step-by-step map
of a journey within the input tree `T` that is complete enough so no information is lost in the
process.

Consider the input graph `T=a`:
```
              a
           /     \
         b         c
       /   \     /   \
      d     e   f     g
     / \
    x   y
```

A journey always starts from the root (a) and simply is a list of steps, either a Left-step
or a Right-step, Up-step (choosing from the current node 2 children (L, R) or parent (U)).
Lets represent a journey by the list of steps: J = (L, L, R, U, R) taken. This journey
ends on node y.

Lets see how this journey will deconstruct `T` in a zipper form `Z` and how we can retrieve
`T` from `Z`. The zipper data structure will consist of a `sub-tree` (representing the part
of the tree that can be explored without ever going Up), and a `contexts` list (containing
all necessary information required to explore the rest of the tree).

Let's proceed by iterating on the journey's length.
  (0) First, if no step was taken, then the journey is empty J = (), which means that
  we can go anywhere in the tree from there without ever going Up. Therefore the
  zipper `Z` is equal to:
```
sub-tree = T
contexts = []
```
  (1) We now have stepped in the tree, our first programmed step was L. Our journey is
  J = (L). This lead us to node b, from there, without going Up, we can only go to this
  sub-tree:

```
           b
         /   \
        d     e
       / \
      x   y
```

  and if we want to be able to visit the whole tree T without any external information
  we need to store what is above, ie., the "context":

```
                   a
                   |
                   c
                 /   \
                f     g
```

  But if we store only this information, we wont be able to reconstruct T, as we forgot
  to mention which edge with just took when going Left from a. We need to remember that we
  went down using the Left edge! Otherwise we wouldn't know in which of these two graphs
  we are:
```
                          a                              a
                       /     \                        /     \
                     b         c                    c         b
                   /   \     /   \                /   \     /   \
                  d     e   f     g              f     g   d     e
                 / \                                      / \
                x   y                                    x   y
```

  We will thus store this as a the first item of our contexts list:

```
              a
           /     \
         .         c
                 /   \
                f     g
```

  I'll represent contexts like this, but this simply mean we added the extra information
  about where we went down to the partial sub-tree from before:

```
                   a                                           a
                   |                                        /     \
                   c           +     Left         =       .         c
                 /   \                                            /   \
                f     g                                          f     g
```

  Now we know where to attach the sub-tree rooted at b (ie., replace '.' by the tree sub-rooted at b).
  Phew! To sum-up, zipper `Z` is now equal to:

```
sub-tree =
                b
              /   \
             d     e
            / \
           x   y
contexts = [
              a
           /     \
         .         c
                 /   \
                f     g
]
```

  (2) Now that you got the idea, we can go faster. Remember that the final journey
  is J = (L, L, R, U, R). After 2 steps, the journey is J = (L, L). To compute the
  zipper, just mimic step (1) and deconstruct the sub-tree while saving the upward
  part in the contexts list. The zipper `Z` will look like this:

```
sub-tree =
            d
           / \
          x   y
contexts = [
          a
       /     \
     .         c        ,     b
             /   \           / \
            f     g         e   .
]
```

  (3) After 3 steps, the journey is J = (L, L, R) and the zipper is:

```
sub-tree = y
contexts = [
           a                                               Notice how the '.' is going deeper and deeper
        /     \                                            because I aligned contexts on their original depth
      .         c        ,      b      ,                       <-- step 1
              /   \           /   \
             f     g         e     .          d                <-- step 2
                                             / \
                                            x   .              <-- step 3
]                                                          (we are not allowed to use that information, I just
                                                            added this so you can see the evolution of the position
                                                            during the journey)
```

  (4) Step 4 is a new kind of step, it's going Up, the journey is J = (L, L, R, U).
  Going up, simply means "reconstruct to previous step" or "cancel pleas!" also known
  as "ctrl + z". In order to reconstruct from a zipper `Z`, we simply need to invert actions
  we made when going down. Which means: (i) Extract the last context from the contexts list,
  call it `c`, (ii) Define the new sub-tree to be sub-tree attached to c (on the right side).
  We already demonstrate that this would indeed re-construct the graph (we designed it
  so this could work! Details in step (1)). The sub-tree operation (ii) is the following:

```
                                        d                      d
      reattach     y      to           / \        =           / \
                                      x   .                  x   y
```

  The zipper `Z` is:

```
sub-tree =
            d
           / \
          x   y
contexts = [
          a
       /     \
     .         c        ,     b
             /   \           /
            f     g         e
    ]
```
  Which is the same as in step (2).

  (5) Is the exact same as step (3).

In order to retrieve `T` from `Z`, we only need to repeat Up operations until the root is
reached (until contexts list is empty).

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

- Python 2.7: `py.test zipper_test.py`
- Python 3.4+: `pytest zipper_test.py`

Alternatively, you can tell Python to run the pytest module (allowing the same command to be used regardless of Python version):
`python -m pytest zipper_test.py`

### Common `pytest` options

- `-v` : enable verbose output
- `-x` : stop running tests on first failure
- `--ff` : run failures from previous test before running other test cases

For other options, see `python -m pytest -h`

## Submitting Exercises

Note that, when trying to submit an exercise, make sure the solution is in the `$EXERCISM_WORKSPACE/python/zipper` directory.

You can find your Exercism workspace by running `exercism debug` and looking for the line that starts with `Workspace`.

For more detailed information about running tests, code style and linting,
please see [Running the Tests](http://exercism.io/tracks/python/tests).

## Submitting Incomplete Solutions

It's possible to submit an incomplete solution so you can see how others have completed the exercise.
