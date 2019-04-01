import math


class ComplexNumber(object):
    def __init__(self, real, imaginary, precision=10**-10):
        self.precision = precision
        self.r = real
        self.i = imaginary

    @property
    def real(self):
        return self.r

    @property
    def imaginary(self):
        return self.i

    def __repr__(self):
        return "{} + {}i".format(self.r, self.i)

    def __eq__(self, other):
        precision = min(self.precision, other.precision)
        return (abs(self.r - other.r) < precision) and (abs(self.i - other.i) < precision)

    def __add__(self, other):
        return ComplexNumber(self.r+other.r, self.i+other.i)

    def __sub__(self, other):
        return ComplexNumber(self.r-other.r, self.i-other.i)

    def __mul__(self, other):
        real = (self.r * other.r - self.i * other.i)
        imaginary = (self.i * other.r + self.r * other.i)
        return ComplexNumber(real, imaginary)

    def __truediv__(self, other):
        denominator = (other.r**2 + other.i**2)
        real = (self.r * other.r + self.i * other.i)/denominator
        imaginary = (self.i * other.r - self.r * other.i)/denominator
        return ComplexNumber(real, imaginary)

    def __abs__(self):
        return math.sqrt(self.r**2 + self.i**2)

    def conjugate(self):
        return ComplexNumber(self.r, -self.i)

    def exp(self):
        c1 = ComplexNumber(math.exp(self.r), 0)
        c2 = ComplexNumber(math.cos(self.i), math.sin(self.i))
        return c1*c2
