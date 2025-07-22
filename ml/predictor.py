import joblib
import numpy as np
import os
import pandas as pd

MODEL_PATH = "ml/adaptive_difficulty_model.pkl"

# Explicit feature order — crucial for consistent prediction
FEATURE_COLUMNS = [
    "time_taken",
    "mistakes_made",
    "hints_used",
    "cells_filled_by_user",
    "solved_successfully"
]

def predict_cells_to_remove(metrics: dict):
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("🚫 Model not found. Please train the model first.")

    model = joblib.load(MODEL_PATH)

    # Ensure all features are included
    missing = [col for col in FEATURE_COLUMNS if col not in metrics]
    if missing:
        raise ValueError(f"🚫 Missing features in input: {missing}")

    # Convert input dict to DataFrame with correct column order
    input_df = pd.DataFrame([[metrics[col] for col in FEATURE_COLUMNS]], columns=FEATURE_COLUMNS)

    # Make prediction
    predicted_cells = model.predict(input_df)[0]

    # Clamp result to reasonable range (optional but good practice)
    return int(max(10, min(60, round(predicted_cells))))
