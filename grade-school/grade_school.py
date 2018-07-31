"""Exercise from https://exercism.io/my/tracks/python"""
from collections import defaultdict


class School:
    """Handle a school set of students with unique names, grouped by grades."""
    # A given grade will be sorted only if someone asked directly or undirectly for it.
    # Untill then each grade contains the students names in insertion order.
    # Dictionary `self.is_sorted` will be used to serve this lazzy sorting, ie.:
    #       if `self.is_sorted[i]` then `self.students[i]` is sorted
    # Note that calling `self.students[i]` directly will not sort the students of grade `i`.
    def __init__(self):
        self.students = defaultdict(list)
        self.is_sorted = defaultdict(bool)

    def add_student(self, name, grade):
        """Add the student named `name` to the `grade` school section."""
        self.students[grade].append(name)
        self.is_sorted[grade] = False

    def roster(self):
        """Returns a sorted list of all students. Sort is done by grade then by name."""
        return [name for grade in sorted(self.students.keys()) for name in self.grade(grade)]

    def grade(self, grade_number):
        """Returns an alphabetically-sorted list of students' names from grade `grade_number`"""
        if not self.is_sorted[grade_number]:
            self.students[grade_number] = sorted(self.students[grade_number])
            self.is_sorted[grade_number] = True
        return self.students[grade_number]
