import math
import tools.numerical_integration as ni
import matplotlib.pyplot as plt
import numpy as np


def f(x):
    if x == 0.0:
        x = 0.00000001
    return math.log(x, math.e) * (x ** 0.5)


h_list = [0.008, 0.01, 0.02, 0.04, 0.05, 0.1, 0.2, 0.5]
n_list = np.arange(2, 11)
composite = ni.Composite()
xs1, ys1 = [], []
xs2, ys2 = [], []
for n in n_list:
    h = 1 / n
    result1 = composite.Simpson(f, 0, 1, n)
    result2 = composite.Rectangle(f, 0, 1, n)
    xs1.append(h)
    xs2.append(h)
    ys1.append(math.fabs((-4 / 9) - result1))
    ys2.append(math.fabs((-4 / 9) - result2))
    print('result1 =', result1, '\t delta =', math.fabs((-4 / 9) - result1))
    print('result2 =', result2, '\t delta =', math.fabs((-4 / 9) - result2))
    print('------------------------------------------------------------')
plt.plot(xs1, ys1, 'b')
plt.plot(xs2, ys2, 'r')
plt.show()





