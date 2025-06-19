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

    # часть 5.1: сравнение методов
    t1 = timeit.timeit(lambda: generate_compositions_recursive(S, K), number=1)
    rec_comps = generate_compositions_recursive(S, K)
    print("\nАлгоритмический метод:")
    print(f"Всего комбинаций: {len(rec_comps)}")
    print("Первые 5 комбинаций (каждая в новой строке):")
    for comb in rec_comps[:5]: print(comb)
    print(f"Время выполнения: {t1:.6f} сек")

    t2 = timeit.timeit(lambda: generate_compositions_product(S, K), number=1)
    prod_comps = generate_compositions_product(S, K)
    print("\nPython-функции метод:")
    print(f"Всего комбинаций: {len(prod_comps)}")
    print("Первые 5 комбинаций (каждая в новой строке):")
    for comb in prod_comps[:5]: print(comb)
    print(f"Время выполнения: {t2:.6f} сек")

    faster = "алгоритмический" if t1 < t2 else "Python-функции"
    print(f"\nБолее быстрый метод: {faster}")

    # характеристики банков
    capacities = []
    while True:
        capacities = [random.randint(0, S) for _ in range(K)]
        if sum(capacities) >= S:
            break
    rates = [round(random.uniform(0.01, 0.1), 3) for _ in range(K)]
    print("\nХарактеристики банков:")
    print(f"Максимальные суммы (capacities): {capacities}")
    print(f"Доходности (rates): {rates}")

    # часть 5.2: генерация допустимых композиций с нуля по условию
    if faster == 'алгоритмический':
        valid = generate_compositions_recursive(S, K)
        # отсекаем лишнее сразу при генерации 
        def valid_recur_with_caps():
            result = []
            def helper(prefix, remaining, idx):
                if idx == K - 1:
                    if remaining <= capacities[idx]:
                        result.append(prefix + [remaining])
                else:
                    max_val = capacities[idx]
                    for i in range(min(remaining, max_val) + 1):
                        helper(prefix + [i], remaining - i, idx + 1)
            helper([], S, 0)
            return result
        valid = valid_recur_with_caps()
    else:
        valid = [comb for comb in itertools.product(*(range(min(cap, S) + 1) for cap in capacities)) if sum(comb) == S]

    print(f"\nПосле ограничения переборов: {len(valid)}")
    print("Первые 5 допустимых вариантов:")
    for comb in valid[:5]: print(comb)

    # поиск оптимального
    yields = [sum(comb[i] * rates[i] for i in range(K)) for comb in valid]
    max_yield = max(yields) if yields else 0
    optimal = [valid[i] for i,y in enumerate(yields) if y==max_yield]
    print(f"\nОптимальных вариантов: {len(optimal)}")
    if optimal:
        print(f"Лучший вариант: {optimal[0]} с доходом {max_yield:.2f}")
