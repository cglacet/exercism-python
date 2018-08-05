"""This is an exercise from https://exercism.io/my/tracks/python

The goal is to find Saddle points in a matrix.
For an input matrix M, a cell (i, j) of M is said to be a "Saddle point" if
the cell's value is greater than or equal to every element in its row and
less than or equal to every element in its column:

        M[i,j] >= M[c,j] | c any column index of M
    and M[i,j] >= M[i,r] | r any row index of M

For example, with an input matrix M, the only Saddle point is on cell M[1, 0] = "5":
  [ 9 8 7 ]
  [ 5 3 2 ]
  [ 6 6 7 ]

The internal process used to find Saddle points is located in function `saddle_points`
and apply the following steps:

Finding "row's max.", a column vector equal to [9, 5, 7], and use if to compute a boolean
matrix in which each cell (i,j) is `True` if this cell's value is the maximum value it
its own row. This second operation is done using the `match` function:
  [ 9 8 7 ]   match   [ 9 ]   =   [ O . . ]
  [ 5 3 2 ]           [ 5 ]       [ O . . ]
  [ 6 6 7 ]           [ 7 ]       [ . . O ]


The same is done for "column's min.", we first compute the row vector representing min.
column values and then compute the boolean mask using the `match` function:
  [ 9 8 7 ]   match   [ 5 3 2 ]   =   [ . . . ]
  [ 5 3 2 ]                           [ O O O ]
  [ 6 6 7 ]                           [ . . . ]


Once we have these two boolean matrix, we just need to find cells where both conditions
are met to find Saddle points (using the logical `&` operator):
  [ O . . ]     &     [ . . . ]   =   [ . . . ]
  [ O . . ]           [ O O O ]       [ O . . ]
  [ . . O ]           [ . . . ]       [ . . . ]

Finally, Saddle points coordinates are retrieved using the `where` method on this last matrix:
  [ . . . ]
  [ O . . ]   where   {(1, 0)}
  [ . . . ]
"""
from enum import Enum
from textwrap import indent


def saddle_points(data):
    """A "saddle point" is greater than or equal to every element in its row
    and less than or equal to every element in its column.
    """
    matrix = Matrix2D(data)
    rows_maximums = matrix.reduce(Matrix2D.Axes.ROW, max)
    is_max_in_row = matrix.match(rows_maximums)
    columns_minimums = matrix.reduce(Matrix2D.Axes.COLUMN, min)
    is_min_in_col = matrix.match(columns_minimums)
    is_saddle = is_max_in_row & is_min_in_col
    saddle_indexes = set(is_saddle.where())

    print("Input matrix is: \n{}".format(matrix))
    print("Row's max locations: \n{}".format(is_max_in_row))
    print("Columns's min locations: \n{}".format(is_min_in_col))
    print("Saddle points locations: \n{}".format(is_saddle))
    print("Saddle points are at indexes: \n{}".format(saddle_indexes))

    return saddle_indexes


class Vector(list):
    """Adds a 2D-orientation to a list. This is usefull when dealing with matrices."""
    def __init__(self, *args, axis=None):
        if axis not in Matrix2D.Axes:
            raise ValueError("{} is not valid `axis`, accepted values are:".format(Matrix2D.Axes))
        list.__init__(self, *args)
        self.axis = axis
        self.shape = (0, len(self)) if self.is_row else (len(self), 0)

    def is_matrix_compatible(self, matrix):
        """Returns `True` if the input `matrix` has the same row (/colum) shape as the row (/column) `Vector`."""
        return matrix.shape[self.axis_index] == self.shape[self.axis_index]

    @property
    def axis_index(self):
        """Returns the axis index that corresponds the this `Vector` axis."""
        return 0 if self.is_column else 1

    @property
    def is_row(self):
        """True if this is a row-vector"""
        return self.axis == Matrix2D.Axes.ROW

    @property
    def is_column(self):
        """True if this is a column-vector"""
        return self.axis == Matrix2D.Axes.COLUMN

    def __repr__(self):
        if self.is_row:
            return Matrix2D.repr([self])
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
    def data(self):
        """Returns a copy of the matrix raw content."""
        return self[:]

    @property
    def T(self):
        """Returns the transposed matrix."""
        if self._transpose is None:
            self._transpose = Matrix2D(list(map(list, zip(*self))))
        return self._transpose

    def reduce(self, axis, function):
        """Reduce the matrix using `function`. The optional parameter `axis`
        allows to reduce only along the given axis.

        If no `axis` is given, then this method returns a scalar.

        Reminder: reducing a matrix with shape (R,C) on the row axis, result in returning
        a column vector of size (0, C). Reciprocally a row vector of size (R, 0)
        is returned when reducing columns.
        """
        if axis is Matrix2D.Axes.ROW:
            matrix = self
            vector_axis = Matrix2D.Axes.COLUMN
        else:
            matrix = self.T
            vector_axis = Matrix2D.Axes.ROW
        return Vector([function(v) for v in matrix], axis=vector_axis)

    def map(self, function):
        """Returns a matrix in which `function` has been applied to all element.
        `function` will be called with three arguments (on each cell):
            - the `cell` value,
            - the row index and the
            - the column index.
        """
        return Matrix2D([[function(cell, i, j) for j, cell in enumerate(row)] for i, row in enumerate(self)])

    def where(self, condition=lambda x: x):
        """Returns a generator that goes over cells that satisfy `condition`."""
        for coordinates, cell in self.enumarate_cells():
            if condition(cell):
                yield coordinates

    def all(self, condition=lambda x: x):
        """Return `True` if all cells verify `condition`, notice that the default value for `condition`
        is the identity function."""
        all(condition(cell) for _, cell in self.enumarate_cells())

    def enumarate_cells(self):
        """Returns a generator such that each item is one of the matrix's `(coordinates, cell)` pair."""
        for i, row in enumerate(self):
            for j, cell in enumerate(row):
                yield (i, j), cell

    def match(self, vector):
        """`Matching` is some sort of matrix to row(/column) vector equality.
        Each row/column of the input matrix is compared to the input `vector`:

        Row matching:

            [1 2 3]    match    [1 5 3]    = [O . O]
            [4 5 3]                          [. O O]

        Column matching:

            [1 2 3]    match      [1]      = [O . .]
            [4 5 6]               [5]        [. O .]

        O shows matched items, . shows unmatched items (either it matched the vector/scalar or not).
        The function returns a matrix where matched cells contain `True` while unmatched ones contain `False`.
        """
        if isinstance(vector, Vector):
            if not vector.is_matrix_compatible(self):
                raise ValueError("Matrix and vector have incompatible shapes.")
            return self.map(lambda cell, i, j: cell == vector[j if vector.is_row else i])
        if isinstance(vector, list):
            raise ValueError("Lists can't be matched (orientation ambiguity), use a `Vector` instead.")
        return False

    def __eq__(self, other):
        if not isinstance(other, Matrix2D):
            return NotImplemented
        if self.shape != other.shape:
            return False
        return self.map(lambda cell, i, j: cell == other[i, j]).all()

    def _binary_operation(self, other, operation=None):
        if not operation:
            raise ValueError("Please provide a function.")
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
        shape = (len(data), len(data[0]) if data else 0)
        for row in data:
            if len(row) != shape[1]:
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
