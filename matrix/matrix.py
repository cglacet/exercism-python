ROW_SEP = "\n"
COL_SEP = " "


class Matrix(object):
    def __init__(self, matrix_string):
        self.rows = [[int(c) for c in l.split(COL_SEP)] for l in matrix_string.split(ROW_SEP)]
        self.cols = list(map(list, zip(*self.rows)))

    def row(self, index):
        return self.rows[index-1]

    def column(self, index):
        return self.cols[index-1]
