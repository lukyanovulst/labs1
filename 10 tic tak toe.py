import tkinter as tk
from tkinter import messagebox
import random, math


def best_move(board, ai, human):
    best_score = -math.inf
    move = None
    for i in range(9):
        if board[i] == " ":
            board[i] = ai
            score = minimax(board, 0, False, ai, human)
            board[i] = " "
            if score > best_score:
                best_score = score
                move = i
    return move

def minimax(board, depth, ismax, ai, human):
    winner = check_winner(board)
    if winner == ai:
        return 10-depth
    if winner == human:
        return depth-10
    if " " not in board:
        return 0
    if ismax:
        best = -math.inf
        for i in range(9):
            if board[i] == " ":
                board[i] = ai
                value = minimax(board, depth+1, False, ai, human)
                board[i] = " "
                best = max(best, value)
        return best
    else:
        best = math.inf
        for i in range(9):
            if board[i] == " ":
                board[i] = human
                value = minimax(board, depth+1, True, ai, human)
                board[i] = " "
                best = min(best, value)
        return best

def check_winner(board):
    wins = [
        (0,1,2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6)
    ]
    for a,b,c in wins:
        if board[a] == board[b] == board[c] != " ":
            return board[a]
    return None


class tictak:
    def __init__(self, root):
        self.root = root
        self.root.title("Крестики-нолики")

        self.mod = None
        self.create_menu()

    def create_menu(self):
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack(pady = 20)
        tk.Label(self.menu_frame, text = ("Нажмите на режим игры"), font = ("Arial", 18)).pack(pady = 10)
        tk.Button(self.menu_frame, text = "ИИ", font = ("Arial", 14), command = lambda: self.start_game("Ai")).pack(fill = "x", pady = 5)

    def start_game(self, mod):
        self.mod = mod
        self.current_player = "x"
        self.human = "x"
        self.ai = "0"

        self.board = [" "] * 9


        self.menu_frame.destroy()

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.buttons = []
        for i in range(9):
            btn = tk.Button(self.frame, text = "", font = ("Arial", 24), width = 5, height = 2, command = lambda p = i: self.on_click(p))
            btn.grid(row = i//3, column = i%3)
            self.buttons.append(btn)

        tk.Button(self.root, text = "Перезапустить игру", font = ("Arial", 14), command = self.restart).pack(pady = 10)

    def ai_move(self):
        if self.mod != "Ai":
            return

        move = best_move(self.board[:], self.ai, self.human)

        if move is None:
            move = random.choice([i for i in range(9) if self.board[i] == " "])


        self.make_move(move, self.ai)

        if self.check_game_end():
            return

        self.switch_turn()

    def on_click(self, position):
        if self.board[position] != " ":
            return
        self.make_move(position, self.human)
        if self.check_game_end():
            return
        self.switch_turn()
        self.ai_move()

    def make_move(self, position, player):
        self.board[position] = player
        self.buttons[position].config(text = player, state = "disabled")

    def check_game_end(self):
        winner = check_winner(self.board)
        if winner:
            messagebox.showinfo("Конец игры", f"победил {winner}")
            self.disabled_all()
            return True

        if " " not in self.board:
            messagebox.showinfo("Конец игры", f"ничья")
            self.disabled_all()
            return True

        return False

    def disabled_all(self):
        for btn in self.buttons:
            btn.config(state= "disabled")

    def switch_turn(self):

        if self.current_player == "x":
            self.current_player = "0"
        else:
            self.current_player = "x"

    def restart(self):
        self.frame.destroy()
        for wit in self.root.pack_slaves():
            wit.destroy()

        self.create_menu()

root = tk.Tk()
app = tictak(root)
root.mainloop()

