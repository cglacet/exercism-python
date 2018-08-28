""" This is an exercise from https://exercism.io/my/tracks/python

Refs. I used to implement this:
     - https://ferd.ca/yet-another-article-on-zippers.html
     - http://blog.ezyang.com/2010/04/you-could-have-invented-zippers/
     - https://www.youtube.com/watch?v=Xdc7NkgfIgQ

I tried to stick to name notations used there in these, but some things change names
so be ready to get confused xD.
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
            print(tree)
        return Tree.to_dict(tree)

    def __repr__(self):
        context_str = '('+'), ('.join(map(str, self.context))+')'
        return f"focus:\n{self.focus}\ncontext:[\n{context_str}\n]"


def bt(value, left, right):
    return {
        'value': value,
        'left': left,
        'right': right
    }

def leaf(value):
    return bt(value, None, None)

# # Test the Tree class:
# t1 = bt("a", bt("b", bt("d", leaf("x"), leaf("y")), leaf("e")), bt("c", leaf("f"), leaf("h")))
# t = Tree.from_dict(t1)
# print(t)
# print("-"*15)
#
# focus_l, t_l = t.focus_left()
# print(f"L focus is\n{focus_l}\ncontext is [\n{t_l}\n]")
# print("-"*15)
#
# focus_ll, t_ll = focus_l.focus_left()
# print(f"L L focus is\n{focus_ll}\ncontext is [\n({t_l}), \n({t_ll})\n]")
# print("-"*15)
#
# focus_llr, t_llr = focus_ll.focus_right()
# print(f"L L R focus is\n{focus_llr}\ncontext is [\n({t_l}), \n({t_ll}), \n({t_llr})\n]")
# print("-"*15)
#
# tree = focus_llr
# context = [t_l, t_ll, t_llr]
# while context:
#     c = context.pop()
#     tree = c.attach_to_pending_branch(tree)
#
# print(tree) # this should be equal to t

# # Tests cases for zipper:
#t1 = bt("a", bt("b", bt("d", leaf("x"), leaf("y")), leaf("e")), bt("c", leaf("f"), leaf("h")))
t1 = bt(1, bt(2, None, leaf(3)), leaf(4))
zipper = Zipper.from_tree(t1)
print(zipper)
z = zipper.left().right()
print(z)
new_t1 = z.to_tree()

import unittest
print(t1)
print(new_t1)
print(t1 == new_t1)
