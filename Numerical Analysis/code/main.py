import numpy as np


# 矩阵乘法：np.dot(A, B)
# 矩阵转置， 矩阵求逆 np.transpose(A), np.linalg.inv(A)
# 矩阵特征值， 特征向量 = np.linalg.eig(A) (eigvals)
# 矩阵行列式：np.linalg.det(A)
# 矩阵求范数


A = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
Y = np.array([[2, 0, 0], [0, 3, 0], [0, 0, 4]])
print(2 * A)
print(A * np.array([1, 1, 1]))
print(np.dot(A, np.array([1, 1, 1])))
# A = np.matrix(A)
print(np.linalg.inv(Y))
a = np.array([-1,3,2,-100])
print(max(a))
print(max(np.maximum(a, -a)))
print('---------')
print(np.dot(np.linalg.inv(np.array([[3.0, 0.0, 0.0], [0.0, 2.0, 0.0], [-2.0, 1.0, 2.0]])), np.array([[0.0, 0.0, 2.0], [0.0, 0.0, -1.0], [0.0, 0.0, 0.0]])))

print('--  --   --')
print('answer: %.4fx' % 1.00009 + '1234')
print('----------------------------------------------')
a = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
c = np.array([2, 3, 4])
b = np.array([2, 3, 4])
print(b * a)
print(np.dot(a, b))
print(np.dot(b, a))
print(np.dot(b, c))
print(b * c)

