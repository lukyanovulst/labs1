import tkinter as tk
import random

SIZE = 10
COLORS = {
    "bg": "#1a1a2e", "frame": "#16213e", "btn": "#ffffff",
    "ship": "#0f4c75", "hit": "#e94560", "miss": "#8d99ae",
    "sunk": "#2d4059", "text": "#eeeeee", "accent": "#00adb5"
}


class Board:
    def __init__(self):
        self.ships, self.shots = self.place_ships(), set()

    def place_ships(self):
        cells, ships = set(), []
        for size in [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]:
            for _ in range(100):
                h = random.choice([True, False])
                x = random.randint(0, SIZE - (size if h else 1))
                y = random.randint(0, SIZE - (size if not h else 1))
                ship_cells = {(x + (i if h else 0), y + (i if not h else 0)) for i in range(size)}
                if not any(
                        (cx + dx, cy + dy) in cells for cx, cy in ship_cells for dx in (-1, 0, 1) for dy in (-1, 0, 1)):
                    ships.append(ship_cells);
                    cells |= ship_cells;
                    break
            else:
                ships.append(ship_cells); cells |= ship_cells
        return ships

    def shoot(self, pos):
        if pos in self.shots: return None
        self.shots.add(pos)
        for ship in self.ships:
            if pos in ship: return "sunk" if ship <= self.shots else "hit"
        return "miss"

    def all_sunk(self):
        return all(ship <= self.shots for ship in self.ships)


class AI:
    def __init__(self):
        self.board, self.targets, self.used = Board(), [], set()

    def shoot(self):
        if self.targets: return self.targets.pop()
        available = [(x, y) for x in range(SIZE) for y in range(SIZE) if (x, y) not in self.used]
        return random.choice(available) if available else (0, 0)

    def feedback(self, pos, res):
        self.used.add(pos)
        if res == "hit":
            x, y = pos
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < SIZE and 0 <= ny < SIZE and (nx, ny) not in self.used:
                    self.targets.append((nx, ny))
        elif res == "sunk":
            self.targets.clear()


class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Морской бой")
        self.root.configure(bg=COLORS["bg"])
        self.player = Board()
        self.ai = AI()
        self.game_over = False
        self.setup_ui()

    def setup_ui(self):
        main = tk.Frame(self.root, bg=COLORS["frame"], padx=15, pady=15)
        main.pack(padx=10, pady=10)

        tk.Label(main, text="⚓ МОРСКОЙ БОЙ", font=("Arial", 16, "bold"),
                 bg=COLORS["frame"], fg=COLORS["accent"]).grid(row=0, column=0, columnspan=22, pady=10)

        self.status = tk.Label(main, text="Ваш ход!", font=("Arial", 11),
                               bg=COLORS["frame"], fg=COLORS["text"])
        self.status.grid(row=1, column=0, columnspan=22, pady=5)


        tk.Label(main, text="Мой флот", font=("Arial", 10, "bold"),
                 bg=COLORS["frame"], fg=COLORS["text"]).grid(row=2, column=0, columnspan=10)
        tk.Label(main, text="Флот противника", font=("Arial", 10, "bold"),
                 bg=COLORS["frame"], fg=COLORS["text"]).grid(row=2, column=12, columnspan=10)


        sep = tk.Frame(main, bg=COLORS["accent"], width=2, height=220)
        sep.grid(row=3, column=11, rowspan=SIZE, sticky="ns", padx=10)

        self.p_btns, self.e_btns = [], []
        for y in range(SIZE):
            row_p, row_e = [], []
            for x in range(SIZE):
                b_p = tk.Button(main, width=2, height=1, bg=COLORS["btn"],
                                font=("Arial", 8), relief=tk.RAISED, bd=1, state="disabled")
                b_p.grid(row=y + 3, column=x, padx=1, pady=1)
                row_p.append(b_p)

                b_e = tk.Button(main, width=2, height=1, bg=COLORS["btn"],
                                font=("Arial", 8), relief=tk.RAISED, bd=1,
                                command=lambda x=x, y=y: self.shot(x, y))
                b_e.grid(row=y + 3, column=x + 12, padx=1, pady=1)
                row_e.append(b_e)
            self.p_btns.append(row_p)
            self.e_btns.append(row_e)

        tk.Button(main, text="🔄 Новая игра", font=("Arial", 10),
                  bg=COLORS["accent"], fg="white", relief=tk.RAISED, bd=2,
                  padx=15, pady=5, command=self.restart
                  ).grid(row=SIZE + 4, column=0, columnspan=22, pady=10)

        legend_frame = tk.Frame(main, bg=COLORS["frame"])
        legend_frame.grid(row=SIZE + 3, column=0, columnspan=22, pady=5)

        for i, (text, color) in enumerate([("Корабль", COLORS["ship"]),
                                           ("Попадание", COLORS["hit"]),
                                           ("Промах", COLORS["miss"])]):
            tk.Label(legend_frame, text="■", fg=color, bg=COLORS["frame"],
                     font=("Arial", 12)).grid(row=0, column=i * 2, padx=2)
            tk.Label(legend_frame, text=text, fg=COLORS["text"], bg=COLORS["frame"],
                     font=("Arial", 8)).grid(row=0, column=i * 2 + 1, padx=5)

        self.update()

    def update(self):
        for y in range(SIZE):
            for x in range(SIZE):
                p, e = self.p_btns[y][x], self.e_btns[y][x]
                pos = (x, y)

                if pos in self.player.shots:
                    p.config(bg=COLORS["hit"] if any(pos in s for s in self.player.ships) else COLORS["miss"])
                elif any(pos in s for s in self.player.ships):
                    p.config(bg=COLORS["ship"])


                if pos in self.ai.board.shots:
                    e.config(bg=COLORS["hit"] if any(pos in s for s in self.ai.board.ships) else COLORS["miss"],
                             state="disabled")
                elif not self.game_over:
                    e.config(bg=COLORS["btn"], state="normal")
                else:
                    e.config(state="disabled")

    def shot(self, x, y):
        if self.ai.board.shoot((x, y)) is None: return

        ai_pos = self.ai.shoot()
        self.player.shoot(ai_pos)
        self.ai.feedback(ai_pos, "hit" if any(ai_pos in s for s in self.player.ships) else "miss")

        self.update()

        if self.ai.board.all_sunk():
            self.status.config(text="🎉 ПОБЕДА!", fg="#4CAF50")
            self.game_over = True
            self.show_all_ships()
        elif self.player.all_sunk():
            self.status.config(text="💀 ПОРАЖЕНИЕ", fg="#F44336")
            self.game_over = True
            self.show_all_ships()

    def show_all_ships(self):
        for y in range(SIZE):
            for x in range(SIZE):
                if any((x, y) in s for s in self.ai.board.ships) and (x, y) not in self.ai.board.shots:
                    self.e_btns[y][x].config(bg=COLORS["ship"])

    def restart(self):
        self.player = Board()
        self.ai = AI()
        self.game_over = False
        self.status.config(text="Ваш ход!", fg=COLORS["text"])

        for y in range(SIZE):
            for x in range(SIZE):
                self.p_btns[y][x].config(bg=COLORS["btn"])
                self.e_btns[y][x].config(bg=COLORS["btn"], state="normal")

        self.update()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("700x500")
    Game(root)
    root.mainloop()