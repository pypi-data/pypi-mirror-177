import numpy


def list_input() -> numpy.array:
    """
    Input an array of numbers
    :return: numpy array
    """
    while True:
        try:
            return numpy.array([elem for elem in map(int, input().split())])
        except ValueError as text_error:
            print(text_error)


def selection_sort(numbers) -> numpy.array:
    """
    Sorting an array with selection method
    :param numbers: numpy array of integer numbers
    :return: sorted numpy array
    """
    for i in range(len(numbers)):
        reserved_index = i
        for j in range(len(numbers) - i):
            if numbers[i + j] < numbers[reserved_index]:
                reserved_index = i + j
        numbers[i], numbers[reserved_index] = numbers[reserved_index], numbers[i]
    return numbers
