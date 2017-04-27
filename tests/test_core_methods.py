from wardmetrics.core_methods import *
import unittest


class TestCoreMethods(unittest.TestCase):
    def test_is_segment_in_interval(self):
        self.assertTrue(is_segment_in_interval(0, 10, -5, 20))
        self.assertFalse(is_segment_in_interval(0, 10, -5, -1))
        self.assertFalse(is_segment_in_interval(0, 10, 11, 15))
        self.assertFalse(is_segment_in_interval(0, 10, 10, 15))
        self.assertFalse(is_segment_in_interval(0, 10, -10, 0))
        self.assertFalse(is_segment_in_interval(0, 10, 1, 9))

if __name__ == '__main__':
    unittest.main()
