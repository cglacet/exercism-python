from __future__ import division

import unittest

import math

from complex_numbers import ComplexNumber


# Tests adapted from `problem-specifications//canonical-data.json` @ v1.3.0

class ComplexNumbersTest(unittest.TestCase):

    def test_real_part_of_a_purely_real_number(self):
        input_number = ComplexNumber(1, 0)
        self.assertEqual(input_number.real, 1)

    def test_real_part_of_a_purely_imaginary_number(self):
        input_number = ComplexNumber(0, 1)
        self.assertEqual(input_number.real, 0)

    def test_real_part_of_a_number_with_real_and_imaginary_part(self):
        input_number = ComplexNumber(1, 2)
        self.assertEqual(input_number.real, 1)

    def test_imaginary_part_of_a_purely_real_number(self):
        input_number = ComplexNumber(1, 0)
        self.assertEqual(input_number.imaginary, 0)

    def test_imaginary_part_of_a_purely_imaginary_number(self):
        input_number = ComplexNumber(0, 1)
        self.assertEqual(input_number.imaginary, 1)

    def test_imaginary_part_of_a_number_with_real_and_imaginary_part(self):
        input_number = ComplexNumber(1, 2)
        self.assertEqual(input_number.imaginary, 2)

    def test_imaginary_unit(self):
        first_input = ComplexNumber(0, 1)
        second_input = ComplexNumber(0, 1)
        expected = ComplexNumber(-1, 0)
        self.assertEqual(first_input * second_input, expected)

    def test_add_purely_real_numbers(self):
        first_input = ComplexNumber(1, 0)
        second_input = ComplexNumber(2, 0)
        expected = ComplexNumber(3, 0)
        self.assertEqual(first_input + second_input, expected)

    def test_add_purely_imaginary_numbers(self):
        first_input = ComplexNumber(0, 1)
        second_input = ComplexNumber(0, 2)
        expected = ComplexNumber(0, 3)
        self.assertEqual(first_input + second_input, expected)

    def test_add_numbers_with_real_and_imaginary_part(self):
        first_input = ComplexNumber(1, 2)
        second_input = ComplexNumber(3, 4)
        expected = ComplexNumber(4, 6)
        self.assertEqual(first_input + second_input, expected)

    def test_subtract_purely_real_numbers(self):
        first_input = ComplexNumber(1, 0)
        second_input = ComplexNumber(2, 0)
        expected = ComplexNumber(-1, 0)
        self.assertEqual(first_input - second_input, expected)

    def test_subtract_purely_imaginary_numbers(self):
        first_input = ComplexNumber(0, 1)
        second_input = ComplexNumber(0, 2)
        expected = ComplexNumber(0, -1)
        self.assertEqual(first_input - second_input, expected)

    def test_subtract_numbers_with_real_and_imaginary_part(self):
        first_input = ComplexNumber(1, 2)
        second_input = ComplexNumber(3, 4)
        expected = ComplexNumber(-2, -2)
        self.assertEqual(first_input - second_input, expected)

    def test_multiply_purely_real_numbers(self):
        first_input = ComplexNumber(1, 0)
        second_input = ComplexNumber(2, 0)
        expected = ComplexNumber(2, 0)
        self.assertEqual(first_input * second_input, expected)

    def test_multiply_purely_imaginary_numbers(self):
        first_input = ComplexNumber(0, 1)
        second_input = ComplexNumber(0, 2)
        expected = ComplexNumber(-2, 0)
        self.assertEqual(first_input * second_input, expected)

    def test_multiply_numbers_with_real_and_imaginary_part(self):
        first_input = ComplexNumber(1, 2)
        second_input = ComplexNumber(3, 4)
        expected = ComplexNumber(-5, 10)
        self.assertEqual(first_input * second_input, expected)

    def test_divide_purely_real_numbers(self):
        input_number = ComplexNumber(1.0, 0.0)
        expected = ComplexNumber(0.5, 0.0)
        divider = ComplexNumber(2.0, 0.0)
        self.assertEqual(input_number / divider, expected)

    def test_divide_purely_imaginary_numbers(self):
        input_number = ComplexNumber(0, 1)
        expected = ComplexNumber(0.5, 0)
        divider = ComplexNumber(0, 2)
        self.assertEqual(input_number / divider, expected)

    def test_divide_numbers_with_real_and_imaginary_part(self):
        input_number = ComplexNumber(1, 2)
        expected = ComplexNumber(0.44, 0.08)
        divider = ComplexNumber(3, 4)
        self.assertEqual(input_number / divider, expected)

    def test_absolute_value_of_a_positive_purely_real_number(self):
        self.assertEqual(abs(ComplexNumber(5, 0)), 5)

    def test_absolute_value_of_a_negative_purely_real_number(self):
        self.assertEqual(abs(ComplexNumber(-5, 0)), 5)

    def test_absolute_value_of_imaginary_number_positive_imaginary_part(self):
        self.assertEqual(abs(ComplexNumber(0, 5)), 5)

    def test_absolute_value_of_imaginary_number_negative_imaginary_part(self):
        self.assertEqual(abs(ComplexNumber(0, -5)), 5)

    def test_absolute_value_of_a_number_with_real_and_imaginary_part(self):
        self.assertEqual(abs(ComplexNumber(3, 4)), 5)

    def test_equality(self):
        real = 1
        imaginary = 2
        for precision in [10**-2, 10**-5, 10**-10]:
            input_number = ComplexNumber(real, imaginary, precision=precision)
            for imaginary_offset in [0, 1, -1]:
                for real_offset in [0, 1, -1]:
                    if imaginary_offset == 0 and real_offset == 0:
                        continue
                    expected_in = ComplexNumber(real+(0.9*precision*real_offset), imaginary+(0.9*precision*imaginary_offset), precision=precision)
                    expected_out = ComplexNumber(real+(1.1*precision*real_offset), imaginary+(1.1*precision*imaginary_offset), precision=precision)
                    self.assertEqual(input_number, expected_in)
                    self.assertNotEqual(input_number, expected_out)

    def test_conjugate_a_purely_real_number(self):
        input_number = ComplexNumber(5, 0)
        expected = ComplexNumber(5, 0)
        self.assertEqual(input_number.conjugate(), expected)

    def test_conjugate_a_purely_imaginary_number(self):
        input_number = ComplexNumber(0, 5)
        expected = ComplexNumber(0, -5)
        self.assertEqual(input_number.conjugate(), expected)

    def test_conjugate_a_number_with_real_and_imaginary_part(self):
        input_number = ComplexNumber(1, 1)
        expected = ComplexNumber(1, -1)
        self.assertEqual(input_number.conjugate(), expected)

    def test_eulers_identity_formula(self):
        input_number = ComplexNumber(0, math.pi)
        expected = ComplexNumber(-1, 0)
        self.assertEqual(input_number.exp(), expected)

    def test_exponential_of_0(self):
        input_number = ComplexNumber(0, 0)
        expected = ComplexNumber(1, 0)
        self.assertEqual(input_number.exp(), expected)

    def test_exponential_of_a_purely_real_number(self):
        input_number = ComplexNumber(1, 0)
        expected = ComplexNumber(math.e, 0)
        self.assertEqual(input_number.exp(), expected)

    def test_exponential_of_a_number_with_real_and_imaginary_part(self):
        input_number = ComplexNumber(math.log(2), math.pi)
        expected = ComplexNumber(-2, 0)
        self.assertEqual(input_number.exp(), expected)


if __name__ == '__main__':
    unittest.main()
