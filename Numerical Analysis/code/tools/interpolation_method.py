from math import *
import numpy as np
import matplotlib.pyplot as plt


def goal():
    def func(x):
        return 1 / (x ** 2 + 1)
    return func


def Draw(func, color, _a, _b):
    _xs = np.arange(_a, _b + 0.00001, 0.01)
    _ys = func(_xs)
    plt.plot(_xs, _ys, color)


class Lagrange:
    # 返回插值多项式
    def __init__(self, _xs: list, _ys: list):
        def func(x: np.array):
            fx = 0.0
            for i in range(len(_xs)):
                fx += _ys[i] * self.make_lk(_xs, i)(x)
            return fx
        self.func = func

    @staticmethod
    def make_lk(_xs, k):
        def lk(x):
            denominator, numerator = 1, 1
            for i in range(len(_xs)):
                if i != k:
                    denominator *= (_xs[k] - _xs[i])
                    numerator *= (x - _xs[i])
            return numerator / denominator
        return lk


class Newton:
    # 返回插值多项式
    def __init__(self, _xs: list, _ys: list):
        self.xs = _xs
        n = len(_xs)

        def func(_xs: np.array):
            y_list = []
            for x in _xs:
                val = 0.0
                for k in range(n):
                    val += self.Omega(k, x) * self.AverageDifference(_ys[:k + 1])
                y_list.append(val)
            return y_list
        self.func = func

    def AverageDifference(self, _ys):
        result = 0.0
        n = len(_ys)
        for j in range(n):
            numerator = _ys[j]
            denominator = 1.0
            for k in range(n):
                if k != j:
                    denominator *= (self.xs[j] - self.xs[k])
            result += (numerator / denominator)

        return result

    def Omega(self, n, x):
        result = 1
        for i in range(n):
            result *= (x - self.xs[i])
        return result


# 为简便，此处均分区间
class Composite:
    def __init__(self, _xs: list, _ys: list, _type: str, n: int):
        pass


class Hermite:
    def __init__(self, _xs: list, _ys: list):
        pass


# 设立区间参数，以及目标点集
# 编辑test函数
if __name__ == '__main__':
    a = -5
    b = 5
    xs = np.arange(a, b + 0.00001, 1)
    ys = goal()(xs)

    flag = 0
    if flag == 1:
        my = Newton(xs, ys)
    else:
        my = Lagrange(xs, ys)

    plt.scatter(xs, ys)
    Draw(goal(), 'b', a, b)
    Draw(my.func, 'r', a, b)
    plt.show()
















