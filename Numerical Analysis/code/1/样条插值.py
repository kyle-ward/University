from functions import *

# 1.区间 [a, b]
# 2.几个端点 n
# 3.各自的自变量以及函数值 x[n], y[n]
# 待拟合函数 f(x) -> S(x) -> S[n](x)
# 4.边界条件：S1(x[0]) = f1(x[0]), S1(x[n]) = f1(x[n])
#           S2(x[0]) = f2(x[0]), S2(x[n]) = f2(x[n])

# k = 0 ~ n - 1
# h[k] = x[k + 1] - x[k]  ->  缺少h[n]

# k = 1 ~ n - 1
# lmd[k] = h[k] / (h[k] + h[k - 1])  ->  缺少lmd[0]
# mju[k] = h[k - 1] / (h[k] + h[k - 1])  -> 缺少mju[0]
# d[k] = 6 * f[x[k - 1], x[k], x[k +1]]
# 第一类边界条件：d[0] = (6/h[0]) * (f[x[0], x[1]] - f'(a))    d[n] = (6/h[0]) * (f'(b) - f[x[n - 1], x[n]])
# 第二类边界条件：d[0] = 2f''(a), d[n] = 2f''(b)


# 简化的均差函数
def AverageDifference(ii: int, jj: int):
    global _x, _y
    return (_y[ii] - _y[jj]) / (_x[ii] - _x[jj])


# 求出h
def _h_(x: list):
    h = []
    for k in range(len(x) - 1):
        h.append(x[k + 1] - x[k])
    return h


# 求出lmd
def _lmd_(h: list):
    lmd = [0]
    global boundary_condition
    for k in range(1, len(h)):
        lmd.append(h[k] / (h[k] + h[k - 1]))
    lmd.append(0)
    # 判断是第几种临界条件，并赋予不同的值
    if boundary_condition[0].nth_derivative == 1:
        lmd[0] = 1
    return lmd


# 求出mju
def _mju_(h: list):
    mju = [0]
    global boundary_condition
    for k in range(1, len(h)):
        mju.append(h[k - 1] / (h[k] + h[k - 1]))
    mju.append(0)
    # 判断是第几种临界条件，并赋予不同的值
    if boundary_condition[0].nth_derivative == 1:
        mju[-1] = 1
    return mju


# 求出d
def _d_(x, h):
    global boundary_condition, n
    # 判断是第几种临界条件，并赋予不同的值
    state = boundary_condition[0].nth_derivative
    d = [(6/h[0]) * (AverageDifference(0, 1) - boundary_condition[0].y_val) if state == 1 else boundary_condition[0].y_val]
    for k in range(1, len(x) - 1):
        d.append(6 * ((AverageDifference(k, k + 1) - AverageDifference(k - 1, k))/(x[k + 1] - x[k - 1])))
    d.append((6/h[n - 1]) * (boundary_condition[1].y_val - AverageDifference(n, n - 1)) if state == 1 else boundary_condition[1].y_val)
    return d


# 根据h，lmd以及mju的值初始化矩阵
def MatrixInit(lmd, mju):
    global n
    mat = []
    for i in range(n + 1):
        temp = [0] * (n + 1)
        for j in range(n + 1):
            if i == j:
                temp[j] = 2
            elif j == i + 1:
                temp[j] = lmd[i]
            elif j == i - 1:
                temp[j] = mju[i]
        mat.append(temp)
    return np.array(mat)


# 计算S[j](x)的值
def Sj(x: float, j: int):
    global _m, _x, _y, _h
    a1 = (_m[j] / (6 * _h[j])) * (_x[j + 1] - x) ** 3
    a2 = (_m[j + 1] / (6 * _h[j])) * (x - _x[j]) ** 3
    a3 = ((_y[j] - (_m[j] / 6) * (_h[j] ** 2)) / _h[j]) * (_x[j + 1] - x)
    a4 = ((_y[j + 1] - (_m[j + 1] / 6) * (_h[j] ** 2)) / _h[j]) * (x - _x[j])
    return a1 + a2 + a3 + a4


# 批量计算S(x)的值，便于绘制函数图像
def S(xs: np.array):
    global _x, n
    temp = []
    for x in xs:
        for j in range(n):
            if _x[j] <= x <= _x[j + 1] + 0.000000001:
                temp.append(Sj(x, j))
                break
    return np.array(temp)


# 分段打印出S(x)的表达式
def Print_Sx():
    global n, _x
    for j in range(n):
        Print_Sjx(j)
        print('[' + str(_x[j]) + ', ' + str(_x[j +1]) + ']')


# 打印出S[j](x)的表达式
def Print_Sjx(j: int):
    sup_map = str.maketrans('0123456789', '⁰¹²³⁴⁵⁶⁷⁸⁹')
    global _m, _x, _y, _h
    a1 = _m[j]/(6 * _h[j])
    a2 = _m[j + 1]/(6 * _h[j])
    a3 = (_y[j] - (_m[j]/6) * (_h[j] ** 2))/_h[j]
    a4 = (_y[j + 1] - (_m[j + 1]/6) * (_h[j] ** 2))/_h[j]
    string1 = str(round(a1, 5)) + '(' + str(_x[j + 1]) + ' - x)3'.translate(sup_map)
    string2 = str(round(math.fabs(a2), 5)) + '(x - ' + str(_x[j]) + ')3'.translate(sup_map)
    string3 = str(round(math.fabs(a3), 5)) + '(' + str(_x[j + 1]) + ' - x)'
    string4 = str(round(math.fabs(a4), 5)) + '(x - ' + str(_x[j]) + ')'
    print(string1 + (' + ' if a3 >= 0 else ' - ') + string3 + (' + ' if a2 >= 0 else ' - ') + string2 + (' + ' if a4 >= 0 else ' - ') + string4, end='\t\t')


# 请输入区间：
a, b = FloatList(input('')[1:-1].split(', '))
xs = np.arange(a, b, 0.01)
# 插值区间个数(x[0] ~ x[n])：
n = int(input(''))
_x = FloatList(input().split(' '))
_y = FloatList(input().split(' '))
boundary_condition = [BoundaryCondition(input()), BoundaryCondition(input())]

_h = _h_(_x)
_mju = _mju_(_h)
_lmd = _lmd_(_h)

_d = _d_(_x, _h)
print('_h, _lmd, _mju: ')
FloatListPrint(_h)
FloatListPrint(_lmd)
FloatListPrint(_mju)
print('-----------------------------------')
FloatListPrint(_d)

matrix = MatrixInit(_lmd, _mju)
for aa in matrix:
    FloatListPrint(aa)
    pass
print('计算出来各点处的二阶导数值：')
_m = np.linalg.solve(matrix, np.array(_d))
print(_m)
print('------------------------------------')
Print_Sx()

ys = S(xs)
zs = xs ** 0.5
print(xs)
print(ys)
plt.plot(xs, ys, color='black')
plt.plot(xs, zs, color='red')
plt.grid()
plt.show()


'''
xs = np.arange(-3, 3, 0.1)
print(type(xs))
ys = xs ** 2
zs = np.exp(xs)
plt.plot(xs, zs, color='black')
plt.plot(xs, ys)
plt.grid()
plt.show()
'''

'''
测试输入1

[27.7, 30]
3
27.7 28 29 30
4.1 4.3 4.1 3.0
S1(27.7) = 3.0
S1(30) = -4.0


测试输入2

[0.25, 0.53]
4
0.25 0.30 0.39 0.45 0.53
0.5000 0.5477 0.6245 0.6708 0.7280
S1(0.25) = 1.0000
S1(0.53) = 0.6868


测试输入3

[0.25, 0.53]
4
0.25 0.30 0.39 0.45 0.53
0.5000 0.5477 0.6245 0.6708 0.7280
S2(0.25) = 0
S2(0.53) = 0


实习题输入：

[0, 64]
8
0 1 4 9 16 25 36 49 64
0 1 2 3 4 5 6 7 8
S1(0) = 10000
S1(64) = 0.0625
'''








