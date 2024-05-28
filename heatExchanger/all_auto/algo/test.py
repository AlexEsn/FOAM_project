import numpy as np


def transform_matrix(A):
    M, N = A.shape

    # Обнуление второй диагонали
    for i in range(min(M, N)):
        A[i, N-1-i] = 0

    # Обнуление элементов под второй диагональю (лесенка)
    for i in range(1, M):
        if N - i >= 0:
            A[i, N-1-i + 1] = 0

    return A


# Пример использования
A = np.array([[1,  2,  3,  4,  5,  6],
              [7,  8,  9, 10, 11, 12],
              [13, 14, 15, 16, 17, 18],
              [19, 20, 21, 22, 23, 24],
              [25, 26, 27, 28, 29, 30],
              [31, 32, 33, 34, 35, 36]])

print("Исходная матрица:")
print(A)

A_transformed = transform_matrix(A)

print("Преобразованная матрица:")
print(A_transformed)
