import unittest

from module9.part1.eample_code import my_area_function

class TestMyAreaFunction(unittest.TestCase):

    def test_area(self):
        self.assertEqual(20, my_area_function(4, 5))

    def test_invalid_area(self):
        self.assertRaises(ValueError, my_area_function, -4, 5)