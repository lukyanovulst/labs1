import tkinter as tk
from tkinter import messagebox
import random

class MazeGame:
    def __init__(self, root, cols=21, rows=15, cell_size=30, time_limit_sec=40):
        self.root = root
        self.root.title("Паук в лабиринте")
        self.cols = cols if cols % 2 == 1 else cols + 1
        self.rows = rows if rows % 2 == 1 else rows + 1
        self.cell_size = cell_size
        self.time_limit = time_limit_sec

        self.canvas = tk.Canvas(root, width=self.cols * self.cell_size,
                                height=self.rows * self.cell_size, bg="#f8f9fa")
        self.canvas.pack(pady=10)

        btn_frame = tk.Frame(root)
        btn_frame.pack()
        tk.Button(btn_frame, text="Новая игра", command=self.reset_game).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Запустить", command=self.start_dfs).pack(side=tk.LEFT, padx=5)

        self.timer_label = tk.Label(root, text="Время: -- с", font=("Arial", 12))
        self.timer_label.pack()

        self.reset_game()

    def reset_game(self): #сброс игры
        if hasattr(self, 'moving') and self.moving:
            return
        self.game_over = False
        self.moving = False
        self.remaining = self.time_limit
        self.timer_label.config(text="Время: -- с")
        self.generate_maze()
        self.draw_maze()
        self.draw_player()
        self.canvas.delete("trail")

    def generate_maze(self): #создает лабиринт
        self.maze = [[True for _ in range(self.cols)] for _ in range(self.rows)]

        def dfs(x, y):
            self.maze[y][x] = False
            directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]
            random.shuffle(directions)
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 < nx < self.cols - 1 and 0 < ny < self.rows - 1 and self.maze[ny][nx]:
                    self.maze[y + dy // 2][x + dx // 2] = False
                    dfs(nx, ny)

        dfs(1, 1)

        # собираем все проходы и выбираем случайный старт и выход
        passages = []
        for y in range(1, self.rows - 1):
            for x in range(1, self.cols - 1):
                if not self.maze[y][x]:
                    passages.append((x, y))

        if len(passages) >= 2:
            self.exit_pos = random.choice(passages) #рандомный выход
            start_candidates = [p for p in passages if p != self.exit_pos]
            self.player_pos = random.choice(start_candidates) #рандомный старт
        else:
            self.player_pos = (1, 1)
            self.exit_pos = (self.cols - 2, self.rows - 2)

    def draw_maze(self): #рисует лабиринт
        self.canvas.delete("all")
        for y in range(self.rows):
            for x in range(self.cols):
                cx, cy = x * self.cell_size, y * self.cell_size
                if self.maze[y][x]:
                    self.canvas.create_rectangle(
                        cx, cy, cx + self.cell_size, cy + self.cell_size,
                        fill="black", outline=""
                    )
        ex, ey = self.exit_pos
        cx = ex * self.cell_size + self.cell_size // 2
        cy = ey * self.cell_size + self.cell_size // 2
        self.canvas.create_text(cx, cy, text="Выход", fill="red", font=("Arial", 12, "bold"))

    def draw_player(self): #рисует паучка
        if hasattr(self, '_player_id'):
            self.canvas.delete(self._player_id)
        x, y = self.player_pos
        cx = x * self.cell_size + self.cell_size // 2
        cy = y * self.cell_size + self.cell_size // 2
        r = self.cell_size * 0.35
        self._player_id = self.canvas.create_oval(
            cx - r, cy - r, cx + r, cy + r,
            fill="black", outline="white", width=1
        )

    def tick_timer(self): #таймер
        if not self.game_over:
            self.remaining = max(0, self.remaining - 1)
            self.timer_label.config(text=f"Время: {self.remaining:02d} с")
            if self.remaining == 0:
                self.end_game(win=False)
        if not self.game_over:
            self.root.after(1000, self.tick_timer)

    def end_game(self, win): #завершение игры
        self.game_over = True
        self.moving = False
        msg = "Ура, паучок выбрался!" if win else "Паучок проиграл(("
        messagebox.showinfo("Победа!" if win else "Проигрыш", msg)

    def start_dfs(self): #запуск движения
        if self.moving or self.game_over:
            return
        self.moving = True
        self.tick_timer()
        self.stack = [self.player_pos]
        self.visited = {self.player_pos}
        self.dfs_step()

    def dfs_step(self): #движение
        if self.game_over or not self.moving:
            return
        if not self.stack:
            return

        current = self.stack[-1]
        self.player_pos = current
        self.draw_player()

        x, y = current
        cx = x * self.cell_size + self.cell_size // 2
        cy = y * self.cell_size + self.cell_size // 2
        r = self.cell_size * 0.12
        self.canvas.create_oval(
            cx - r, cy - r, cx + r, cy + r,
            fill="black", outline="", tags="trail"
        )

        if current == self.exit_pos:
            self.end_game(win=True)
            return

        neighbors = []
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.cols and 0 <= ny < self.rows:
                if not self.maze[ny][nx] and (nx, ny) not in self.visited:
                    neighbors.append((nx, ny))

        if neighbors:
            next_cell = random.choice(neighbors)
            self.visited.add(next_cell)
            self.stack.append(next_cell)
        else:
            self.stack.pop()

        self.root.after(200, self.dfs_step)

if __name__ == "__main__":
    root = tk.Tk()
    game = MazeGame(root, cols=21, rows=15, cell_size=30, time_limit_sec=40)
    root.mainloop()