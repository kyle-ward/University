import numpy as np
import copy


# 初等置换矩阵的性质
# 上下三角矩阵分别如何求逆
# m的推导
# 求解LU以及依次求Li，Li与L的关系
# 对称正定矩阵，主元之间的性质


# 高斯消去法
class Gauss:
    xs = []

    def __init__(self, mat, b):
        self.original = mat  # 记录原矩阵
        self.A = copy.deepcopy(mat)  # 待高斯化简矩阵
        self.b = copy.deepcopy(b)  # 待高斯化简b
        self.n = len(mat)
        self.Simplify()
        self.Solve()

    def __str__(self):
        mat_str = 'det(A):\t' + str(round(self.GetDet(), 3)) + '\n'
        for index, row in enumerate(self.A):
            temp = []
            for num in row:
                temp.append(str(round(num, 3)))
            mat_str += '\t\t' + '     \t'.join(temp) + '     \t-> ' + str(self.b[index]) + '\n'
        mat_str += 'Solve:\t' + '     \t'.join(self.xs) + '\n'
        mat_str += 'Cond:\t' + str(self.GetCond()) + '\n\n'
        return 'Gauss:\n' + mat_str

    # 对self.A进行高斯化简
    def Simplify(self):
        for st in range(self.n - 1):
            # print(self.A, end='\n------------------------------------\n')
            for cur in range(st + 1, self.n):
                alpha = self.A[cur][st] / self.A[st][st]
                self.A[cur] = self.A[cur] - self.A[st] * alpha
                self.b[cur] = self.b[cur] - self.b[st] * alpha

    # 计算输入原矩阵的条件数
    def GetCond(self):
        m1 = max(np.linalg.eigvals(np.dot(self.original.T, self.original)))
        m2 = min(np.linalg.eigvals(np.dot(self.original, self.original.T)))
        return (m1 / m2) ** 0.5

    # 计算矩阵行列式（化简前后行列式保持不变）
    def GetDet(self):
        ans = 1
        for i in range(self.n):
            ans *= self.A[i][i]
        return ans

    # 对于输入的matrix与b，求解xs
    def Solve(self):
        for i in range(self.n - 1, -1, -1):
            temp = 0
            for j in range(i + 1, self.n):
                temp += self.A[i][j] * self.xs[j - i - 1]
            self.xs = [(self.b[i] - temp) / self.A[i][i]] + self.xs
        for i in range(len(self.xs)):
            self.xs[i] = str(round(self.xs[i], 3))


# LU分解
class LU:
    pass


if __name__ == '__main__':
    # test_A = np.array([12.0, -3.0, 3.0, -18.0, 3.0, -1.0, 1.0, 1.0, 1.0]).reshape(3, 3)
    # test_b = np.array([15.0, -15.0, 6.0])
    # test = Gauss(test_A, test_b)
    inp1_A = np.array([3.01, 6.03, 1.99, 1.27, 4.16, -1.23, 0.987, -4.81, 9.34]).reshape(3, 3)
    inp2_A = np.array([3.00, 6.03, 1.99, 1.27, 4.16, -1.23, 0.990, -4.81, 9.34]).reshape(3, 3)
    inp1_b = inp2_b = np.array([1.0, 1.0, 1.0])
    test1 = Gauss(inp1_A, inp1_b)
    test2 = Gauss(inp2_A, inp2_b)
    print('(1)')
    print(test1)
    print('(2)')
    print(test2)

