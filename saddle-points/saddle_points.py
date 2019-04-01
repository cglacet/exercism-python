"""This is an exercise from https://exercism.io/my/tracks/python

The goal is to find Saddle points in a matrix.
For an input matrix M, a cell (i, j) of M is said to be a "Saddle point" if
the cell's value is greater than or equal to every element in its row and
less than or equal to every element in its column:

        M[i,j] >= M[c,j] | c any column index of M
    and M[i,j] <= M[i,r] | r any row index of M

For example, with an input matrix M, the only Saddle point is on cell M[1, 0] = "5":
  [ 9 8 7 ]
  [ 5 3 2 ]
  [ 6 6 7 ]

The internal process used to find Saddle points is located in function `saddle_points`
and apply the following steps:

Finding "row's max.", a column vector equal to [9, 5, 7], and use if to compute a boolean
matrix in which each cell (i,j) is `True` if this cell's value is the maximum value of
its own row. This second operation is done using `flag_projected_matches`:
      [ 9 ]      flag_projected_matches     [ 9 8 7 ]    =   [ O . . ]
      [ 5 ]                                 [ 5 3 2 ]        [ O . . ]     =    A
      [ 7 ]                                 [ 6 6 7 ]        [ . . O ]

                                                      ("O" match, "." otherwise)

The same is done for "column's min.", we first compute the row vector representing min.
column values and then compute the boolean mask using `flag_projected_matches`:
    [ 5 3 2 ]    flag_projected_matches     [ 9 8 7 ]    =   [ . . . ]
                                            [ 5 3 2 ]        [ O O O ]    =     B
                                            [ 6 6 7 ]        [ . . . ]

Once we have these two boolean matrix, in order to find Saddle points we just need
to find cells for which both conditions (A and B) are met (using the logical `&` operator):
  [ O . . ]     &     [ . . . ]   =   [ . . . ]
  [ O . . ]           [ O O O ]       [ O . . ]
  [ . . O ]           [ . . . ]       [ . . . ]

Finally, Saddle points coordinates are retrieved using the `where` method on this last matrix:
          [ . . . ]
  where   [ O . . ]   =   {(1, 0)}
          [ . . . ]
"""
from enum import Enum
from collections import namedtuple
from textwrap import indent


def saddle_points(data):
    """A "saddle point" is greater than or equal to every element in its row
    and less than or equal to every element in its column.
    """
    matrix = Matrix2D(data)
    rows_maximums = matrix.axis_reduce(Matrix2D.Axes.ROW, max)
    is_max_in_row = matrix.flag_projected_matches(rows_maximums)
    columns_minimums = matrix.axis_reduce(Matrix2D.Axes.COLUMN, min)
    is_min_in_col = matrix.flag_projected_matches(columns_minimums)
    is_saddle = is_max_in_row & is_min_in_col
    saddle_indexes = set(is_saddle.where())

    print("Input matrix is: \n{}".format(matrix))
    print("Row's max locations: \n{}".format(is_max_in_row))
    print("Columns's min locations: \n{}".format(is_min_in_col))
    print("Saddle points locations: \n{}".format(is_saddle))
    print("Saddle points are at indexes: \n{}".format(saddle_indexes))

    return saddle_indexes


Coordinates = namedtuple('Coordinates', ['x', 'y'])
Shape = namedtuple('Shape', ['row', 'column'])


class RowVector(list):
    """An orientation aware list."""
    def is_matrix_compatible(self, matrix):
        """Returns `True` if the input `matrix` has the same row shape as the `RowVector`."""
        return matrix.shape.column == len(self)

    @staticmethod
    def projected_coordinates(coordinates):
        """Returns the 1D coordinates projected any multidimensional coordinates in the `RowVector`'s space."""
        return coordinates.y

    def __repr__(self):
        return Matrix2D.repr([self])


class ColumnVector(list):
    """An orientation aware list."""
    def is_matrix_compatible(self, matrix):
        """Returns `True` if the input `matrix` has the same colum shape as the `ColumnVector`."""
        return matrix.shape.row == len(self)

    @staticmethod
    def projected_coordinates(coordinates):
        """Returns the 1D coordinates projected any multidimensional coordinates in the `ColumnVector`'s space."""
        return coordinates.x

    def __repr__(self):
        return Matrix2D.repr(zip(self))


class Matrix2D:
    """A 2D-matrix, built from a list of lists."""
    class Axes(Enum):
        """Give the user a way to name a 2D-matrix Axes"""
        ROW = 1
        COLUMN = 2

    def __init__(self, data):
        self.shape = Matrix2D._shape_raise_for_error(data)
        self._data = data
        self._transpose = None

    @property
    def T(self):
        """Returns the transposed matrix."""
        if self._transpose is None:
            self._transpose = Matrix2D(list(map(list, zip(*self))))
        return self._transpose

    def axis_reduce(self, axis, function):
        """Reduce the matrix using `function`. The optional parameter `axis`
        allows to reduce only along the given axis.

        If no `axis` is given, then this method returns a scalar.

        Reminder: reducing a matrix with shape (R,C) on the row axis, result in returning
        a column vector of size (0, C). Reciprocally a row vector of size (R, 0)
        is returned when reducing columns.
        """
        if axis is Matrix2D.Axes.ROW:
            return ColumnVector(function(v) for v in self)
        return RowVector(function(v) for v in self.T)

    def flag_projected_matches(self, vector):
        """Each row/column of the input matrix is compared to the input `vector`:

        Rows matching:

            [1 2 3]    flag_projected_matches    [1 5 3]    = [O . O]
            [4 5 3]                                           [. O O]

        Columns matching:

            [1 2 3]    flag_projected_matches      [1]      = [O . .]
            [4 5 6]                                [5]        [. O .]

        O shows matched items, . shows unmatched items (either it matched the vector or not).
        The function returns a matrix where matched cells contain `True` while unmatched ones contain `False`.
        """
        return self.map_cells(lambda coordinates, cell: cell == vector[vector.projected_coordinates(coordinates)])

    def where(self, condition=lambda x: x):
        """Returns a generator that goes over cells that satisfy `condition`."""
        for coordinates, cell in self.enumerate_cells():
            if condition(cell):
                yield Coordinates(*coordinates)

    def all(self, condition=lambda x: x):
        """Return `True` if all cells verify `condition`, notice that the default value for `condition`
        is the identity function."""
        all(condition(cell) for _, cell in self.enumerate_cells())

    def map_cells(self, function):
        """Returns a matrix in which `function` has been applied to all elements.
        `function` will be called with the three following arguments (on each cell):
            - the `cell` value,
            - the row index and the
            - the column index.
        """
        return Matrix2D([[function(Coordinates(i, j), cell) for j, cell in enumerate(row)] for i, row in enumerate(self)])

    def enumerate_cells(self):
        """Returns a generator such that each item is one of the matrix's `(coordinates, cell)` pair."""
        for i, row in enumerate(self):
            for j, cell in enumerate(row):
                yield Coordinates(i, j), cell

    def __eq__(self, other):
        if not isinstance(other, Matrix2D):
            return NotImplemented
        if self.shape != other.shape:
            return False
        return self.map_cells(lambda coordinates, cell: cell == other[coordinates]).all()

    def _binary_operation(self, other, operation):
        return Matrix2D([[operation(a, b) for (a, b) in zip(*rows)] for rows in zip(self, other)])

    def __and__(self, other):
        return self._binary_operation(other, lambda a, b: a & b)

    def __iter__(self):
        return self._data.__iter__()

    def __next__(self):
        return self._data.__next__()

    def __getitem__(self, index):
        if not isinstance(index, tuple) or len(index) != 2:
            raise ValueError("2D-matrix index should be a pair.")
        return self._data[index[0]][index[1]]

    @staticmethod
    def _cell_repr(cell):
        if cell is True:
            return 'O'
        if cell is False:
            return '.'
        return str(cell)

    @staticmethod
    def _shape_raise_for_error(data):
        shape = Shape(len(data), len(data[0]) if data else 0)
        for row in data:
            if len(row) != shape.column:
                raise ValueError("Matrix shape doesn't appear to be correct.")
        return shape

    def __repr__(self):
        return Matrix2D.repr(self)

    @staticmethod
    def repr(matrix_like):
        """String representation of any 2D-matrix-shaped object."""
        cell_sep = " "
        row_sep = " ]  \n"
        rows_text = map(lambda x: cell_sep.join(map(Matrix2D._cell_repr, x)), matrix_like)
        matrix_text = "{} ]  \n".format(row_sep.join(rows_text))
        return indent(matrix_text, "  [ ")
