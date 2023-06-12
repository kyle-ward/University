import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate as si


def P(n):
    if n == 0:
        return lambda x: 1
    elif n == 1:
        return lambda x: x
    else:
        return lambda x: (1 / n) * ((2 * n - 1) * x * P(n - 1)(x) - (n - 1) * P(n - 2)(x))


def T(n):
    if n == 0:
        return lambda x: 1
    elif n == 1:
        return lambda x: x
    else:
        return lambda x: 2 * x * T(n - 1)(x) - T(n - 2)(x)


# 计算f(x)与g(x)在[a, b]上的rho(x)加权内积
def inner_product(f, g, rho=lambda x: 1, a=-1, b=1):
    def t(x): return f(x) * g(x) * rho(x)
    result = si.quad(t, a, b)[0]
    return result


class FuncApprox:
    @staticmethod
    # 采用切比雪夫多项式，对f(x)在去区间[a, b]上进行n次最佳平方逼近
    def Chebyshev(func, a, b, n):
        # 对f(x)在[a, b]上积分等价于对g(x)在[-1, 1]上积分
        def rho(x): return np.sqrt(1 - x ** 2) ** -1

        def goal(x):
            result = 0.0
            for i in range(n + 1):
                ai = inner_product(T(i), func, rho) / inner_product(T(i), T(i), rho)
                result += ai * T(i)(x)
            return result
        return goal

    @staticmethod
    # 采用勒让德多项式，对f(x)在去区间[a, b]上进行n次最佳平方逼近
    def Legendre(func, a, b, n):
        # 对f(x)在[a, b]上积分等价于对g(x)在[-1, 1]上积分
        def goal(x):
            result = 0.0
            for i in range(n + 1):
                ai = inner_product(P(i), func) / inner_product(P(i), P(i))
                result += ai * P(i)(x)
            return result
        return goal


if __name__ == "__main__":
    def f1(x): return x ** 5
    def f2(x): return np.sin(np.pi * x) * np.exp(x)

    xs = np.linspace(0, 1, 101)
    bg_color = (0.95, 0.95, 0.95)
    plt.figure()
    n_list = np.arange(5, 9, 1)

    # f1
    plt.plot(xs, f1(xs), label='f(x)')
    for _n in n_list:
        g1 = FuncApprox.Legendre(f1, 0, 1, _n)
        plt.plot(xs, g1(xs), label=f'n={_n}')
    plt.gca().set_facecolor(bg_color)
    plt.xlabel('x')
    plt.ylabel('y', rotation='horizontal')
    plt.legend()
    plt.title("Approximation of f(x) = x^5")
    plt.show()

    # f2
    plt.plot(xs, f2(xs), label='f(x)')
    for _n in n_list:
        g2 = FuncApprox.Legendre(f2, 0, 1, _n)
        plt.plot(xs, g2(xs), label=f'n={_n}')
    plt.gca().set_facecolor(bg_color)
    plt.xlabel('x')
    plt.ylabel('y', rotation='horizontal')
    plt.legend()
    plt.title("Approximation of f(x) = sin(pi*x) * e^x")
    plt.show()








