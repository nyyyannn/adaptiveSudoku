import tkinter as tk
from tkinter import messagebox
import time
import random
import copy
from generator.board_generator import generate_full_board
from generator.puzzle_maker import remove_cells, print_board

# -----------------------------
# 🧠 Difficulty Settings
DIFFICULTY_HINTS = {
    'easy': float('inf'),
    'medium': 10,
    'hard': 5
}
current_difficulty = 'easy'

# -----------------------------
# 🧩 Game State
game_state = {
    'start_time': None,
    'mistakes': 0,
    'hints_used': 0,
    'cells_filled': 0,
    'solved_successfully': 0,
    'user_metrics': {},
    'solution_board': [],
    'original_puzzle': []
}

# -----------------------------
# 🎯 Hint logic
def find_empty_and_solution(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j, game_state['solution_board'][i][j]
    return None, None, None

# -----------------------------
# 🎲 UI Setup
root = tk.Tk()
root.title("Adaptive Sudoku 🧠")
entries = [[None for _ in range(9)] for _ in range(9)]

def start_new_game():
    board = generate_full_board()
    solution = copy.deepcopy(board)
    user_metrics = {
        'time_taken': 0,
        'mistakes_made': 0,
        'hints_used': 0,
        'cells_filled_by_user': 0,
        'solved_successfully': 0
    }

    puzzle = remove_cells(board, user_metrics)

    game_state['solution_board'] = solution
    game_state['original_puzzle'] = puzzle
    game_state['start_time'] = time.time()
    game_state['mistakes'] = 0
    game_state['hints_used'] = 0
    game_state['cells_filled'] = 0

    for i in range(9):
        for j in range(9):
            if entries[i][j] is not None:
                entries[i][j].destroy()

            entry = tk.Entry(root, width=3, font=('Arial', 18), justify='center')
            entry.grid(row=i, column=j, padx=2, pady=2)
            entries[i][j] = entry

            val = puzzle[i][j]
            if val != 0:
                entry.insert(0, str(val))
                entry.config(state='disabled', disabledforeground='black')

def submit():
    user_board = []
    for i in range(9):
        row = []
        for j in range(9):
            val = entries[i][j].get()
            if val == '':
                row.append(0)
            else:
                row.append(int(val))
        user_board.append(row)

    # Check correctness
    correct = True
    filled = 0
    for i in range(9):
        for j in range(9):
            if game_state['original_puzzle'][i][j] == 0:
                user_val = user_board[i][j]
                solution_val = game_state['solution_board'][i][j]
                if user_val != solution_val:
                    correct = False
                    game_state['mistakes'] += 1
                if user_val != 0:
                    filled += 1

    game_state['cells_filled'] = filled
    game_state['solved_successfully'] = 1 if correct else 0
    game_state['user_metrics'] = {
        'time_taken': int(time.time() - game_state['start_time']),
        'mistakes_made': game_state['mistakes'],
        'hints_used': game_state['hints_used'],
        'cells_filled_by_user': filled,
        'solved_successfully': game_state['solved_successfully']
    }

    print("\n📊 Final Game Stats:")
    for k, v in game_state['user_metrics'].items():
        print(f"{k}: {v}")

    if correct:
        messagebox.showinfo("🎉 Success", "Congratulations! You solved the puzzle!")
    else:
        messagebox.showerror("❌ Incorrect", "There are mistakes in the puzzle.")

def give_hint():
    if game_state['hints_used'] >= DIFFICULTY_HINTS[current_difficulty]:
        messagebox.showwarning("⚠️ No Hints Left", "You've used all available hints!")
        return

    row, col, solution = find_empty_and_solution(game_state['original_puzzle'])
    if row is None:
        messagebox.showinfo("ℹ️ Done", "No empty cells to give hint for.")
        return

    entries[row][col].delete(0, tk.END)
    entries[row][col].insert(0, str(solution))
    entries[row][col].config(fg='blue')
    game_state['original_puzzle'][row][col] = solution
    game_state['hints_used'] += 1

def end_game():
    messagebox.showinfo("👋 Game Over", "You gave up! Try again?")
    retry = messagebox.askyesno("Retry?", "Do you want to try a new puzzle?")
    if retry:
        start_new_game()
    else:
        root.quit()

# -----------------------------
# 🧠 UI Buttons
button_frame = tk.Frame(root)
button_frame.grid(row=10, column=0, columnspan=9, pady=10)

submit_btn = tk.Button(button_frame, text="✅ Submit", command=submit)
submit_btn.grid(row=0, column=0, padx=5)

hint_btn = tk.Button(button_frame, text="💡 Hint", command=give_hint)
hint_btn.grid(row=0, column=1, padx=5)

end_btn = tk.Button(button_frame, text="🚪 End Game", command=end_game)
end_btn.grid(row=0, column=2, padx=5)

# -----------------------------
start_new_game()
root.mainloop()
