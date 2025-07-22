import csv
import os

FILE_PATH = "ml/training_data.csv"

FIELDNAMES = [
    "time_taken",
    "mistakes_made",
    "hints_used",
    "cells_filled_by_user",
    "solved_successfully",
    "cells_to_remove"  # 🎯 New target for regression
]

def log_game_result(data: dict):
    # Ensure only valid fields are logged
    filtered_data = {field: data.get(field, "") for field in FIELDNAMES}

    # Create the file with headers if it doesn't exist
    file_exists = os.path.isfile(FILE_PATH)
    
    with open(FILE_PATH, mode="a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)
        if not file_exists:
            writer.writeheader()
        writer.writerow(filtered_data)

    print(f"[✅] Game result logged: {filtered_data}")
