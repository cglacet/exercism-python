from enum import Enum

def apply(array, function=None):
    if function is None:
        return array
    return [function(v) for v in array]

class Axis(Enum):
    ROW = 1
    COLUMN = 2

class Matrix:
    def __init__(self, data):
        self.shape = Matrix._shape_raise_for_error(data)
        self._data = data
        self._transpose = None

    @property
    def data(self):
        return self._data[:]

    @property
    def T(self):
        """Returns the transposed matrix."""
        if self._transpose is None:
            self._transpose = Matrix(list(map(list, zip(*self._data))))
        return self._transpose

    def saddle_points(self):
        """A "saddle point" is greater than or equal to every element in its row
        and less than or equal to every element in its column.
        """
        is_max_in_row = self.is_cell(condition=max, within=Axis.ROW)
        is_min_in_col = self.is_cell(condition=min, within=Axis.COLUMN)
        is_saddle = is_max_in_row & is_min_in_col
        saddle_indexes = set(self.index_where(is_saddle))
        return saddle_indexes

    def index_where(self, condition):
        for i, row in enumerate(self._data):
            for j in range(len(row)):
                if condition[i, j]:
                    yield (i, j)

    def is_cell(self, condition=lambda x: x is not None, within=None):
        if within not in Axis:
            raise ValueError("You must define a valid axis `within`, accepted values are:", Axis)
        if within == Axis.ROW:
            return self.is_cell_row_condition(condition)
        elif within == Axis.COLUMN:
            return self.is_cell_col_condition(condition)

    def is_cell_row_condition(self, condition):
        return Matrix([apply(row, function=lambda x, test_value=condition(row): x == test_value) for row in self._data])

    def is_cell_col_condition(self, condition):
        return self.T.is_cell_row_condition(condition).T

    @staticmethod
    def _shape_raise_for_error(data):
        shape = (len(data), len(data[0]) if data else 0)
        for row in data:
            if len(row) != shape[1]:
                raise ValueError("Matrix shape doesn't appear to be correct.")
        return shape

    def __getitem__(self, index):
        if not isinstance(index, tuple) or len(index) != 2:
            raise ValueError("2D-matrix index should be a pair.")
        return self._data[index[0]][index[1]]

    def __and__(self, other):
        return Matrix([[(a & b) for (a, b) in zip(*rows)] for rows in zip(self._data, other.data)])

    def __repr__(self):
        return "Matrix(\n\t{}\n)".format(',\n\t'.join(map(str, self._data)))

def saddle_points(data):
    matrix = Matrix(data)
    return matrix.saddle_points()

if __name__ == "__main__":
    print(saddle_points([
        [9, 8, 7],
        [5, 3, 2],
        [6, 6, 7]
    ]))
