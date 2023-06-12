import tools.numerical_integration as tn
import matplotlib.pyplot as plt
import scipy.integrate as si
import numpy as np
import time
import math


# 广播函数
def f(xs):
    return (xs * np.exp(xs)) / ((xs + 1) ** 2)


if __name__ == '__main__':
    n_list = [5, 6, 7, 8, 9, 10]
    Simpson_result_list = []
    Gauss_result_list = []
    for n in n_list:
        result1 = tn.Composite.Simpson(f, 0, 1, n)
        result2 = tn.Composite.Gauss(f, 0, 1, n)
        Simpson_result_list.append(result1)
        Gauss_result_list.append(result2)
    res = si.quad(f, 0, 1)[0]
    plt.plot(n_list, Simpson_result_list, 'r')
    plt.plot(n_list, Gauss_result_list, 'b')
    plt.plot(n_list, [res] * 6, 'g')
    plt.show()





