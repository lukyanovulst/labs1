import numpy as np
import matplotlib.pyplot as plt

np.set_printoptions(precision=2, suppress=True)

def read_matrix_from_file(filename):
    return np.loadtxt(filename, dtype=int)

def print_matrix(m, title):
    print(f"\n{title}:")
    for row in m:
        if np.issubdtype(m.dtype, np.floating):
            print(" ".join(f"{x:6.2f}" for x in row))
        else:
            print(" ".join(f"{int(x):6d}" for x in row))

def swap_B_C_symmetrically(mat, n):
    half = n // 2
    for i in range(half):
        for j in range(half):
            ci, cj = half + i, j
            bi, bj = half + i, n - 1 - j
            mat[ci, cj], mat[bi, bj] = mat[bi, bj], mat[ci, cj]

def swap_C_E_asymmetrically(mat, n):
    half = n // 2
    for i in range(half):
        for j in range(half):
            ci, cj = half + i, j
            ei, ej = i, half + j
            mat[ci, cj], mat[ei, ej] = mat[ei, ej], mat[ci, cj]

def create_lower_triangular(matrix):
    return np.tril(matrix)

def plot_matrices(matrices, titles):
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    axes[0].plot(matrices[0].mean(axis=1), marker='o', label=titles[0])
    axes[0].legend()
    axes[1].hist(matrices[1].flatten(), bins=20, label=titles[1])
    axes[1].legend()
    if len(matrices) > 2:
        axes[2].scatter(matrices[0].flatten(), matrices[2].flatten(), alpha=0.7)
        axes[2].legend([f'{titles[0]} vs {titles[2]}'])
    else:
        axes[2].axis('off')
    plt.tight_layout()
    plt.show()

def count_gt(matrix, k, n):
    half = n // 2
    C = matrix[half:n, 0:half]
    cols = np.arange(half) % 2 == 0
    return np.sum(C[:, cols] > k)

def product_odd_rows(matrix, n):
    half = n // 2
    C = matrix[half:n, 0:half]
    rows = np.arange(half) % 2 == 0
    vals = C[rows, :]
    return int(np.prod(vals)) if vals.size else 0

def main():
    n = int(input('Введите размерность N: '))
    if n <= 1 or n % 2 != 0:
        print('Ошибка: N должно быть чётным числом больше 1')
        return
    k = int(input('Введите число k: '))
    try:
        A_full = read_matrix_from_file('matrix_data2.txt')
    except:
        print('Ошибка чтения файла')
        return
    if A_full.shape[0] < n or A_full.shape[1] < n:
        print(f'Ошибка: недостаточно данных для матрицы {n}×{n}')
        return
    A = A_full[:n, :n]
    print_matrix(A, 'Матрица A')
    F = A.copy()
    c = count_gt(F, k, n)
    p = product_odd_rows(F, n)
    if c > p:
        swap_B_C_symmetrically(F, n)
        print('\nВыполнен симметричный обмен блоков C и B')
    else:
        swap_C_E_asymmetrically(F, n)
        print('Выполнен асимметричный обмен блоков C и E')
    print_matrix(F, 'Матрица F после преобразований')
    detA = float(np.round(np.linalg.det(A), 2))
    sumF = float(np.round(np.trace(F), 2))
    print(f"\ndet(A) = {detA:.2f}")
    print(f"sum(diag(F)) = {sumF:.2f}")
    if detA > sumF:
        try:
            result = A @ A.T - k * np.linalg.inv(F)
        except:
            result = None
    else:
        G = create_lower_triangular(A)
        result = k * (A + G - F.T)
    if result is not None:
        result = np.round(result, 2)
        print_matrix(result, 'Итоговая матрица Result')
        plot_matrices([A, F, result], ['A', 'F', 'Result'])
    else:
        plot_matrices([A, F], ['A', 'F'])

if __name__ == '__main__':
    main()
