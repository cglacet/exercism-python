"""This is a exercise from https://exercism.io/my/tracks/python"""
from enum import Enum
from textwrap import indent


class Vector(list):
    """Adds a 2D-orientation to a list. This is usefull when dealing with matrices."""
    def __init__(self, *args, axis=None):
        if axis not in Matrix2D.Axes:
            raise ValueError("{} is not valid `axis`, accepted values are:".format(Matrix2D.Axes))
        list.__init__(self, *args)
        self.axis = axis
        self.shape = (0, len(self)) if self.is_row else (len(self), 0)

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

    def reduce(self, function=None, axis=None):
        """Reduce the matrix using `function`. The optional parameter `axis`
        allows to reduce only along the given axis.

        If no `axis` is given, then this method returns a scalar.

        Reminder: reducing a matrix with shape (R,C) on the row axis, result in returning
        a column vector of size (0, C). Reciprocally a row vector of size (R, 0)
        is returned when reducing columns.
        """
        if axis is not None and axis not in Matrix2D.Axes:
            raise ValueError("{} is not valid `axis`, accepted values are:".format(Matrix2D.Axes))
        if function is None:
            raise ValueError("You must provide a reduction function array => number|boolean|string|... .")
        if axis:
            if axis is Matrix2D.Axes.ROW:
                matrix = self
                vector_axis = Matrix2D.Axes.COLUMN
            else:
                matrix = self.T
                vector_axis = Matrix2D.Axes.ROW
            return Vector([function(v) for v in matrix], axis=vector_axis)

        return function([elem for row in self for elem in row])

    def min(self, axis=None):
        """Simply a shorthand for matrix.reduce(function=min, axis=axis)."""
        return self.reduce(function=min, axis=axis)

    def max(self, axis=None):
        """Simply a shorthand for matrix.reduce(function=max, axis=axis)."""
        return self.reduce(function=max, axis=axis)

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
        for i, row in enumerate(self):
            for j, cell in enumerate(row):
                if condition(cell):
                    yield (i, j)

    def all(self, condition=lambda x: x):
        """Return `True` if all cells verify `condition`, notice that the default value for `condition`
        is the identity function."""
        for row in self:
            for cell in row:
                if not condition(cell):
                    return False
        return True

    def match(self, other):
        """`Matching` is some sort of equality with three discint functionalities:

            Matrix to matrix match:

            [1 2 3]    match    [2 1 3]    =  False
            [4 5 6]             [4 5 7]

            [1 2 3]    match    [1 2 3]    =  True
            [4 5 6]             [4 5 6]

            Matrix to (row/column) vector match:

            [1 2 3]    match    [1 5 3]    = [O . O]
            [4 5 3]                          [. O O]

            [1 2 3]    match      [1]      = [O . .]
            [4 5 6]               [5]        [. O .]

            Matrix to scalar match:

            [1 2 3]    match       3       = [. . O]
            [4 5 6]                          [. . .]

        O shows matched items, . shows unmatched items (either it matched the vector/scalar or not).
        The function return either (i) `True` or `False` if `other` is a matrix,
        (ii) or a matrix where matched cells contain `True` while unmatched ones contain `False`.
        """
        if isinstance(other, Matrix2D):
            if self.shape != other.shape:
                raise ValueError("Can't match matrices that have different shapes.")
            return self.map(lambda cell, i, j: cell == other[i, j]).all()
        if isinstance(other, Vector):
            is_shape_ok = (other.is_column and self.shape[0] == other.shape[0])
            is_shape_ok = is_shape_ok or (other.is_row and self.shape[1] == other.shape[1])
            if not is_shape_ok:
                raise ValueError("Matrix and vector have incompatible shapes.")
            return self.map(lambda cell, i, j: cell == other[j if other.is_row else i])
        if isinstance(other, (int, float, bool, str)):
            return self.map(lambda cell, i, j: cell == other)
        if isinstance(other, list):
            raise ValueError("You can't use a list with '==', but you can use a `Vector` instead.")
        return False

    def __eq__(self, other):
        self.match(other)

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


def saddle_points(data):
    """A "saddle point" is greater than or equal to every element in its row
    and less than or equal to every element in its column.
    """
    matrix = Matrix2D(data)
    rows_maximums = matrix.max(axis=Matrix2D.Axes.ROW)
    is_max_in_row = (matrix.match(rows_maximums))
    columns_minimums = matrix.min(axis=Matrix2D.Axes.COLUMN)
    is_min_in_col = (matrix.match(columns_minimums))
    is_saddle = is_max_in_row & is_min_in_col
    saddle_indexes = set(is_saddle.where())

    print("Input matrix is: \n{}".format(matrix))
    print("Row's max locations:")
    print(same_line(str(matrix), " match ", str(rows_maximums), ' = ', str(is_max_in_row)))
    print("Columns's min locations:")
    print(same_line(str(matrix), " match ", str(columns_minimums), ' = ', str(is_min_in_col)))
    print("Saddle points locations:")
    print(same_line(str(is_max_in_row), "   &   ", str(is_min_in_col), ' = ', str(is_saddle)))
    print("Saddle points are at indexes: \n{}".format(saddle_indexes))

    return saddle_indexes


def same_line(*strings, ghost=None):
    strings_lines = [string.split('\n') for string in strings]
    if ghost and len(ghost) > 0:
        for string_index in ghost:
            strings_lines[string_index] = [" "*len(line) for line in strings_lines[string_index]]
    strings_max_len = [max(len(line) for line in lines) for lines in strings_lines]
    max_nb_of_lines = max(len(lines) for lines in strings_lines)
    concatenation = ""
    for i in range(max_nb_of_lines):
        for j, lines in enumerate(strings_lines):
            line = lines[i] if i < len(lines) else " "
            concatenation += line
            concatenation += " "*(strings_max_len[j]-len(line))
        concatenation += "\n"
    return concatenation

def test_reduce_and_eq():
    matrix = Matrix2D([
        [9, 8, 7],
        [5, 3, 2]
    ])
    # The idea is to test wether a matrix "match" a given matrix/vector/scalar
    # to be the most general as possible. This way the user can even create
    # its own matrix/vector/scalar, and then try to "match" it with a matrix.
    #
    # "Matching" is some sort of equality such that:
    #
    #     [1 2 3]    match    [2 1 3]    =  False
    #     [4 5 6]             [4 5 7]
    #
    #     [1 2 3]    match    [1 2 3]    =  True
    #     [4 5 6]             [4 5 6]
    #
    #     [1 2 3]    match    [1 5 3]    = [O . O]
    #     [4 5 6]                          [. O .]
    #
    #     [1 2 3]    match      [1]      = [O . .]
    #     [4 5 6]               [5]        [. O .]
    #
    #     [1 2 3]    match       3       = [. . O]
    #     [4 5 6]                          [. . .]
    #
    # O means true, . means false (either it matched the vector/scalar or not)
    row_mins = matrix.min(axis=Matrix2D.Axes.ROW)
    print(same_line(str(matrix), " match   ", str(row_mins), '   = ', str(matrix.match(row_mins))))

    col_maxs = matrix.max(axis=Matrix2D.Axes.COLUMN)
    print(same_line(str(matrix), " match ", str(col_maxs), ' = ', str(matrix.match(col_maxs)), ghost=[0]))

    overall_min = matrix.min()
    print(same_line(str(matrix), " match       ", str(overall_min), '       = ', str(matrix.match(overall_min)), ghost=[0]))

    print(same_line(str(matrix), " match ", str(matrix.T.T), ' =     ', str(matrix.match(matrix.T.T)), ghost=[0]))

def test_and_operator():
    matrix_A = Matrix2D([
        [True, False, True],
        [False, True, True]
    ])
    matrix_B = Matrix2D([
        [False, True, False],
        [False, True, True]
    ])
    print(same_line(str(matrix_A), " AND ", str(matrix_B), ' = ', str(matrix_A & matrix_B)))
    print(same_line(str(matrix_A), " OR  ", str(matrix_B), ' = ', str(matrix_A | matrix_B)))

if __name__ == "__main__":
    saddle_points([
        [9, 8, 7],
        [5, 3, 2],
        [6, 6, 7]
    ])
    # test_reduce_and_eq()
    #test_and_operator()
