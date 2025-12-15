import tkinter as tk
from tkinter import messagebox
import random
from collections import deque


class SpiderMazeAdventure:

    def __init__(self, window, grid_width=21, grid_height=15, tile_size=30, countdown=10):
        self.window = window
        self.window.title("Приключения паука (BFS)")
        self.grid_width = grid_width if grid_width % 2 == 1 else grid_width + 1
        self.grid_height = grid_height if grid_height % 2 == 1 else grid_height + 1
        self.tile_size = tile_size
        self.countdown_limit = countdown
        self.display = tk.Canvas(
            window,
            width=self.grid_width * self.tile_size,
            height=self.grid_height * self.tile_size,
            bg="#e0e0e0"
        )

        self.display.pack(pady=10)
        controls = tk.Frame(window)
        controls.pack()

        tk.Button(
            controls,
            text="Перезапуск",
            command=self.init_game,
            bg="#E2AC36",
            fg="white"
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            controls,
            text="Старт",
            command=self.begin_pathfinding,
            bg="#3FA73B",
            fg="white"
        ).pack(side=tk.LEFT, padx=5)

        self.countdown_display = tk.Label(
            window,
            text="Осталось: -- сек",
            font=("Helvetica", 14, "bold")
        )

        self.countdown_display.pack()
        self.init_game()

    def init_game(self):
        if hasattr(self, 'in_progress') and self.in_progress:
            return

        self.finished = False
        self.in_progress = False
        self.time_left = self.countdown_limit
        self.countdown_display.config(text="Осталось: -- сек")
        self.build_maze()
        self.render_maze()
        self.render_spider()
        self.display.delete("path_trace")

    def build_maze(self):
        self.grid = [[True] * self.grid_width for _ in range(self.grid_height)]

        def dfs(x, y):
            self.grid[y][x] = False
            moves = [(0, -2), (0, 2), (-2, 0), (2, 0)]
            random.shuffle(moves)
            for dx, dy in moves:
                nx, ny = x + dx, y + dy
                if 0 < nx < self.grid_width - 1 and 0 < ny < self.grid_height - 1:
                    if self.grid[ny][nx]:
                        self.grid[y + dy // 2][x + dx // 2] = False
                        dfs(nx, ny)
        dfs(1, 1)

        open_tiles = [
            (x, y)
            for y in range(1, self.grid_height - 1)
            for x in range(1, self.grid_width - 1)
            if not self.grid[y][x]
        ]

        self.finish_points = random.sample(open_tiles, 3)

        self.spider_location = random.choice(
            [tile for tile in open_tiles if tile not in self.finish_points]
        )

    def render_maze(self):
        self.display.delete("all")

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

        for fx, fy in self.finish_points:
            cx = fx * self.tile_size + self.tile_size // 2
            cy = fy * self.tile_size + self.tile_size // 2
            self.display.create_oval(cx - 10, cy - 10, cx + 10, cy + 10, fill="yellow")
            self.display.create_text(cx, cy, text="Выход")

    def render_spider(self):
        if hasattr(self, "_spider"):
            self.display.delete(self._spider)
        x, y = self.spider_location

        cx = x * self.tile_size + self.tile_size // 2
        cy = y * self.tile_size + self.tile_size // 2
        r = self.tile_size * 0.3
        self._spider = self.display.create_oval(
            cx - r, cy - r, cx + r, cy + r,
            fill="#4CAF50",
            outline="black",
            width=2
        )

    def update_timer(self):
        if not self.finished:
            self.time_left -= 1
            self.countdown_display.config(
                text=f"Осталось: {self.time_left:02d} сек"
            )
            if self.time_left <= 0:
                self.conclude_game(False)
        if not self.finished:
            self.window.after(1000, self.update_timer)

    def conclude_game(self, success):
        self.finished = True
        self.in_progress = False
        messagebox.showinfo(
            "Результат",
            "Паук выбрался!" if success else "Паук застрял :("
        )

    def begin_pathfinding(self):
        if self.in_progress or self.finished:
            return
        self.in_progress = True
        self.update_timer()
        queue = deque([self.spider_location])
        visited = {self.spider_location}
        parent = {}
        target = None
        while queue:
            current = queue.popleft()
            if current in self.finish_points:
                target = current
                break
            for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                nx, ny = current[0] + dx, current[1] + dy
                if (0 <= nx < self.grid_width and
                    0 <= ny < self.grid_height and
                    not self.grid[ny][nx] and
                    (nx, ny) not in visited):
                    visited.add((nx, ny))
                    parent[(nx, ny)] = current
                    queue.append((nx, ny))

        if target is None:
            self.conclude_game(False)
            return

        self.path = []
        cur = target
        while cur != self.spider_location:
            self.path.append(cur)
            cur = parent[cur]
        self.path.append(self.spider_location)
        self.path.reverse()
        self.step_index = 0
        self.animate_path()

    def animate_path(self):
        if self.finished:
            return
        if self.step_index >= len(self.path):
            self.conclude_game(True)
            return
        self.spider_location = self.path[self.step_index]
        self.render_spider()

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

        self.step_index += 1
        self.window.after(150, self.animate_path)


if __name__ == "__main__":
    root = tk.Tk()
    game = SpiderMazeAdventure(root)
    root.mainloop()
