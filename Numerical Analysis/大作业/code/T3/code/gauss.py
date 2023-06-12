import numpy as np
import time

def gauss_elimination(A, B):
    n = len(B)
    AB = np.column_stack((A, B))  # 形成增广矩阵

    for i in range(n):
        # 部分主元选取
        max_row = i
        for j in range(i + 1, n):
            if abs(AB[j, i]) > abs(AB[max_row, i]):     # 选绝对值最大的作为主元
                max_row = j
        AB[[i, max_row]] = AB[[max_row, i]]  # 交换行

        # 前向消元
        for j in range(i + 1, n):
            factor = AB[j, i] / AB[i, i]
            AB[j] -= factor * AB[i]     # 让每一列主元下的元素为0

    # 回代求解(逆序)
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = AB[i, n]  # 式子左边等于右边
        for j in range(i + 1, n):
            x[i] -= AB[i, j] * x[j]  # 减去已知解的部分
        x[i] /= AB[i, i]  # 除以系数得到答案

    return x

def compute_numerical_error(A, B, x):
    # 计算验证向量 y
    y = np.dot(A, x) - B

    # 计算验证向量 y 的范数
    error = np.linalg.norm(y)

    return error

if __name__ == "__main__":
    r_num = 100
    total_time = 0
    A = np.array([[10.0, 1.0, 2.0, 3.0, 4.0],
                [1.0, 9.0, -1.0, 2.0, -3.0],
                [2.0, -1.0, 7.0, 3.0, -5.0],
                [3.0, 2.0, 3.0, 12.0, -1.0],
                [4.0, -3.0, -5.0, -1.0, 15.0]])

    B = np.array([12.0, -27.0, 14.0, -17.0, 12.0])
    errors = []
    for _ in range(r_num):
        start_time = time.time()
        x = gauss_elimination(A, B)
        end_time = time.time()
        total_time += end_time - start_time
        error = compute_numerical_error(A, B, x)
        errors.append(error)
    average_time = total_time / r_num
    average_error = np.mean(errors)
    print("方程组的解：", x)
    print("共耗费了：%fs" %average_time)
    print("数值误差评估结果：", average_error)
