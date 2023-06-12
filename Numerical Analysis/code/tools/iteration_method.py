import numpy as np
from copy import deepcopy


def print_matrix(mat):
    if len(mat) != len(mat[0]):
        print('print matrix error.')
        return

    for row in mat:
        for num in row:
            print(num, end=' \t')
        print()
    print('----------------')


class Basic:
    A = None
    L, U, D = None, None, None
    M, N = None, None
    B, f = None, None
    final_solution = None
    initial_solution = []
    error = 0.000005
    count = 0

    def __init__(self, mat, b):
        if len(mat) != len(b) or len(mat[0]) != len(b) or len(mat) != len(mat[0]):
            print('error!')
            return

        self.n = len(b)
        self.A = deepcopy(mat)
        self.L, self.U, self.D = [], [], []
        self.initial_solution = [1.0] * self.n
        for row in range(self.n):
            l_row, d_row, u_row = [], [], []
            for col in range(self.n):
                if row < col:
                    u_row.append(-mat[row][col] if mat[row][col] != 0.0 else 0.0)
                    d_row.append(0.0)
                    l_row.append(0.0)
                elif row == col:
                    d_row.append(mat[row][col])
                    l_row.append(0.0)
                    u_row.append(0.0)
                elif row > col:
                    l_row.append(-mat[row][col] if mat[row][col] != 0.0 else 0.0)
                    d_row.append(0.0)
                    u_row.append(0.0)
                else:
                    pass
            self.L.append(l_row)
            self.D.append(d_row)
            self.U.append(u_row)
        self.L = np.array(self.L)
        self.D = np.array(self.D)
        self.U = np.array(self.U)

    def ldu_print(self):
        print('L:')
        print_matrix(self.L)
        print('D:')
        print_matrix(self.D)
        print('U:')
        print_matrix(self.U)

    @staticmethod
    def GetError(new_xs, xs):
        choices = ['absolute', 'relative']
        choice = choices[0]
        if choice == 'absolute':
            exact_solution = np.array([0.5, 1.0, -0.5])
            temp = exact_solution - new_xs
        else:
            temp = new_xs - xs
        return max(np.maximum(temp, -temp))

    def Solve(self):
        xs = deepcopy(self.initial_solution)
        print('enter while:')
        while True and self.count < 10:
            new_xs = np.dot(self.B, xs) + self.f
            print('new_xs:', new_xs, '(', self.GetError(new_xs, xs), ')')
            self.count += 1
            if self.GetError(new_xs, xs) < self.error:
                self.final_solution = new_xs
                break
            xs = new_xs

    def PrintAnswer(self):
        # print('equations:')
        for row_i in range(self.n):
            for col_i in range(self.n):
                # print('%.6fx' % self.B[row_i][col_i] + str(col_i + 1), end=' + ')
                pass
            # print('\b\b= %.6f' % self.f[row_i])
            pass
        print('answer:', self.final_solution)
        print('count: ', self.count)

    def Tradition(self):
        pass

    def __str__(self):
        pass


class Jacobi(Basic):
    def __init__(self, mat, b):
        super().__init__(mat, b)
        self.M = deepcopy(self.D)
        self.N = deepcopy(self.L + self.U)
        self.B = np.dot(np.linalg.inv(self.M), self.N)
        self.f = np.dot(np.linalg.inv(self.M), np.array(b))
        print('finish initializing.')
        self.Solve()
        self.PrintAnswer()

    def ConvergenceSpeed(self):
        pass


class GaussSeidel(Basic):
    def __init__(self, mat, b):
        super().__init__(mat, b)
        self.M = deepcopy(self.D - self.L)
        self.N = deepcopy(self.U)
        self.B = np.dot(np.linalg.inv(self.M), self.N)
        self.f = np.dot(np.linalg.inv(self.M), np.array(b))
        print('finish initializing.')
        self.Solve()
        self.PrintAnswer()

    def ConvergenceSpeed(self):
        pass


class SOR(Basic):
    w = 1.1

    def __init__(self, mat, b):
        super().__init__(mat, b)
        self.M = (1 / self.w) * (self.D - self.w * self.L)
        self.B = np.dot(np.linalg.inv(self.D - self.w * self.L), ((1 - self.w) * self.D + self.w * self.U))
        self.f = np.dot(np.linalg.inv(self.M), np.array(b))
        print('finish initializing.')
        self.Solve()
        self.PrintAnswer()

    def IsConvergent(self):
        flag = 1
        if flag:
            pass
        else:
            pass

    def ConvergenceSpeed(self):
        pass


class CG:
    alpha_l, beta_l = [], []
    p_l, r_l, x_l = [], [], []
    cnt = 0

    def __init__(self, mat, b):
        if len(mat) != len(mat[0]) or len(mat) != len(b):
            raise 'format error!'
        self.A = np.array(mat)
        self.b = np.array(b)
        self.n = len(b)
        self.x_init = np.array([0] * self.n)

    def Solution(self):
        self.x_l.append(self.x_init)
        self.p_l.append(self.b - np.dot(self.A, self.x_init))
        self.r_l.append(self.b - np.dot(self.A, self.x_init))
        k = 0
        while True:
            self.alpha_l.append(np.dot(self.r_l[k], self.r_l[k]) / np.dot(self.p_l[k], np.dot(self.A, self.p_l[k])))
            self.x_l.append(self.x_l[k] + self.alpha_l[k] * self.p_l[k])
            self.r_l.append(self.r_l[k] - self.alpha_l[k] * np.dot(self.A, self.p_l[k]))
            self.beta_l.append(np.dot(self.r_l[k + 1], self.r_l[k + 1]) / np.dot(self.r_l[k], self.r_l[k]))


if __name__ == '__main__':
    a1 = [[4.0, -1.0, 0.0], [-1.0, 4.0, -1.0], [0.0, -1.0, 4.0]]
    vec1 = [1.0, 4.0, -3.0]

    a2 = [[5.0, 2.0, 1.0], [-1.0, 4.0, 2.0], [2.0, -3.0, 10.0]]
    vec2 = [-12.0, 20.0, 3.0]
    tt = SOR(a1, vec1)


