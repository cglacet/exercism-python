def apply(array, function=None):
    if function is None:
        return array
    return [function(v) for v in array]


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
        row_argmax = self.is_row(condition=max)
        col_argmin = self.is_col(condition=min)
        is_saddle = row_argmax & col_argmin
        saddle_indexes = set(self.index_where(is_saddle))
        return saddle_indexes

    def index_where(self, condition):
        for i, row in enumerate(self._data):
            for j in range(len(row)):
                if condition[i, j]:
                    yield (i, j)

    def is_row(self, condition=min):
        return Matrix([apply(row, function=lambda x, r=row: x == condition(r)) for row in self._data])

    def is_col(self, condition=min):
        return self.T.is_row(condition=condition).T

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
    import numpy
    # saddle_points([
    #     [9, 8, 7],
    #     [5, 3, 2],
    #     [6, 6, 7]
    # ])
    m = numpy.array([0,0,0,0])
    sub_m = m[:]
    sub_m[0] = 1
    print(m)
    print("sub_m address =",hex(id(sub_m[0])))
    print("sub_m_2 address =",hex(id(m[0])))
