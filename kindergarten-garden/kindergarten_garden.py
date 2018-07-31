"""This is an exercise from https://exercism.io/"""

from collections import defaultdict

PLANTS = {name[0]: name for name in ("Grass", "Clover", "Radishes", "Violets")}
STUDENTS = [
    "Alice", "Bob", "Charlie", "David", "Eve", "Fred", "Ginny",
    "Harriet", "Ileana", "Joseph", "Kincaid", "Larry"
]


class Garden:
    """The kindergarten class is learning about growing plants.
    They've chosen to grow grass, clover, radishes, and violets.
    Each child gets 4 `cups`, two on each `row`.
    Their teacher assigns cups to the children alphabetically by their names.

    The garden is built using a `diagram` and and optional list of `students` (names).
    The garden ``Garden("VVCCGG\nCRCCGG")`` starts with two violets `VV` on the first row,
    they belong to the first student, by default *Alice*. This student also have
    a clover and radishes in the second row.
    """
    def __init__(self, diagram, students=None):
        self.students = sorted(students if students else STUDENTS)
        self.cups = defaultdict(list)
        for student, plants in self._cups_in_diagram(diagram):
            self.cups[student].extend(plants)

    def plants(self, student):
        """Returns a list containing the given `student`'s plants."""
        return [PLANTS[plant] for plant in self.cups[student]]

    def _cups_in_diagram(self, diagram):
        for row in Garden._plant_rows(diagram):
            yield from self._cups_in_row(row)

    @staticmethod
    def _plant_rows(diagram):
        return diagram.split("\n")

    def _cups_in_row(self, plant_row):
        cup_size = 2
        cups = zip(*[iter(plant_row)]*cup_size)
        return zip(self.students, cups)
