import numpy as np
import matplotlib.pyplot as plt

np.set_printoptions(precision=2, suppress=True)

def read_matrix_from_file(filename):
    return np.loadtxt(filename, dtype=int)

def print_matrix(m, title):
    print(f"\n{title}:")
    if m.ndim == 2:
        for row in m:
            print(" ".join(f"{int(x):6d}" for x in row))
    else:
        print(m)

def swap_B_C_symmetrically(mat):
    m = mat.shape[0]
    half = m // 2
    for i in range(half):
        for j in range(half):
            cj = half + j
            mat[i, j], mat[i, m-1-j] = mat[i, m-1-j], mat[i, j]

def swap_C_E_asymmetrically(mat):
    m = mat.shape[0]
    half = m // 2
    for i in range(half):
        for j in range(half):
            ci, cj = i, half + j
            ei, ej = half + i, half + j
            mat[ci, cj], mat[ei, ej] = mat[ei, ej], mat[ci, cj]

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

def count_gt_C(matrix, k):
    m = matrix.shape[0]
    half = m // 2
    C = matrix[:half, half:m]
    cols = np.arange(half) % 2 == 0
    return np.sum(C[:, cols] > k)

def product_B(matrix):
    m = matrix.shape[0]
    half = m // 2
    B = matrix[:half, :half]
    rows = np.arange(half) % 2 == 0
    vals = B[rows, :]
    return int(np.prod(vals)) if vals.size else 0

def main():
    n = int(input('Введите размерность N: '))
    k = int(input('Введите число k: '))
    A_full = read_matrix_from_file('matrix_data2.txt')
    N = A_full.shape[0]
    A = A_full.copy()
    if n < N:
        start = (N - n) // 2
        A = A_full[start:start+n, start:start+n]
    print_matrix(A, 'Матрица A (ввод)')
    if n % 2 == 1:
        mid = n // 2
        A = np.delete(np.delete(A, mid, axis=0), mid, axis=1)
    print_matrix(A, f'Матрица A после удаления середины ({A.shape[0]}×{A.shape[1]})')
    F = A.copy()
    m = F.shape[0]
    print_matrix(F, 'Матрица F до преобразований')
    c = count_gt_C(F, k)
    p = product_B(F)
    print(f"Количество >k в нечётных столбцах блока C: {c}")
    print(f"Произведение в нечётных строках блока B: {p}")
    if c * k > p:
        swap_B_C_symmetrically(F)
        print('Симметричный обмен B и C выполнен')
    else:
        swap_C_E_asymmetrically(F)
        print('Несимметричный обмен C и E выполнен')
    print_matrix(F, 'Матрица F после преобразований')
    detA = float(np.round(np.linalg.det(A), 2))
    sumF = float(np.round(np.trace(F), 2))
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
        print_matrix(result, 'Итоговая матрица')
        plot_matrices([A, F, result], ['A', 'F', 'Result'])
    else:
        plot_matrices([A, F], ['A', 'F'])

if __name__ == '__main__':
    main()
