# Подключаем библиотеку tkinter для создания графического интерфейса
import tkinter as tk

# Импортируем окно сообщений (для победы / поражения)
from tkinter import messagebox

# Модуль random нужен для случайных выборов (лабиринт, старт, выходы)
import random

# deque — эффективная очередь (нужна для BFS)
from collections import deque


# Основной класс игры
class SpiderMazeAdventure:

    # Конструктор класса (вызывается при создании объекта)
    def __init__(self, window, grid_width=21, grid_height=15, tile_size=30, countdown=10):
        # Сохраняем главное окно
        self.window = window

        # Устанавливаем заголовок окна
        self.window.title("Приключения паука (BFS)")

        # Делаем ширину лабиринта нечётной
        self.grid_width = grid_width if grid_width % 2 == 1 else grid_width + 1

        # Делаем высоту лабиринта нечётной
        self.grid_height = grid_height if grid_height % 2 == 1 else grid_height + 1

        # Размер одной клетки в пикселях
        self.tile_size = tile_size

        # Ограничение времени на прохождение
        self.countdown_limit = countdown

        # Создаём холст для рисования лабиринта
        self.display = tk.Canvas(
            window,
            width=self.grid_width * self.tile_size,   # ширина холста
            height=self.grid_height * self.tile_size, # высота холста
            bg="#e0e0e0"                              # цвет фона
        )

        # Размещаем холст в окне
        self.display.pack(pady=10)

        # Панель управления
        controls = tk.Frame(window)
        controls.pack()

        # Кнопка перезапуска игры
        tk.Button(
            controls,
            text="Перезапуск",
            command=self.init_game,
            bg="#E2AC36",
            fg="white"
        ).pack(side=tk.LEFT, padx=5)

        # Кнопка старта поиска пути
        tk.Button(
            controls,
            text="Старт",
            command=self.begin_pathfinding,
            bg="#3FA73B",
            fg="white"
        ).pack(side=tk.LEFT, padx=5)

        # Надпись с таймером
        self.countdown_display = tk.Label(
            window,
            text="Осталось: -- сек",
            font=("Helvetica", 14, "bold")
        )

        # Размещаем таймер
        self.countdown_display.pack()

        # Запускаем первую инициализацию игры
        self.init_game()

    # -------------------------------------------------
    # Полный сброс и запуск новой игры
    # -------------------------------------------------
    def init_game(self):
        # Если паук уже движется — не даём перезапустить
        if hasattr(self, 'in_progress') and self.in_progress:
            return

        # Игра не завершена
        self.finished = False

        # Поиск пути ещё не идёт
        self.in_progress = False

        # Восстанавливаем таймер
        self.time_left = self.countdown_limit

        # Обновляем текст таймера
        self.countdown_display.config(text="Осталось: -- сек")

        # Генерируем новый лабиринт
        self.build_maze()

        # Рисуем лабиринт
        self.render_maze()

        # Рисуем паука
        self.render_spider()

        # Удаляем старый путь
        self.display.delete("path_trace")

    # -------------------------------------------------
    # Генерация лабиринта
    # -------------------------------------------------
    def build_maze(self):
        # True — стена, False — проход
        self.grid = [[True] * self.grid_width for _ in range(self.grid_height)]

        # Внутренняя функция DFS для генерации лабиринта
        def dfs(x, y):
            # Текущая клетка становится проходом
            self.grid[y][x] = False

            # Возможные направления (шаг через одну клетку)
            moves = [(0, -2), (0, 2), (-2, 0), (2, 0)]

            # Перемешиваем направления
            random.shuffle(moves)

            # Проходим по направлениям
            for dx, dy in moves:
                nx, ny = x + dx, y + dy


                # Проверяем границы и посещённость
                if 0 < nx < self.grid_width - 1 and 0 < ny < self.grid_height - 1:
                    if self.grid[ny][nx]:
                        # Убираем стену между клетками
                        self.grid[y + dy // 2][x + dx // 2] = False
                        # Рекурсивно продолжаем
                        dfs(nx, ny)

        # Начинаем генерацию с точки (1,1)
        dfs(1, 1)

        # Список всех свободных клеток
        open_tiles = [
            (x, y)
            for y in range(1, self.grid_height - 1)
            for x in range(1, self.grid_width - 1)
            if not self.grid[y][x]
        ]

        # Случайно выбираем 3 выхода
        self.finish_points = random.sample(open_tiles, 3)

        # Стартовая позиция паука (не выход)
        self.spider_location = random.choice(
            [tile for tile in open_tiles if tile not in self.finish_points]
        )

    # -------------------------------------------------
    # Отрисовка лабиринта и выходов
    # -------------------------------------------------
    def render_maze(self):
        # Очищаем холст
        self.display.delete("all")

        # Рисуем стены
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                if self.grid[y][x]:
                    self.display.create_rectangle(
                        x * self.tile_size,
                        y * self.tile_size,
                        (x + 1) * self.tile_size,
                        (y + 1) * self.tile_size,
                        fill="#3F51B5",
                        outline="#303F9F"
                    )

        # Рисуем все выходы
        for fx, fy in self.finish_points:
            cx = fx * self.tile_size + self.tile_size // 2
            cy = fy * self.tile_size + self.tile_size // 2
            self.display.create_oval(cx - 10, cy - 10, cx + 10, cy + 10, fill="yellow")
            self.display.create_text(cx, cy, text="Выход")

    # -------------------------------------------------
    # Отрисовка паука
    # -------------------------------------------------
    def render_spider(self):
        # Если паук уже был — удаляем
        if hasattr(self, "_spider"):
            self.display.delete(self._spider)

        # Текущая позиция паука
        x, y = self.spider_location

        # Центр клетки
        cx = x * self.tile_size + self.tile_size // 2
        cy = y * self.tile_size + self.tile_size // 2

        # Радиус паука
        r = self.tile_size * 0.3

        # Рисуем паука
        self._spider = self.display.create_oval(
            cx - r, cy - r, cx + r, cy + r,
            fill="#4CAF50",
            outline="black",
            width=2
        )

    # -------------------------------------------------
    # Таймер
    # -------------------------------------------------
    def update_timer(self):
        # Если игра не завершена
        if not self.finished:
            # Уменьшаем время
            self.time_left -= 1

            # Обновляем текст таймера
            self.countdown_display.config(
                text=f"Осталось: {self.time_left:02d} сек"
            )

            # Если время вышло — проигрыш
            if self.time_left <= 0:
                self.conclude_game(False)

        # Запускаем таймер снова через 1 секунду
        if not self.finished:
            self.window.after(1000, self.update_timer)

    # -------------------------------------------------
    # Завершение игры
    # -------------------------------------------------
    def conclude_game(self, success):
        # Помечаем игру завершённой
        self.finished = True

        # Останавливаем движение
        self.in_progress = False

        # Показываем результат
        messagebox.showinfo(
            "Результат",
            "Паук выбрался!" if success else "Паук застрял :("
        )


    # -------------------------------------------------
    # BFS — поиск пути с помощью очереди
    # -------------------------------------------------
    def begin_pathfinding(self):
        # Защита от повторного запуска
        if self.in_progress or self.finished:
            return

        # Поиск запущен
        self.in_progress = True

        # Запускаем таймер
        self.update_timer()

        # Очередь BFS
        queue = deque([self.spider_location])

        # Множество посещённых клеток
        visited = {self.spider_location}

        # Словарь для восстановления пути
        parent = {}

        # Найденный выход
        target = None

        # Пока очередь не пуста
        while queue:
            # Берём первый элемент
            current = queue.popleft()

            # Если дошли до выхода
            if current in self.finish_points:
                target = current
                break

            # Проверяем соседей
            for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                nx, ny = current[0] + dx, current[1] + dy

                # Проверка допустимости хода
                if (0 <= nx < self.grid_width and
                    0 <= ny < self.grid_height and
                    not self.grid[ny][nx] and
                    (nx, ny) not in visited):
                    visited.add((nx, ny))
                    parent[(nx, ny)] = current
                    queue.append((nx, ny))

        # Если путь не найден
        if target is None:
            self.conclude_game(False)
            return

        # Восстанавливаем путь
        self.path = []
        cur = target
        while cur != self.spider_location:
            self.path.append(cur)
            cur = parent[cur]
        self.path.append(self.spider_location)
        self.path.reverse()

        # Индекс шага
        self.step_index = 0

        # Запускаем анимацию
        self.animate_path()

    # -------------------------------------------------
    # Анимация движения паука
    # -------------------------------------------------
    def animate_path(self):
        # Если игра завершена — выходим
        if self.finished:
            return

        # Если путь пройден — победа
        if self.step_index >= len(self.path):
            self.conclude_game(True)
            return

        # Перемещаем паука
        self.spider_location = self.path[self.step_index]
        self.render_spider()

        # Рисуем линию пути
        if self.step_index > 0:
            x1, y1 = self.path[self.step_index - 1]
            x2, y2 = self.path[self.step_index]
            self.display.create_line(
                x1 * self.tile_size + self.tile_size // 2,
                y1 * self.tile_size + self.tile_size // 2,
                x2 * self.tile_size + self.tile_size // 2,
                y2 * self.tile_size + self.tile_size // 2,
                fill="red",
                width=2,
                tags="path_trace"
            )

        # Переходим к следующему шагу
        self.step_index += 1

        # Задержка между шагами
        self.window.after(150, self.animate_path)


# -------------------------------------------------
# Запуск программы
# -------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()                 # Создаём окно
    game = SpiderMazeAdventure(root)  # Создаём игру
    root.mainloop()                # Запускаем главный цикл
