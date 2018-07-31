from collections import Counter


class Triangle:
    def __init__(self, sides):
        if not Triangle.is_triangle(sides):
            raise ValueError("No triangle has these sides lengths: {}.".format(sides))
        self.sides = sides
        self.count = Counter(sides)

    def nb_equal_sides(self):
        return self.count.most_common(1)[0][1]

    def has_k_equal_sides(self, k):
        return self.nb_equal_sides() == k

    def has_at_least_k_equal_sides(self, k):
        return self.nb_equal_sides() >= k

    def is_triangle(sides):
        if min(sides) <= 0:
            return False
        sorted_sides = sorted(sides)
        if sum(sorted_sides[:-1]) < sorted_sides[-1]:
            return False
        return True

def return_false_on_value_error(function):
    def decorator(*args):
        try:
            return function(*args)
        except ValueError as e:
            print('Error "{}" \n\t => returning False'.format(e))
            return False
    return decorator

@return_false_on_value_error
def is_equilateral(sides):
    triangle = Triangle(sides)
    return triangle.has_k_equal_sides(3)
@return_false_on_value_error
def is_isosceles(sides):
    triangle = Triangle(sides)
    return triangle.has_at_least_k_equal_sides(2)
@return_false_on_value_error
def is_scalene(sides):
    triangle = Triangle(sides)
    return triangle.has_k_equal_sides(1)
