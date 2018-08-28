"""This is a part of an exercise from https://exercism.io/my/tracks/python"""
from textwrap import indent


class BinaryTree:
    def __init__(self, value, left, right):
        self.value = value
        self.left = left
        self.right = right

    @staticmethod
    def from_dict(dict_tree):
        if not dict_tree:
            return None
        return BinaryTree(
            dict_tree['value'],
            BinaryTree.from_dict(dict_tree['left']),
            BinaryTree.from_dict(dict_tree['right']))

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
            'left':  BinaryTree.to_dict(tree.left),
            'right': BinaryTree.to_dict(tree.right)}

    def __repr__(self):
        text = str(self.value)
        if self.left:
            text += '\n L:' + indent(str(self.left), '  ')
        if self.right:
            text += '\n R:' + indent(str(self.right), '  ')
        return text


class Context(BinaryTree):
    def __init__(self, value, left, right, is_left=False):
        self.is_left = is_left
        super().__init__(value, left, right)

    def reattach(self, tree):
        if self.is_left:
            return BinaryTree(self.value, tree, self.right)
        else:
            return BinaryTree(self.value, self.left, tree)


class Zipper:
    def __init__(self, root, context=None):
        self.focus = root
        self.context = context or []

    @staticmethod
    def from_tree(dict_tree):
        return Zipper(BinaryTree.from_dict(dict_tree))

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
        location.focus.left = BinaryTree.from_dict(left_tree_dict)
        return location

    def right(self):
        new_focus, new_context = self.focus.focus_right()
        if not new_focus:
            return None
        return Zipper(new_focus, self.context+[new_context])

    def set_right(self, right_tree_dict):
        location = Zipper(self.focus, self.context)
        location.focus.right = BinaryTree.from_dict(right_tree_dict)
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
        return BinaryTree.to_dict(tree)

    def __repr__(self):
        context_str = '('+'), ('.join(map(str, self.context))+')'
        return f"focus:\n{self.focus}\ncontext:[\n{context_str}\n]"
