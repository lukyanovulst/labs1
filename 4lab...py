import numpy as np
import matplotlib.pyplot as plt

np.set_printoptions(precision=2, suppress=True)

def read_matrix_from_file(filename):
    return np.loadtxt(filename, dtype=int)

def print_matrix(m, title):
    print(f"\n{title}:")
    for row in m:
        print(" ".join(f"{int(x):6d}" for x in row))

def swap_C_B_symmetrically(mat, n):
    half = n // 2
    for i in range(half, n):
        for j in range(half):
            mat[i, j], mat[i, n-1-j] = mat[i, n-1-j], mat[i, j]

def swap_C_E_asymmetrically(mat, n):
    half = n // 2
    for i in range(half):
        for j in range(half):
            mat[half + i, j], mat[i, half + j] = mat[i, half + j], mat[half + i, j]

def count_numbers_greater_than_k_in_odd_cols_C(matrix, k, n):
    half = n // 2
    C = matrix[half:n, :half]
    odd_cols = np.arange(C.shape[1]) % 2 == 1
    return np.sum(C[:, odd_cols] > k)

def product_in_odd_rows_B(matrix, n):
    half = n // 2
    B = matrix[half:n, half:n]
    odd_rows = np.arange(B.shape[0]) % 2 == 1
    vals = B[odd_rows, :]
    return int(np.prod(vals)) if vals.size else 0

def create_lower_triangular(matrix):
    return np.tril(matrix)

def plot_matrices(matrices, titles):
    fig, axes = plt.subplots(1, len(matrices), figsize=(5*len(matrices), 5))
    axes[0].plot(matrices[0].mean(axis=1), marker='o', label=titles[0])
    axes[0].legend()
    axes[1].hist(matrices[1].flatten(), bins=20, label=titles[1])
    axes[1].legend()
    if len(matrices) > 2:
        axes[2].scatter(matrices[0].flatten(), matrices[2].flatten(), alpha=0.7)
        axes[2].legend([f'{titles[0]} vs {titles[2]}'])
    for ax in axes:
        ax.grid(True)
    plt.tight_layout()
    plt.show()

def main():
    n = int(input('Введите размерность N: '))
    k = int(input('Введите число k: '))
    A_full = read_matrix_from_file('matrix_data2.txt')
    if A_full.shape[0] < n or A_full.shape[1] < n:
        print(f"Ошибка: в файле недостаточно данных для матрицы {n}×{n}")
        return
    A = A_full[:n, :n]
    print_matrix(A, 'Матрица A (ввод)')
    if n % 2 == 1:
        mid = n // 2
        A = np.delete(np.delete(A, mid, axis=0), mid, axis=1)
        n = A.shape[0]
        print_matrix(A, f'После удаления середины ({n}×{n})')
    F = A.copy()
    print_matrix(F, 'Матрица F до преобразований')
    c = count_numbers_greater_than_k_in_odd_cols_C(F, k, n)
    p = product_in_odd_rows_B(F, n)
    print(f"Количество >{k} в нечётных столбцах C: {c}")
    print(f"Произведение в нечётных строках B: {p}")
    if c * k > p:
        swap_C_B_symmetrically(F, n)
        print("→ Симметричный обмен C↔B выполнен")
    else:
        swap_C_E_asymmetrically(F, n)
        print("→ Асимметричный обмен C↔E выполнен")
    print_matrix(F, 'Матрица F после преобразований')
    detA = float(np.round(np.linalg.det(A), 2))
    sumF = float(np.round(np.trace(F), 2))
    print(f"\ndet(A) = {detA:.2f}, trace(F) = {sumF:.2f}")
    if detA > sumF:
        try:
            result = A @ A.T - k * np.linalg.inv(F)
        except np.linalg.LinAlgError:
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
