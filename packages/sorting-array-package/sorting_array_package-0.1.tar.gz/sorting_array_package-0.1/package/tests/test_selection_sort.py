import unittest
import numpy
from ..listfunc.funcs import selection_sort


class MyTestCase(unittest.TestCase):
    def test_selection_sort(self):
        self.assertEqual(selection_sort(numpy.array([5, 4, 3, 2, 1])).all(),
                         numpy.array([1, 2, 3, 4, 5]).all())


if __name__ == '__main__':
    unittest.main()
