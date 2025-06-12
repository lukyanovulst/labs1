#18.F(1) = 2; G(1) = 1; F(n) =(-1)n*( F(n–1) – G(n–1) /(2n)!), G(n) = F(n–1) + G(n–1), при n >=2
import math
import timeit
import matplotlib.pyplot as plt

def FG_recursive(n: int):
    if n == 1:
        return 2.0, 1.0
    prev_F, prev_G = FG_recursive(n - 1)
    sign = 1.0 if n % 2 == 0 else -1.0
    F = sign * (prev_F - prev_G / math.factorial(2 * n))
    G = prev_F + prev_G
    return F, G

def FG_iterative(n: int):
    F, G = 2.0, 1.0
    fact = math.factorial(2)
    for i in range(2, n + 1):
        fact *= (2 * i - 1) * (2 * i)
        sign = 1.0 if i % 2 == 0 else -1.0
        F, G = sign * (F - G / fact), F + G
    return F, G

results = []
for n in range(1, 16):
    t_rec = timeit.timeit(lambda: FG_recursive(n), number=50)
    t_itr = timeit.timeit(lambda: FG_iterative(n), number=50)
    results.append((n, t_rec, t_itr))

print(" n | Recursive Time (s) | Iterative Time (s)")
print("---+--------------------+--------------------")
for n, t_rec, t_itr in results:
    print(f"{n:2d} | {t_rec: .6f}          | {t_itr: .6f}")

xs = [r[0] for r in results]
yrec = [r[1] for r in results]
yitr = [r[2] for r in results]

plt.figure(figsize=(8,5))
plt.plot(xs, yrec, marker='o', label='Рекурсивный')
plt.plot(xs, yitr, marker='o', label='Итеративный')
plt.xlabel('n')
plt.ylabel('Время выполнения (с)')
plt.title('Сравнение рекурсивного и итеративного подходов')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
