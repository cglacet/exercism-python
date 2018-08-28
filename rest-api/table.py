"""This is a part of an exercise from https://exercism.io/my/tracks/python"""


class Table(dict):
    """A table is a row-column matrix where each row is indexed using the
    `index` column. A table is initialized using a list of rows, where each row
    is a dictionnary maping column names to their respective values. (Note that
    no verification of the rows shape is made, we trust you on this one :D).
    """
    def __init__(self, table_name, elements, index):
        self.name = table_name
        self.elements = {entry[index]: entry for entry in elements}
        super().__init__(self.elements)
        self.index = index

    def __getitem__(self, key):
        return self.elements[key]

    def __setitem__(self, key, value):
        self.elements[key] = value

    def __repr__(self):
        return str(self.elements)

    def add_row(self, entry):
        """Add a row in the table. The `entry` argument is a dictionnary maping
        column names to their respective values. (Note that no verification of
        the rows shape is made, we trust you on this one :D).
        """
        self.elements[entry[self.index]] = entry
