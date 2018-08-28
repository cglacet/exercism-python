r"""References I used to implement this (I tried to stick to name notations used there in
these, but I'm new to this concept so things may have been mixed up):
    - [1] Why do we even need such a data structure? A clear starting point:
        http://blog.ezyang.com/2010/04/you-could-have-invented-zippers/
    - [2] The "Zipper Binary Trees" part gives some interesting hints on implementation:
        https://ferd.ca/yet-another-article-on-zippers.html
    - [3] Even more details, this time with any arity trees:
        https://www.youtube.com/watch?v=Xdc7NkgfIgQ

One very important thing here is that we want a data structure that is immutable.
Otherwise this whole thing would have no sense as in place insertion/deletion in
trees work perfectly fine using only classic data structure.

If you understand why we need such a data structure ([1] explains it very well, I think
I couldn't add anything valuable to it), here is my (novice) definition of what a zipper
(for binary tree) is and how why we will implement it this way.

A zipper is a soft destruction of a given binary tree T. It's a destruction as the structure
of the tree is not directly accessible from the zipper. It's a soft destruction as T can be
reconstructed efficiently from the zipper. The deconstruction represents a step-by-step map
of a journey within the input tree T that is complete enough so no information is lost in the
process.

Consider the input graph T=a:

              a
           /     \
         b         c
       /   \     /   \
      d     e   f     g
     / \
    x   y

A journey always starts from the root (a) and simply is a list of steps, either a Left-step
or a Right-step, Up-step (choosing from the current node 2 children (L, R) or parent (U)).
Lets represent a journey by the list of steps: J = (L, L, R, U, R) taken. This journey
ends on node y.

Lets see how this journey will deconstruct T in a zipper form Z and how we can retrieve
T from Z. The zipper data structure will consist of a sub-tree (representing the part
of the tree that can be explored without ever going Up), and a contexts list (containing
all necessary information required to explore the rest of the tree).

Let's proceed by iterating on the journey's length.
  (0) First, if no step was taken, then the journey is empty J = (), which means that
  we can go anywhere in the tree from there without ever going Up. Therefore the
  zipper Z is equal to:
        - sub-tree = T
        - contexts = []
  (1) We now have stepped in the tree, our first programmed step was L. Our journey is
  J = (L). This lead us to node b, from there, without going Up, we can only go to this
  sub-tree:

           b
         /   \
        d     e
       / \
      x   y

  and if we want to be able to visit the whole tree T without any external information
  we need to store what is above, ie., the "context":

                   a
                   |
                   c
                 /   \
                f     g

  But if we store only this information, we wont be able to reconstruct T, as we forgot
  to mention which edge with just took when going Left from a. We need to remember that we
  went down using the Left edge! Otherwise we wouldn't know in which of these two graphs
  we are:
                          a                              a
                       /     \                        /     \
                     b         c                    c         b
                   /   \     /   \                /   \     /   \
                  d     e   f     g              f     g   d     e
                 / \                                      / \
                x   y                                    x   y

  We will thus store this as a the first item of our contexts list:

              a
           /     \
         .         c
                 /   \
                f     g

  I'll represent contexts like this, but this simply mean we added the extra information
  about where we went down to the partial sub-tree from before:

                   a                                           a
                   |                                        /     \
                   c           +     Left         =       .         c
                 /   \                                            /   \
                f     g                                          f     g

  Now we know where to attach the sub-tree rooted at b (ie., replace '.' by the tree sub-rooted at b).
  Phew! To sum-up, zipper Z is now equal to:
    - sub-tree =
                b
              /   \
             d     e
            / \
           x   y
    - contexts = [
              a
           /     \
         .         c
                 /   \
                f     g
      ]

  (2) Now that you got the idea, we can go faster. Remember that the final journey
  is J = (L, L, R, U, R). After 2 steps, the journey is J = (L, L). To compute the
  zipper, just mimic step (1) and deconstruct the sub-tree while saving the upward
  part in the contexts list. The zipper Z will look like this:
    - sub-tree =
            d
           / \
          x   y
    - contexts = [
          a
       /     \
     .         c        ,     b
             /   \           /
            f     g         e
    ]

  (3) After 3 steps, the journey is J = (L, L, R) and the zipper is:
     - sub-tree = y
     - contexts = [
           a                                               Notice how the '.' is going deeper and deeper
        /     \                                            because I aligned contexts on their original dept
      .         c        ,      b      ,                       <-- step 1
              /   \           /   \
             f     g         e     .          d                <-- step 2
                                             / \
                                            x   .              <-- step 3
     ]                                                     (we are not allowed to use that information, I just
                                                            added this so you can see the evolution of the position
                                                            during the journey)

  (4) Step 4 is a new kind of step, it's going Up, the journey is J = (L, L, R, U).
  Going up, simply means "reconstruct to previous step" or "cancel pleas!" also known
  as "ctrl + z". In order to reconstruct from a zipper Z, we simply need to invert actions
  we made when going down. Which means: (i) Extract the last context from the contexts list,
  call it c, (ii) Define the new sub-tree to be sub-tree attached to c (on the right side).
  We already demonstrate that this would indeed re-construct the graph (we designed it
  so this could work! Details in step (1)). The sub-tree operation (ii) is the following:

                                        d                      d
      reattach     y      to           / \        =           / \
                                      x   .                  x   y

  The zipper Z is:
    - sub-tree =
            d
           / \
          x   y
    - contexts = [
          a
       /     \
     .         c        ,     b
             /   \           /
            f     g         e
    ]
  Which is the same as in step (2).

  (5) Is the exact same as step (3).

In order to retrieve T from Z, we only need to repeat Up operations until the root is
reached (until contexts list is empty).
"""
from textwrap import indent


class Tree:
    def __init__(self, value, left, right):
        self.value = value
        self.left = left
        self.right = right

    @staticmethod
    def from_dict(dict_tree):
        if not dict_tree:
            return None
        return Tree(
            dict_tree['value'],
            Tree.from_dict(dict_tree['left']),
            Tree.from_dict(dict_tree['right']))

    def focus_left(self):
        return self.left, Context(self.value, None, self.right, is_left=True)

    def focus_right(self):
        return self.right, Context(self.value, self.left, None)

    @staticmethod
    def to_dict(tree):
        if not tree:
            return None
        return {
            'value': tree.value,
            'left':  Tree.to_dict(tree.left),
            'right': Tree.to_dict(tree.right)}

    def __repr__(self):
        text = str(self.value)
        if self.left:
            text += '\n L:' + indent(str(self.left), '  ')
        if self.right:
            text += '\n R:' + indent(str(self.right), '  ')
        return text


class Context(Tree):
    def __init__(self, value, left, right, is_left=False):
        self.is_left = is_left
        super().__init__(value, left, right)

    def reattach(self, tree):
        if self.is_left:
            return Tree(self.value, tree, self.right)
        else:
            return Tree(self.value, self.left, tree)


class Zipper:
    def __init__(self, root, context=None):
        self.focus = root
        self.context = context or []

    @staticmethod
    def from_tree(dict_tree):
        return Zipper(Tree.from_dict(dict_tree))

    def value(self):
        return self.focus.value

    def set_value(self, value):
        location = Zipper(self.focus, self.context)
        location.focus.value = value
        return location

    def left(self):
        new_focus, new_context = self.focus.focus_left()
        if not new_focus:
            return None
        return Zipper(new_focus, self.context+[new_context])

    def set_left(self, left_tree_dict):
        location = Zipper(self.focus, self.context)
        location.focus.left = Tree.from_dict(left_tree_dict)
        return location

    def right(self):
        new_focus, new_context = self.focus.focus_right()
        if not new_focus:
            return None
        return Zipper(new_focus, self.context+[new_context])

    def set_right(self, right_tree_dict):
        location = Zipper(self.focus, self.context)
        location.focus.right = Tree.from_dict(right_tree_dict)
        return location

    def up(self):
        last_context = self.context.pop()
        previous_focus = last_context.reattach(self.focus)
        return Zipper(previous_focus, self.context)

    def to_tree(self):
        tree = self.focus
        while self.context:
            c = self.context.pop()
            tree = c.reattach(tree)
        return Tree.to_dict(tree)

    def __repr__(self):
        context_str = '('+'), ('.join(map(str, self.context))+')'
        return f"focus:\n{self.focus}\ncontext:[\n{context_str}\n]"
