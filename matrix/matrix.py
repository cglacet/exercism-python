class Matrix(object):
    def __init__(self, matrix_string):
        rows = [r.split(" ") for r in matrix_string.splitlines()]
        self.nb_rows = len(rows)
        self.nb_cols = len(rows[0])
        self.matrix = [int(c) for row in rows for c in row]

    def row(self, index):
        start = (index - 1) * self.nb_cols
        end = start + self.nb_cols
        return self.matrix[start:end]

    def column(self, index):
        start = index - 1
        end = self.nb_cols * self.nb_rows
        step = self.nb_cols
        return self.matrix[start:end:step]
