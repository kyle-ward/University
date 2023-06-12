import numpy as np
import time


def backward_substitution(U, y):
    n = U.shape[0]  # 获取矩阵U的维度
    x = np.zeros(n)  # 创建一个与U的维度相同的零向量x

    for i in range(n-1, -1, -1):
        x[i] = y[i]  # 将y的第i个元素赋值给x的第i个元素
        for j in range(i+1, n):
            x[i] -= U[i, j] * x[j]  # 用已知的x的元素计算x的第i个元素
        x[i] /= U[i, i]  # 将计算得到的x的第i个元素除以U的第i行第i列的元素

    return x


def forward_substitution(L, B):
    n = L.shape[0]  # 获取矩阵L的维度
    y = np.zeros(n)  # 创建一个与L的维度相同的零向量y

    for i in range(n):
        y[i] = B[i]  # 将B的第i个元素赋值给y的第i个元素，作为初始值
        for j in range(i):
            y[i] -= L[i, j] * y[j]  # 用已知的y的元素计算y的第i个元素
        y[i] /= L[i, i]  # 将计算得到的y的第i个元素除以L的第i行第i列的元素

    return y


def compute_numerical_error(A, B, x):
    # 计算验证向量 y
    y = np.dot(A, x) - B

    # 计算验证向量 y 的范数
    error = np.linalg.norm(y)

    return error


# 将正定矩阵化为下三角矩阵
def cholesky_decomposition(A):
    n = A.shape[0]  # 获取矩阵A的维度
    L = np.zeros_like(A)  # 创建一个与A形状相同的零矩阵L

    for i in range(n):
        for j in range(i+1):
            if i == j:
                sum_sq = np.sum(L[i, :j]**2)
                # 计算已经计算过的对角线元素的平方和
                # ∑(L[i, k]^2), k=1 to j-1
                L[i, j] = np.sqrt(A[i, i] - sum_sq)
                # 计算L的第i行第j列元素的值
                # L[i, j] = √(A[i, i] - ∑(L[i, k]^2), k=1 to j-1)
            else:
                sum_prod = np.sum(L[i, :j] * L[j, :j])
                # 计算乘积之和
                # ∑(L[i, k] * L[j, k]), k=1 to j-1
                L[i, j] = (A[i, j] - sum_prod) / L[j, j]
                # 计算L的第i行第j列元素的值
                # L[i, j] = (A[i, j] - ∑(L[i, k] * L[j, k]), k=1 to j-1) / L[j, j]

    return L


if __name__ == "__main__":
    r_num = 100
    total_time = 0
    # 构建系数矩阵和右侧常数向量
    A = np.array([[10.0, 1.0, 2.0, 3.0, 4.0],
              [1.0, 9.0, -1.0, 2.0, -3.0],
              [2.0, -1.0, 7.0, 3.0, -5.0],
              [3.0, 2.0, 3.0, 12.0, -1.0],
              [4.0, -3.0, -5.0, -1.0, 15.0]])
    B = np.array([12.0, -27.0, 14.0, -17.0, 12.0])
    errors = []
    for _ in range(r_num):
        start_time = time.time()
        # Cholesky分解
        L = cholesky_decomposition(A)
        # print(L)

        # 前向替换
        y = forward_substitution(L, B)
        # print(y)

        # 后向替换
        X = np.linalg.solve(L.T, y)
        # print(X)
        end_time = time.time()
        total_time += end_time - start_time
        error = compute_numerical_error(A, B, X)
        errors.append(error)
    average_time = total_time / r_num
    average_error = np.mean(errors)
    print("方程组的解：", X)
    print("共耗费了%fs" % average_time)
    print("数值误差评估结果：", average_error)
