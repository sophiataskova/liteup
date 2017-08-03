import unittest
from unittest.mock import patch
import random

from liteup.schemes.sort_scheme import mergesort


class SortSchemeTester(unittest.TestCase):

    def test_mergesort(self):
        random_array = [random.randint(0, 100) for x in range(1000)]
        #mergesort is an iterator. drain it to complete
        highlights = list(mergesort(random_array, 0, len(random_array)))
        self.assertEqual(random_array, sorted(random_array))


if __name__ == '__main__':
    unittest.main()
