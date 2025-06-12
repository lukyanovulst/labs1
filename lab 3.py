def read_matrix(filename):
    with open(filename, 'r') as f:
        return [list(map(int, line.split())) for line in f if line.strip()]

def print_matrix(M, name):
    print(f"\n{name} ({len(M)}×{len(M)}):")
    for row in M:
        print(" ".join(f"{x:6}" for x in row))

def transpose(M):
    return [list(row) for row in zip(*M)]

def mat_mul(A, B):
    n, p, m = len(A), len(B), len(B[0])
    C = [[0]*m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def scalar_mult(K, M):
    return [[K * x for x in row] for row in M]

def get_regions(n):
    r1, r2, r3, r4 = [], [], [], []
    for i in range(n):
        for j in range(n):
            if i < j and i < n - 1 - j:
                r4.append((i, j))
            elif i < j and i > n - 1 - j:
                r1.append((i, j))
            elif i > j and i > n - 1 - j:
                r2.append((i, j))
            elif i > j and i < n - 1 - j:
                r3.append((i, j))
    return r1, r2, r3, r4

def build_F(A, K):
    n = len(A)
    F = [row[:] for row in A]
    r1, r2, r3, r4 = get_regions(n)
    zeros = sum(1 for (i, j) in r4 if j % 2 == 0 and A[i][j] == 0)
    prod, found = 1, False
    for (i, j) in r1:
        if i % 2 == 0:
            prod *= A[i][j]
            found = True
    if not found:
        prod = 1
    print("\n--- Проверка условия ---")
    print(f"Нули в области 4:              {zeros}")
    print(f"Произведение в области 1:      {prod}")
    print(f"Нули * K → {zeros} * {K} = {zeros * K}")
    print("------------------------------")
    if zeros * K > prod:
        print(f"Так как {zeros} * {K} = {zeros * K} > {prod},")
        print("выполняется симметричная замена областей 1 и 2 по главной диагонали.\n")
        for (i, j) in r1:
            F[i][j], F[j][i] = F[j][i], F[i][j]
    else:
        print(f"Так как {zeros} * {K} = {zeros * K} ≤ {prod},")
        print("выполняется несимметричная замена областей 2 и 3.\n")
        for ((i1, j1), (i2, j2)) in zip(r2, r3):
            F[i1][j1], F[i2][j2] = F[i2][j2], F[i1][j1]
    return F

def main():
    N = int(input("Введите размерность N: "))
    if N % 2 == 0 or N <= 1:
        raise ValueError("Размер матрицы N должен быть нечётным и >1")
    K = int(input("Введите целое K: "))
    A = read_matrix("matrix2.txt")
    if len(A) != N or any(len(row) != N for row in A):
        raise ValueError("matrix2.txt не содержит квадратную матрицу нужного размера")
    print_matrix(A, "Матрица A")
    F = build_F(A, K)
    print_matrix(F, "Матрица F")
    AF = mat_mul(A, F)
    print_matrix(AF, "A * F")
    FT = transpose(F)
    print_matrix(FT, "F^T")
    KFT = scalar_mult(K, FT)
    print_matrix(KFT, f"{K} * F^T")
    result = [[AF[i][j] + KFT[i][j] for j in range(N)] for i in range(N)]
    print_matrix(result, "Итог: A*F + K*F^T")

if __name__ == "__main__":
    main()
