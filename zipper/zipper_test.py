import unittest

from zipper import Zipper


# Tests adapted from `problem-specifications//canonical-data.json` @ v1.1.0

class ZipperTest(unittest.TestCase):
    def bt(self, value, left, right):
        return {
            'value': value,
            'left': left,
            'right': right
        }

    def leaf(self, value):
        return self.bt(value, None, None)

    def create_trees(self):
        t1 = self.bt(1, self.bt(2, None, self.leaf(3)), self.leaf(4))
        t2 = self.bt(1, self.bt(5, None, self.leaf(3)), self.leaf(4))
        t3 = self.bt(1, self.bt(2, self.leaf(5), self.leaf(3)), self.leaf(4))
        t4 = self.bt(1, self.leaf(2), self.leaf(4))
        return (t1, t2, t3, t4)

    def test_data_is_retained(self):
        t1, _, _, _ = self.create_trees()
        zipper = Zipper.from_tree(t1)
        tree = zipper.to_tree()
        self.assertEqual(tree, t1)

    def test_left_and_right_value(self):
        t1, _, _, _ = self.create_trees()
        zipper = Zipper.from_tree(t1)
        self.assertEqual(zipper.left().right().value(), 3)

    def test_dead_end(self):
        t1, _, _, _ = self.create_trees()
        zipper = Zipper.from_tree(t1)
        # I think this shouldn't be None as one might want to insert a node here!
        # self.assertIsNone(zipper.left().left())
        # I think the following makes more sense:
        with self.assertRaises(AttributeError):
            zipper.left().left().left()

    def test_tree_from_deep_focus(self):
        t1, _, _, _ = self.create_trees()
        zipper = Zipper.from_tree(t1)
        self.assertEqual(zipper.left().right().to_tree(), t1)

    def test_set_value(self):
        t1, t2, _, _ = self.create_trees()
        zipper = Zipper.from_tree(t1)
        updatedZipper = zipper.left().set_value(5)
        tree = updatedZipper.to_tree()
        self.assertEqual(tree, t2)

    def test_set_left_with_value(self):
        t1, _, t3, _ = self.create_trees()
        zipper = Zipper.from_tree(t1)
        updatedZipper = zipper.left().set_left(self.leaf(5))
        tree = updatedZipper.to_tree()
        self.assertEqual(tree, t3)

    def test_set_right_to_none(self):
        t1, _, _, t4 = self.create_trees()
        zipper = Zipper.from_tree(t1)
        updatedZipper = zipper.left().set_right(None)
        tree = updatedZipper.to_tree()
        self.assertEqual(tree, t4)

    def test_different_paths_to_same_zipper(self):
        t1, _, _, _ = self.create_trees()
        zipper = Zipper.from_tree(t1)
        self.assertEqual(zipper.left().up().right().to_tree(),
                         zipper.right().to_tree())

    def test_immutability_move_insert(self):
        z = Zipper().insert(1).right().insert(4).up().left().insert(2).left().insert(3).left()
        z_2 = z.insert(5)
        z_3 = z.insert(7)
        self.assertIs((z.focus is None), True)
        self.assertEqual(z.up().value(), 3)
        self.assertNotEqual(z_2.value(), z_3.value())

    def  test_immutability_change_whole_tree(self):
        z = Zipper().insert(1).right().insert(4).up().left().insert(2).left().insert(3).up().up()
        z_2 = Zipper().insert(1).right().insert(4).up().left().insert(2).left().insert(3).up().up()
        z.set_value(2).right().set_value(8).up().left().set_value(4).left().set_value(6).up().up()
        self.assertEqual(z.value(), z_2.value())
        self.assertEqual(z.right().value(), z_2.right().value())
        self.assertEqual(z.right().up().left().value(), z_2.right().up().left().value())
        self.assertEqual(z.right().up().left().left().value(), z_2.right().up().left().left().value())
        self.assertEqual(z.right().up().left().up().value(), z_2.right().up().left().up().value())

    def test_immutability_set_value(self):
        z = Zipper().insert(1).right().insert(4).up().left().insert(2).left().insert(3)
        z_2 = z.set_value(5)
        self.assertEqual(z.value(), 3)
        self.assertEqual(z_2.value(), 5)

if __name__ == '__main__':
    unittest.main()
