from collections import OrderedDict
import math

# Keed track of previously asked primes through memoization:
def prime_finder():
    primes = OrderedDict({1: 2})
    max_n = 1
    x = 3

    def nth_prime_finder(n):
        nonlocal max_n, x
        raise_if_non_positive(n)
        if n <= max_n:
            return primes[n]
        max_n = n

        while len(primes) < n:
            if not has_factor_in(x, primes):
                primes[len(primes) + 1] = x
            x += 2
        return primes[n]

    return nth_prime_finder

def has_factor_in(x, candidates):
    for f in candidates.values():
        if f > math.sqrt(x):
            return False
        if x % f == 0:
            return True
    return False

def raise_if_non_positive(n):
    if not isinstance(n, int) or n < 1:
        raise ValueError(f"n must be a positive integer, not {n}.")


nth_prime = prime_finder()