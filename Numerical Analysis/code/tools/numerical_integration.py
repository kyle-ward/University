import math


class Gauss:
    # 求积节点数不超过5
    legendre_table = [
        [[0.0], [2.0]],
        [[-0.5773503, 0.5773503], [1.0, 1.0]],
        [[-0.7745967, 0.0, 0.7745967], [0.5555556, 0.8888889, 0.5555556]],
        [[-0.8611363, -0.3399810, 0.3399810, 0.8611363], [0.3478548, 0.6521452, 0.6521452, 0.3478548]],
        [[-0.9061798, -0.5384693, 0.0, 0.5384693, 0.9061798], [0.2369269, 0.4786287, 0.5688889, 0.4786287, 0.2369269]],
        [[-0.9324695, -0.6612904, -0.2386192, 0.2386192, 0.6612094, 0.9324695], [0.1713245, 0.3607616, 0.4679139, 0.4679139, 0.3607616, 0.1713245]]
    ]

    # 默认积分区间都是[-1， 1]
    def Legendre(self, func, n):
        goal_data = self.legendre_table[n]
        _xs, _as = [], []
        for i in range(n + 1):
            _xs.append(goal_data[0][i])
            _as.append(goal_data[1][i])

        result = 0.0
        for i in range(n + 1):
            result += _as[i] * func(_xs[i])
        return result


class Composite:
    @staticmethod
    def Rectangle(func, a, b, n):
        _xs = [(a + (b - a) * (k / n)) for k in range(n + 1)]
        result = 0.0
        for i in range(n):
            # [_xs[i], _xs[i + 1]]
            ta, tb = _xs[i], _xs[i + 1]
            result += (tb - ta) * (func(ta) + func(tb)) / 2
        return result

    @staticmethod
    def Simpson(func, a, b, n):
        _xs = [(a + (b - a) * (k / n)) for k in range(n + 1)]
        result = 0.0
        for i in range(n):
            # [_xs[i], _xs[i + 1]]
            ta, tb = _xs[i], _xs[i + 1]
            result += ((tb - ta)/6) * (func(ta) + 4 * func((ta + tb)/2) + func(tb))
        return result

    # 只有两个求积节点
    @staticmethod
    def Gauss(func, a, b, n):
        gauss = Gauss()
        result = 0.0
        boundary_points = [(a + (b - a) * (k / n)) for k in range(n + 1)]
        for i in range(n):
            ta, tb = boundary_points[i], boundary_points[i + 1]

            def g(xs):
                return ((tb - ta) / 2) * func(((tb - ta) / 2) * xs + (ta + tb) / 2)
            result += gauss.Legendre(g, 2)
        return result

