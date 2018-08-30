r"""
I modified one of the tests because I really think there problem with it (test_dead_end).
I posted an issue about that matter here:
    https://github.com/exercism/python/issues/1497

Some information about zippers and this implementation can be found here:
    https://github.com/cglacet/exercism-python/tree/master/zipper#implementation-hints-about-my-solution
"""
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
    def __init__(self, root=None, context=None):
        self.focus = root
        self.context = context or []

    @staticmethod
    def from_tree(dict_tree):
        return Zipper(BinaryTree.from_dict(dict_tree))

    def value(self):
        return self.focus.value

    def set_value(self, value):
        new_left = self.focus.left or None
        new_right = self.focus.right or None
        location = Zipper(BinaryTree(value, new_left, new_right), self.context)
        location.focus.value = value
        return location

    def insert(self, value):
        return Zipper(BinaryTree(value, None, None), self.context)

    def left(self):
        new_focus, new_context = self.focus.focus_left()
        # # Uncomment to pass the original `test_dead_end`:
        # if not new_focus:
            # return None
        return Zipper(new_focus, self.context+[new_context])

    def set_left(self, left_tree_dict):
        location = Zipper(self.focus, self.context)
        location.focus.left = BinaryTree.from_dict(left_tree_dict)
        return location

    def right(self):
        new_focus, new_context = self.focus.focus_right()
        # # Uncomment to pass the original `test_dead_end`:
        # if not new_focus:
        #     return None
        return Zipper(new_focus, self.context+[new_context])

    def set_right(self, right_tree_dict):
        location = Zipper(self.focus, self.context)
        location.focus.right = BinaryTree.from_dict(right_tree_dict)
        return location

    def up(self):
        last_context = self.context[-1]
        previous_focus = last_context.reattach(self.focus)
        return Zipper(previous_focus, self.context[:-1])

    def to_tree(self):
        zipper = Zipper(self.focus, self.context)
        while zipper.context:
            zipper = zipper.up()
        return BinaryTree.to_dict(zipper.focus)

    def __repr__(self):
        context_str = '('+'), ('.join(map(str, self.context))+')'
        return f"focus:\n{self.focus}\ncontext:[\n{context_str}\n]"
