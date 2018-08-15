"""This is an exercise from https://exercism.io/my/tracks/python."""
from typing import Iterable
import math


def first_nth_primes(positive_number: int) -> Iterable[int]:
    first_nth_numbers = range(2, positive_number+1)
    for number in range(2, math.sqrt(positive_number+1)):
    return first_nth_numbers

def nth_prime(positive_number: int) -> int:
    pass
