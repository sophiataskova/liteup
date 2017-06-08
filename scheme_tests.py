import unittest
from unittest.mock import patch
import mock

from base_schemes import InterpolateScheme


class InterpolateSchemeTester(unittest.TestCase):

    def test_lin_interp(self):
        self.assertEqual(InterpolateScheme.lin_interp(6, 10, 0, 10), 6)
        self.assertEqual(InterpolateScheme.lin_interp(7, 10, 0, 10), 7)
        # hit rounding
        self.assertEqual(InterpolateScheme.lin_interp(6, 10, 0, 12), 7)

if __name__ == '__main__':
    unittest.main()
