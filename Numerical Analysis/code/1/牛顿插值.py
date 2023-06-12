from functions import *
from threading import Lock, RLock


# P(x) = a[0]f[x[0]] + a[1]f[x[0], x[1]] + ... + a[n]f[x[0], ... ,x[n]]
# a[0] = 1, a[k] = (x - x[0])* ... *(x - x[n - 1])
# f[x[0]] = f(x[0]), 后者都符合均差的定义
lock = Lock()
rlock = RLock()


# 均差函数
def AverageDifference(_list: list):
    global _x, _y
    if len(_list) == 1:
        return _y[_list[0]]
    if len(_list) == 2:
        return (_y[_list[0]] - _y[_list[-1]])/(_x[_list[0]] - _x[_list[-1]])
    else:
        return (AverageDifference(_list[1:]) - AverageDifference(_list[:-1]))/(_x[_list[-1]] - _x[_list[0]])


# 返回Omega[j](x)的值
def Omega(x: float, j: int):
    global _x
    if j == 0:
        return 1
    else:
        val = 1.0
        for k in range(j):
            val *= (x - _x[k])
        return val


# 批量计算出插值多项式函数值
def P(xs: np.array):
    global _x, _y, n
    y_list = []
    for x in xs:
        val = 0.0
        temp = []
        print('st')
        for k in range(n + 1):
            temp.append(k)
            val += Omega(x, k) * AverageDifference(temp)
            print('-----', Omega(x, k))
        y_list.append(val)
    return np.array(y_list)


n = int(input())
_x = FloatList(input().split(' '))
_y = FloatList(input().split(' '))

xs = np.arange(_x[0], _x[-1] + 0.00001, 0.1)
ys = P(xs)
zs = xs ** 0.5

plt.plot(xs, ys, color='black')
plt.plot(xs, zs, color='red')
plt.grid()
plt.show()





'''
8
0 1 4 9 16 25 36 49 64
0 1 2 3 4 5 6 7 8

'''