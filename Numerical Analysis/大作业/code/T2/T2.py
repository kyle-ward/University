import numerical_integration as ni
import matplotlib.pyplot as plt
import scipy.integrate as si
import numpy as np
import time
import math


# 广播函数
def f(xs):
    return (xs * np.exp(xs)) / ((xs + 1) ** 2)


if __name__ == '__main__':
    # 初始化n_list与一些存储变量
    n_list = np.arange(1, 31, 1)
    print(n_list)
    Simpson_result_list = []
    Gauss_result_list = []

    Simpson_error_list = []
    Gauss_error_list = []

    Simpson_time_cost = []
    Gauss_time_cost = []
    temp = []
    # 计算积分的精确结果
    res = si.quad(f, 0, 1)[0]

    # sti和edi用来记录时间
    # 对于每一个n值，计算当前的Simpson和Gauss求积公式结果并记录下来
    for n in n_list:
        st1 = time.perf_counter()
        result1 = ni.Composite.Simpson(f, 0, 1, n)
        ed1 = time.perf_counter()
        Simpson_time_cost.append(ed1 - st1)

        st2 = time.perf_counter()
        result2 = ni.Composite.Gauss(f, 0, 1, n, 2)
        ed2 = time.perf_counter()
        Gauss_time_cost.append(ed2 - st2)

        # 这是三个求积节点的Gauss公式，仅用于对比参考
        st3 = time.perf_counter()
        result3 = ni.Composite.Gauss(f, 0, 1, n, 3)
        ed3 = time.perf_counter()
        temp.append(ed3 - st3)

        # 对于每个n值，分别记录每个求积公式结果以及误差
        Simpson_result_list.append(result1)
        Simpson_error_list.append(math.fabs(result1 - res))
        Gauss_result_list.append(result2)
        Gauss_error_list.append(math.fabs(result2 - res))
    # 打印输出
    print('\n\nSimpson:')
    print(Simpson_error_list)
    print('Gauss:')
    print(Gauss_error_list)
    print('-----------------------')
    print(Simpson_time_cost)
    print(Gauss_time_cost)

    # 绘图可视化
    plt.title('Error Analysis')
    plt.xlabel('n')
    plt.ylabel('error')
    plt.plot(n_list, Simpson_error_list, 'r-d')
    plt.plot(n_list, Gauss_error_list, 'b-d')
    plt.show()

    plt.title('Computing Time')
    plt.xlabel('n')
    plt.ylabel('time/s')
    plt.plot(n_list, Simpson_time_cost, 'r-d')
    plt.plot(n_list, Gauss_time_cost, 'b-d')
    plt.show()
    '''
    plt.plot(n_list, temp, 'r-d')
    plt.plot(n_list, Gauss_time_cost, 'b-d')
    plt.show()
    '''





