import numpy as np
import time
def gauss_elimination(A, B):
    n = len(B)  # 获取向量B的长度，即线性方程组的维度
    AB = np.column_stack((A, B))  # 将矩阵A和向量B按列合并，形成增广矩阵AB

    # 前向消元
    for i in range(n):
        # 主元选取
        max_row = i  # 假设当前行为最大主元所在的行
        for j in range(i + 1, n):
            if abs(AB[j, i]) > abs(AB[max_row, i]):
                max_row = j  # 更新最大主元所在的行
        AB[[i, max_row]] = AB[[max_row, i]]  # 交换行，将最大主元所在行移动到当前行

        # 消元
        for j in range(i + 1, n):
            factor = AB[j, i] / AB[i, i]  # 计算消元的倍乘因子
            for k in range(i, n + 1):
                AB[j, k] -= factor * AB[i, k]  # 将当前行的倍乘因子倍乘后加到下一行，实现消元操作

    # 回代求解(逆序)
    x = np.zeros(n)  # 创建一个与维度n相同的零向量x，用于存储解
    for i in range(n - 1, -1, -1):
        x[i] = AB[i, n]  # 将增广矩阵AB的最后一列元素赋值给x的第i个元素，作为初始值
        for j in range(i + 1, n):
            x[i] -= AB[i, j] * x[j]  # 用已知的解部分计算x的第i个元素
        x[i] /= AB[i, i]  # 将计算得到的x的第i个元素除以AB的第i行第i列的元素，得到最终的解

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
    print("共耗费了%fs" %average_time)
    print("数值误差评估结果：", average_error)
