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

def count_zeros_in_area4(M, n):
    cnt = 0
    for i in range(n):
        for j in range(n):
            if i > j and i + j > n - 1 and j % 2 == 1 and M[i][j] == 0:
                cnt += 1
    return cnt

def product_in_area1(M, n):
    prod = 1
    for i in range(n):
        if i % 2 == 0:
            for j in range(n):
                if j < i and j < n - 1 - i:
                    prod *= M[i][j]
    return prod

def swap_areas_1_2_sym(M, n):
    for i in range(n):
        for j in range(n):
            if j < i and j < n - 1 - i:
                ii, jj = n - 1 - j, n - 1 - i
                M[i][j], M[ii][jj] = M[ii][jj], M[i][j]

def swap_areas_2_3_asym(M, n):
    for i in range(n):
        for j in range(n):
            if i < j and i < n - 1 - j:
                ii, jj = n - 1 - j, n - 1 - i
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

k = int(input("Введите целочисленный множитель K: "))
n = int(input("Введите порядок матрицы n: "))

try:
    full = read_matrix_from_file('matrix_data2.txt')
    if len(full) < n or any(len(r) < n for r in full):
        raise ValueError("Матрица в файле меньше заявленного размера")
    A = extract_submatrix(full, n)
except Exception as e:
    print("Ошибка:", e)
    exit(1)

print_matrix(A, "Матрица A (исходная)")

F = copy.deepcopy(A)

z4 = count_zeros_in_area4(F, n)
p1 = product_in_area1(F, n)

print(f"\nНулей в нечётных столбцах области 4 (низ): {z4}")
print(f"Произведение в нечётных строках области 1 (лево): {p1}")
print(f"Проверяем условие: {z4} * {k} {'>' if z4 * k > p1 else '<='} {p1}")

if z4 * k > p1:
    swap_areas_1_2_sym(F, n)
    print("→ Симметрично обменяли области 1 ↔ 2 (лево ↔ верх)")
else:
    swap_areas_2_3_asym(F, n)
    print("→ Асимметрично обменяли области 2 ↔ 3 (верх ↔ право)")

print_matrix(F, "Матрица F после обмена областей")

AF = mul(A, F)
print_matrix(AF, "A × F")

FT = transpose(F)
print_matrix(FT, "Fᵀ")

KF = scale(FT, k)
print_matrix(KF, "K × Fᵀ")

res = sub(AF, KF)
print_matrix(res, "Результат A×F − K×Fᵀ")
