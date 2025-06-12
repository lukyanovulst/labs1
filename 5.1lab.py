import itertools
import random
import timeit

def generate_compositions_recursive(total, k):
    result = []
    def helper(prefix, remaining, banks_left):
        if banks_left == 1:
            result.append(prefix + [remaining])
        else:
            for i in range(remaining + 1):
                helper(prefix + [i], remaining - i, banks_left - 1)
    helper([], total, k)
    return result

def generate_compositions_product(total, k):
    return [list(comb) for comb in itertools.product(range(total + 1), repeat=k) if sum(comb) == total]

if __name__ == "__main__":
    S = int(input("Введите общую сумму денег (целое неотрицательное): "))
    K = int(input("Введите количество банков (целое положительное): "))

    t1 = timeit.timeit(lambda: generate_compositions_recursive(S, K), number=1)
    rec_comps = generate_compositions_recursive(S, K)
    print("\nАлгоритмический метод:")
    print(f"Всего комбинаций: {len(rec_comps)}")
    print("Первые 5 комбинаций (каждая в новой строке):")
    for comb in rec_comps[:5]:
        print(comb)
    print(f"Время выполнения: {t1:.6f} сек")

    t2 = timeit.timeit(lambda: generate_compositions_product(S, K), number=1)
    prod_comps = generate_compositions_product(S, K)
    print("\nPython-функции метод:")
    print(f"Всего комбинаций: {len(prod_comps)}")
    print("Первые 5 комбинаций (каждая в новой строке):")
    for comb in prod_comps[:5]:
        print(comb)
    print(f"Время выполнения: {t2:.6f} сек")

    faster = "алгоритмический" if t1 < t2 else "Python-функции"
    print(f"\nБолее быстрый метод: {faster}")

    # 2 ЧАСТЬ
    capacities = []
    while True:
        capacities = [random.randint(0, S) for _ in range(K)]
        if sum(capacities) >= S:
            break

    rates = [round(random.uniform(0.01, 0.1), 3) for _ in range(K)] 
    print("\nХарактеристики банков:")
    print(f"Максимальные суммы (capacities): {capacities}")
    print(f"Доходности (rates): {rates}")

    valid = [comb for comb in rec_comps if all(comb[i] <= capacities[i] for i in range(K))]
    print(f"\nПосле введения ограничения переборов: {len(valid)} (раньше было {len(rec_comps)})")
    print("Первые 5 допустимых вариантов (каждая в новой строке):")
    for comb in valid[:5]:
        print(comb)

    yields = [sum(comb[i] * rates[i] for i in range(K)) for comb in valid]
    max_yield = max(yields) if yields else 0
    optimal = [valid[i] for i, y in enumerate(yields) if y == max_yield]
    print(f"\nОптимальных вариантов: {len(optimal)}")
    if optimal:
        print(f"Лучший вариант: {optimal[0]} с доходом {max_yield:.2f}")

    reduction = len(rec_comps) - len(valid)
    print(f"\nКоличество сокращенных переборов: {reduction}")
