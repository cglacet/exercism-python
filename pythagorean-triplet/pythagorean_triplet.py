import math

def primitive_triplets(triplet_sum):
    # a + b + c = triplet_sum
    # a**2 + b**2 = c**2
    # => c = sqrt(a**2 + b**2)
    max_value = math.sqrt(triplet_sum)


#def triplets_in_range(range_start, range_end):


def is_triplet(triplet):
    a,b,c = triplet
    return a**2 + b**2 == c**2


if __name__ == "__main__":
    print(is_triplet([3,4,5]))
