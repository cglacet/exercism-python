"""This is an exercise from https://exercism.io/my/tracks/python."""
from typing import List

class CustomSet:
    def __init__(self, elements: List[object] = None, nb_buckets: int = 10**3) -> None:
        elements = elements or []
        self.buckets = [[]]*nb_buckets

    def isempty(self):
        pass

    def __contains__(self, element):
        pass

    def issubset(self, other):
        pass

    def isdisjoint(self, other):
        pass

    def __eq__(self, other):
        pass

    def add(self, element):
        pass

    def intersection(self, other):
        pass

    def difference(self, other):
        pass

    def union(self, other):
        pass
