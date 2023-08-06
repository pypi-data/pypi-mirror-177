import numpy
from .listfunc.funcs import selection_sort

DATA = (numpy.array([5, 512412, 4214, 788, 34, -3454, 22, 1432, 4, 7, 88, 0, -55]), ["dd", 421, "sad", 4.4],
        numpy.array([777, 555, 666, 421, 222, 333, 1, 2, 3]))


def function_examples():
    print(DATA[0], selection_sort(DATA[0]))
    print(DATA[1], "text_error")
    print(DATA[2], selection_sort(DATA[2]))
