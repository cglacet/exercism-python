from enum import Enum, unique


class TreeNode(object):
    def __init__(self, data=None, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

    def __str__(self):
        fmt = 'TreeNode(data={}, left={}, right={})'
        return fmt.format(self.data, self.left, self.right)


@unique
class TraversalOrder(Enum):
    PRE = 1
    IN = 2
    POST = 3


class BinarySearchTree(object):
    def __init__(self, tree_data):
        if len(tree_data) < 1:
            raise ValueError("Need at least one value to build a tree.")
        self.tree = TreeNode(tree_data[0])
        for value in tree_data[1:]:
            self.insert(value)

    def __repr__(self):
        return str(self.tree)

    def DFS(self, order):
        """DFS (Depth-first search) traversal in the given `order`.
        The `order` can be one of `TraversalOrder.PRE`, `TraversalOrder.IN`, `TraversalOrder.POST`.
        The traversal order doesn't change the way the tree is explored, but only the moment at which
        a traversed node is processed (note that each node is traversed exaclty 3 times):
            - pre-order: a node is processed as soon as it is traversed;
            - in-order: a node is precessed when the left (=min) subtree has been fully explored;
            - post-order: a node is processed when the its subtree has been fully explored;
        Note that traversing a BST (BinarySearchTree) in `IN` order result in processing
        nodes in sorted value order.
        """
        if order not in TraversalOrder:
            raise ValueError("You must define an `order` for the `DFS` , any of", TraversalOrder)

        cursor_stack = [(self.tree, TraversalOrder.PRE)]
        while len(cursor_stack) > 0:
            cursor, cursor_order = cursor_stack[-1]
            if order == cursor_order:
                yield cursor.data

            if cursor_order == TraversalOrder.PRE:
                cursor_stack[-1] = (cursor, TraversalOrder.IN)
                if cursor.left:
                    cursor_stack.append((cursor.left, TraversalOrder.PRE))
            elif cursor_order == TraversalOrder.IN:
                cursor_stack[-1] = (cursor, TraversalOrder.POST)
                if cursor.right:
                    cursor_stack.append((cursor.right, TraversalOrder.PRE))
            elif cursor_order == TraversalOrder.POST:
                cursor_stack.pop()

    def find(self, value):
        """Find a node that has the best matching data for `value` in the BST.
        If the `value` exists in the tree, then the deepest occurence of it is returned.
        It the `value` isn't part of the tree, then it returns what would be a valid parent
        for insertion of a new node having `value` as data.
        """
        parent = None
        cursor = self.tree
        while cursor:
            if cursor.data >= value:
                parent, cursor = cursor, cursor.left
            else:
                parent, cursor = cursor, cursor.right
        return parent

    def insert(self, value):
        parent = self.find(value)
        child = TreeNode(value)
        if parent.data >= value:
            parent.left = child
        else:
            parent.right = child

    def data(self):
        return self.tree

    def sorted_data(self):
        return list(self.DFS(TraversalOrder.IN))

if __name__ == "__main__":
    t = BinarySearchTree(['2', '1', '3', '6', '7', '5'])

    DFS_preorder = list(t.DFS(TraversalOrder.PRE))
    DFS_expected_preorder = ['2', '1', '3', '6', '5', '7']
    assert(DFS_preorder == DFS_expected_preorder)
    print("DFS (pre-order) = ", DFS_preorder)

    DFS_inorder = list(t.DFS(TraversalOrder.IN))
    DFS_expected_inorder = ['1', '2', '3', '5', '6', '7']
    assert(DFS_inorder == DFS_expected_inorder)
    print("DFS (in-order) = ", DFS_inorder)

    DFS_postorder = list(t.DFS(TraversalOrder.POST))
    DFS_expected_postorder = ['1', '5', '7', '6', '3', '2']
    assert(DFS_postorder == DFS_expected_postorder)
    print("DFS (post-order) = ", DFS_postorder)

    print(t.find('11'))
