import itertools
import random
import tkinter as tk
from tkinter import scrolledtext

# Функция генерации композиций (рекурсивно)
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

# Обработчик кнопки "Запустить"
def run_allocation():
    try:
        S = int(entry_sum.get())
        K = int(entry_banks.get())
        if S < 0 or K <= 0:
            raise ValueError
    except ValueError:
        text_output.delete(1.0, tk.END)
        text_output.insert(tk.END, "Ошибка: введите корректные числовые значения (S >= 0, K > 0).\n")
        return

    # Генерация всех композиций
    rec_comps = generate_compositions_recursive(S, K)

    # Генерация capacities так, чтобы суммарная >= S
    while True:
        capacities = [random.randint(0, S) for _ in range(K)]
        if sum(capacities) >= S:
            break
    # Доходности
    rates = [round(random.uniform(0.01, 0.1), 3) for _ in range(K)]

    # Фильтрация по capacities
    valid = [comb for comb in rec_comps if all(comb[i] <= capacities[i] for i in range(K))]

    # Вычисление доходов и поиск оптимальных
    yields = [sum(comb[i] * rates[i] for i in range(K)) for comb in valid]
    max_yield = max(yields) if yields else 0
    optimal = [valid[i] for i, y in enumerate(yields) if y == max_yield]

    # Вывод результатов
    text_output.delete(1.0, tk.END)
    text_output.insert(tk.END, f"Сумма S = {S}, Банков K = {K}\n")
    text_output.insert(tk.END, f"Всего вариантов (алгоритм): {len(rec_comps)}\n")
    text_output.insert(tk.END, f"Максимальные суммы (capacities): {capacities}\n")
    text_output.insert(tk.END, f"Доходности (rates): {rates}\n\n")
    text_output.insert(tk.END, f"Вариантов после ограничения: {len(valid)}\nПервые 5:\n")
    for comb in valid[:5]:
        text_output.insert(tk.END, f"{comb}\n")
    text_output.insert(tk.END, f"\nОптимальных вариантов: {len(optimal)}\n")
    if optimal:
        text_output.insert(tk.END, f"Лучший вариант: {optimal[0]} с доходом {max_yield:.2f}\n")

# Создание GUI
root = tk.Tk()
root.title("Распределение средств по банкам")

frame_input = tk.Frame(root)
frame_input.pack(padx=10, pady=5)

# Поле ввода суммы S
tk.Label(frame_input, text="Сумма S:").grid(row=0, column=0, sticky="e")
entry_sum = tk.Entry(frame_input, width=10)
entry_sum.grid(row=0, column=1, padx=5)

# Поле ввода числа банков K
tk.Label(frame_input, text="Количество банков K:").grid(row=1, column=0, sticky="e")
entry_banks = tk.Entry(frame_input, width=10)
entry_banks.grid(row=1, column=1, padx=5)

# Кнопка запуска
btn_run = tk.Button(root, text="Рассчитать", command=run_allocation)
btn_run.pack(pady=5)

# Окно вывода с прокруткой
text_output = scrolledtext.ScrolledText(root, width=60, height=20)
text_output.pack(padx=10, pady=5)

root.mainloop()
