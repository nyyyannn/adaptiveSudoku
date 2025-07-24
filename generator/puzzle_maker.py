import random
import copy
import joblib
import os
import pandas as pd
from generator.board_generator import is_safe, generate_full_board

MODEL_PATH = "ml/adaptive_difficulty_model.pkl"

# Features expected by the model
FEATURE_COLUMNS = [
    "time_taken"
]

def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Trained difficulty model not found.")
    return joblib.load(MODEL_PATH)

def predict_cells_to_remove(metrics: dict):
    model = load_model()

    # Check that all necessary metrics are present
    missing = [feature for feature in FEATURE_COLUMNS if feature not in metrics]
    if missing:
        raise ValueError(f"Missing required metrics: {missing}")

    # Make a DataFrame for prediction
    input_df = pd.DataFrame([[metrics[feature] for feature in FEATURE_COLUMNS]], columns=FEATURE_COLUMNS)
    prediction = model.predict(input_df)[0]
    
    # Ensure it's an integer within [20, 60] range
    return int(max(20, min(60, round(prediction))))

def count_solutions(board):
    """
    Counts the number of solutions for a given Sudoku board using backtracking.
    Returns the number of solutions (stops at 2 for efficiency).
    """
    def solve_count(bd):
        for row in range(9):
            for col in range(9):
                if bd[row][col] == 0:
                    count = 0
                    for num in range(1, 10):
                        if is_safe(bd, row, col, num):
                            bd[row][col] = num
                            count += solve_count(bd)
                            if count > 1:
                                bd[row][col] = 0
                                return count
                            bd[row][col] = 0
                    return count
        return 1
    # Use a deep copy to avoid mutating the original board
    return solve_count(copy.deepcopy(board))

def remove_cells_from_board(board, num_cells_to_remove):
    """
    Helper to remove up to num_cells_to_remove from a single board, ensuring uniqueness after each removal.
    Returns the puzzle and the number of cells actually removed.
    """
    puzzle = copy.deepcopy(board)
    cells = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(cells)
    removed = 0
    for row, col in cells:
        if removed >= num_cells_to_remove:
            break
        if puzzle[row][col] == 0:
            continue
        backup = puzzle[row][col]
        puzzle[row][col] = 0
        if count_solutions(puzzle) == 1:
            removed += 1
        else:
            puzzle[row][col] = backup
    return puzzle, removed

def remove_cells(board, user_metrics):
    """
    board: fully-filled 9x9 sudoku grid (ignored, for compatibility)
    user_metrics: dict with key - 'time_taken'
    Generates 10 boards, removes cells from each, and returns the puzzle with cells removed closest to the target (ensuring uniqueness).
    Stops early if a puzzle matches the target exactly.
    """
    num_cells_to_remove = predict_cells_to_remove(user_metrics)
    best_puzzle = None
    best_removed = -1
    NUM_BOARDS = 10
    for _ in range(NUM_BOARDS):
        full_board = generate_full_board()
        puzzle, removed = remove_cells_from_board(full_board, num_cells_to_remove)
        if abs(removed - num_cells_to_remove) < abs(best_removed - num_cells_to_remove) or best_puzzle is None:
            best_puzzle = puzzle
            best_removed = removed
        if removed == num_cells_to_remove:
            break
    return best_puzzle

def print_board(board):
    print("\n🧩 Puzzle Board:")
    for i, row in enumerate(board):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j, val in enumerate(row):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            print(val if val != 0 else ".", end=" ")
        print()