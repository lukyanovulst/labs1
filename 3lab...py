import copy

def read_matrix_from_file(filename):
    with open(filename, 'r') as f:
        return [list(map(int, line.split())) for line in f]

def extract_submatrix(M, n):
    return [row[:n] for row in M[:n]]

def print_matrix(M, name):
    print(f"\n{name}:")
    for row in M:
        print(" ".join(f"{x:4}" for x in row))

def in_region(i, j, n, region):
    if region == 1:
        return i < j and i + j > n - 1
    if region == 2:
        return i > j and i + j > n - 1
    if region == 3:
        return i > j and i + j < n - 1
    if region == 4:
        return i < j and i + j < n - 1
    return False

def count_zeros_in_region(M, n, region, col_parity=1):
    cnt = 0
    for i in range(n):
        for j in range(n):
            if in_region(i, j, n, region) and (j % 2 == col_parity) and M[i][j] == 0:
                cnt += 1
    return cnt

def product_in_region(M, n, region, row_parity=0):
    prod = 1
    found = False
    for i in range(n):
        if i % 2 == row_parity:
            for j in range(n):
                if in_region(i, j, n, region):
                    prod *= M[i][j]
                    found = True
    return prod if found else 1

def swap_regions_sym(M, n, r1, r2):
    for i in range(n):
        for j in range(n):
            if in_region(i, j, n, r1):
                ii, jj = n - 1 - i, n - 1 - j
                if in_region(ii, jj, n, r2):
                    M[i][j], M[ii][jj] = M[ii][jj], M[i][j]

def swap_regions_asym(M, n, r1, r2):
    for i in range(n):
        for j in range(n):
            if in_region(i, j, n, r1):
                ii, jj = n - 1 - j, n - 1 - i
                if in_region(ii, jj, n, r2):
                    M[i][j], M[ii][jj] = M[ii][jj], M[i][j]

def transpose(M):
    return [list(row) for row in zip(*M)]

def mul(A, B):
    p, q, r = len(A), len(B), len(B[0])
    return [[sum(A[i][k] * B[k][j] for k in range(q)) for j in range(r)] for i in range(p)]

def scale(M, k):
    return [[k * x for x in row] for row in M]

def sub(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A))] for i in range(len(A))]

if __name__ == "__main__":
    k = int(input("Введите целочисленный множитель K: "))
    n = int(input("Введите порядок матрицы n: "))
    try:
        full = read_matrix_from_file('matrix_data2.txt')
        A = extract_submatrix(full, n)
    except Exception as e:
        print("Ошибка:", e)
        exit(1)

    print_matrix(A, "Матрица A (исходная)")

    z4 = count_zeros_in_region(A, n, region=4, col_parity=1)
    p1 = product_in_region(A, n, region=1, row_parity=0)

    print(f"\nНулей в нечётных столбцах области 4 (верх): {z4}")
    print(f"Произведение в чётных строках области 1 (право): {p1}")
    print(f"Проверяем условие: {z4} * {k} {'>' if z4 * k > p1 else '<='} {p1}")

    F = copy.deepcopy(A)
    if z4 * k > p1:
        swap_regions_sym(F, n, r1=1, r2=2)
        print("→ Симметрично обменяли области 1 ↔ 2 (право ↔ низ)")
    else:
        swap_regions_asym(F, n, r1=2, r2=3)
        print("→ Асимметрично обменяли области 2 ↔ 3 (низ ↔ лево)")

    print_matrix(F, "Матрица F после обмена областей")

    AF = mul(A, F)
    print_matrix(AF, "A × F")

    FT = transpose(F)
    print_matrix(FT, "Fᵀ")

    KF = scale(FT, k)
    print_matrix(KF, "K × Fᵀ")

    res = sub(AF, KF)
    print_matrix(res, "Результат A×F − K×Fᵀ")
