import matplotlib.pyplot as plt
import numpy as np
import math


class BoundaryCondition:
    nth_derivative = None
    x_val = None
    y_val = None

    def __init__(self, condition: str):
        self.nth_derivative = int(condition[condition.index('(') - 1])
        self.x_val = float(condition[condition.index('(') + 1: condition.index(')')])
        self.y_val = float(condition[condition.index('=') + 2:])

    def __str__(self):
        return 'S' + str(self.nth_derivative) + '(' + str(self.x_val) + ') = ' + str(self.y_val)


def FloatList(_list: list):
    for ii in range(len(_list)):
        _list[ii] = float(_list[ii])
    return _list


def FloatListPrint(_list: list):
    for ii in _list:
        print(round(ii, 2), end=' \t')
    print()











