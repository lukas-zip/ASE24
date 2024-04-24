#run using
#python -m unittest -v test_module

import unittest




class MultiplyTestCase(unittest.TestCase):

    def test_multiply_positive_numbers(self):

        result = multiply(3, 4)

        self.assertEqual(result, 12)