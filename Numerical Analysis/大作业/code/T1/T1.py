import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate as igt


# 用递推的方法定义切比雪夫多项式函数
def cheb_poly(n):
    if n == 0:
        return lambda x: 1.0
    elif n == 1:
        return lambda x: x
    else:
        return lambda x: 2 * x * cheb_poly(n - 1)(x) - cheb_poly(n - 2)(x)


# 内积的算法
def inner_product(f, g):
    a = lambda x: f(x) * g(x) * rho(x)
    result = igt.quad(a, -1, 1)[0]
    return result


# 计算最佳平方逼近多项式
def best_approximation(f, n):
    global xs
    # 对f(x)在[a, b]上积分等价于对g(x)在[-1, 1]上积分
    coefficients = np.zeros(n + 1)  # 存储系数 (a0,a1,...,an)
    approx = np.zeros_like(xs)  # 存储逼近多项式计算后的y值

    for i in range(n + 1):
        # 计算系数，并把系数×多项式加到y值里面
        coefficients[i] = inner_product(f, cheb_poly(i)) / \
                          inner_product(cheb_poly(i), cheb_poly(i))
        approx += coefficients[i] * cheb_poly(i)(xs)

    return approx


# 构造最佳平方逼近多项式
n_values = [5, 6, 7, 8]
# 两个函数以及权函数
f1 = lambda x: x**5
f2 = lambda x: np.sin(np.pi * x) * np.exp(x)
rho = lambda x: 1 / np.sqrt(1 - x**2)

xs = np.linspace(0, 1, 1000)  # 在区间 [0, 1] 上取样点

bg_color = (0.95, 0.95, 0.95)

# (a) Approximation of f(x) = x^5
plt.figure()
plt.plot(xs, f1(xs), label="f (x)")
for n in n_values:
    approx = best_approximation(f1, n)
    plt.plot(xs, approx, label=f"n={n}")
plt.gca().set_facecolor(bg_color)
plt.xlabel("x")
plt.ylabel("y", rotation="horizontal")
plt.legend()
plt.title("Approximation of f(x) = x^5")
plt.show()

# (b) Approximation of f(x) = sin(pi*x) * e^x
plt.figure()
plt.plot(xs, f2(xs), label="f (x)")
for n in n_values:
    approx = best_approximation(f2, n)
    plt.plot(xs, approx, label=f"n={n}")
plt.gca().set_facecolor(bg_color)
plt.xlabel("x")
plt.ylabel("y", rotation="horizontal")
plt.legend()
plt.title("Approximation of f(x) = sin(pi*x) * e^x")
plt.show()
