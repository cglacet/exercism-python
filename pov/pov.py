"""This is an exercise from https://exercism.io/my/tracks/python"""
from textwrap import indent
from copy import deepcopy


class Tree:
    """A Tree is defined by it's label and by a (potentially empty) list of children Tree."""
    def __init__(self, label, children=None):
        self.label = label
        self.children = children or []
        # Is this considered cheating?
        self.parent = None
        for child in self.children:
            child.parent = self

    def from_pov(self, from_node_label):
        """Return a new tree rotated in such a way that `from_node` is the new root."""
        # OR `new_tree = self`? Not too sure what is expected here.
        new_tree = deepcopy(self)
        root = new_tree.find(from_node_label)

        current_node = root
        old_parent = new_parent = None
        # Going up toward the current root, for each node on this path:
        #    (1) redirect its parent to the previous node on the path
        #    (2) remove its new parent from its children list,
        #    (3) add its old parent to its children list,
        while current_node:
            # (1)
            old_parent = current_node.parent
            current_node.parent = new_parent

            # (2)
            children = [child for child in current_node if id(child) != id(new_parent)]
            # (3)
            if old_parent:
                children += [old_parent]

            current_node.children = children
            new_parent, current_node = current_node, old_parent

        return root

    def original_path_to(self, from_node_label, to_node_label):
        """Returns the list of nodes that lies on the shortest path from the node
        with label `from_node_label` to the node with label `to_node_label`. A
        `ValueError` is raised if such a path doesn't exist.
        """
        tree = self.from_pov(to_node_label)
        node = tree.find(from_node_label)
        return list(node.path_labels_to_root())

    def other_path_to(self, from_node_label, to_node_label):  # Faster version
        """Returns the list of nodes that lies on the shortest path from the node
        with label `from_node_label` to the node with label `to_node_label`. A
        `ValueError` is raised if such a path doesn't exist.
        """
        from_node = self.find(from_node_label)
        to_node = self.find(to_node_label)
        from_node_to_root = list(from_node.path_labels_to_root())
        to_node_to_root = list(to_node.path_labels_to_root())
        common_ancestor_index = -1
        try:
            while from_node_to_root[common_ancestor_index-1] == to_node_to_root[common_ancestor_index-1]:
                common_ancestor_index -= 1
        except IndexError:
            pass
        first_common_ancestor_index = common_ancestor_index
        fca = from_node_to_root[first_common_ancestor_index]
        from_node_to_fca = from_node_to_root[:first_common_ancestor_index]
        from_fca_to_node = to_node_to_root[:first_common_ancestor_index][::-1]
        return from_node_to_fca + [fca] + from_fca_to_node

    path_to = original_path_to

    def path_labels_to_root(self):
        """Iterate through nodes in the shortest path from any `node` to the root."""
        node = self
        while node:
            yield node.label
            node = node.parent

    def BFS(self):
        """A BFS that iterates over all nodes, children order is the one defined
        while creating the nodes.
        """
        yield self
        next_level = [self]
        while next_level:
            for node in next_level.pop():
                next_level.append(node)
                yield node

    def find(self, node_label):
        """Returns the first node with label `node_label` encountered in BFS traversal."""
        for node in self.BFS():
            if node.label == node_label:
                return node
        raise ValueError(f"no such node {node_label}")

    def __iter__(self):
        for child in self.children:
            yield child

    def __str__(self):
        text = str(self.label)
        if self.children:
            repr_function = Tree._repr_node(len(self.children))
            children_text = map(repr_function, enumerate(self.children))
            text += indent('\n'+"\n".join(children_text), '│   ')
        return text

    @staticmethod
    def _repr_node(length):
        def repr(enum_value):
            index, node = enum_value
            if index == length-1:
                return "└───"+str(node)
            else:
                return "├───"+str(node)
        return repr

    def __lt__(self, other):
        try:
            return self.label < other.label
        except AttributeError:
            raise TypeError(f"{type(other)} can't be compared to {type(self)}.")

    def __eq__(self, other):
        try:
            return self.children == other.children
        except AttributeError:
            return False

    @staticmethod
    def generate(arrity, depth, initial_value=""):
        if depth == 0:
            return Tree(initial_value)
        children = [Tree.generate(arrity, depth-1, initial_value+str(i+1)) for i in range(arrity)]
        return Tree(initial_value or "root", children)

if __name__ == "__main__":
    import timeit
    TEST_TREE = Tree.generate(3, 3)
    print(TEST_TREE)
    #print(TEST_TREE.from_pov('31'))

    for path_to in [TEST_TREE.original_path_to, TEST_TREE.other_path_to]:
        TEST_TREE.path_to = path_to
        print(f'Path to method set to "{path_to.__name__}"')
        print(TEST_TREE.path_to('31', '133'))
        print(TEST_TREE.path_to('31', '321'))

    # I don't know if I can merge this with the above loop, that would look better though:
    TEST_CALL = "TEST_TREE.path_to('31', '321')"
    print(f'Duration for "{TEST_CALL}"')
    for path_to in ["original_path_to", "other_path_to"]:
        setup = f'from __main__ import Tree\nTEST_TREE = Tree.generate(3, 3)\nTEST_TREE.path_to = TEST_TREE.{path_to}'
        duration = timeit.timeit(TEST_CALL, setup=setup, number=1000)
        print(f'\t - {duration:.4f} with "{path_to}"')
