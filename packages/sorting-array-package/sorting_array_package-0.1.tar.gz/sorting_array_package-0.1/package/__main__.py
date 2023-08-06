"""
КИ22-16/1Б
Савельев Александр
Вариант 28
Selection_sort function
"""
import sys
import numpy
from .listfunc.funcs import selection_sort, list_input
from .example import function_examples


def main():
    numbers = numpy.array([])
    while True:
        command_var = input("Вывод списка на экран - 1\n"
                            "Ввод списка - 2\n"
                            "Сортировка списка - 3\n"
                            "Примеры работы - 4\n"
                            "Выход - 5\n")
        match command_var:
            case '1':
                print(numbers)
            case '2':
                print('Введите элементы списка через пробел')
                numbers = list_input()
            case '3':
                selection_sort(numbers)
                print('Список отсортирован')
            case '4':
                function_examples()
            case '5':
                sys.exit()
            case _:
                print('Неверная команда. Повторите попытку.\n')


if __name__ == '__main__':
    main()
