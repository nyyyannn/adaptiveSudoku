import random
import copy
import joblib
import os
import pandas as pd

MODEL_PATH = "ml/adaptive_difficulty_model.pkl"

# Features expected by the model
FEATURE_COLUMNS = [
    "time_taken",
    "mistakes_made",
    "hints_used",
    "cells_filled_by_user",
    "solved_successfully"
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

def remove_cells(board, user_metrics):
    """
    board: fully-filled 9x9 sudoku grid
    user_metrics: dict with keys - 'time_taken', 'mistakes_made', 'hints_used', 'cells_filled_by_user', 'solved_successfully'
    """
    num_cells_to_remove = predict_cells_to_remove(user_metrics)

    puzzle = copy.deepcopy(board)
    removed = 0

    while removed < num_cells_to_remove:
        row = random.randint(0, 8)
        col = random.randint(0, 8)

        if puzzle[row][col] != 0:
            puzzle[row][col] = 0
            removed += 1

    return puzzle

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