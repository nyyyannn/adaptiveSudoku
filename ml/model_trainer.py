import pandas as pd
import joblib
import time
import logging
from math import sqrt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error

# Setup logging
logging.basicConfig(level=logging.INFO)

MODEL_PATH = "ml/adaptive_difficulty_model.pkl"
DATA_PATH = "ml/training_data.csv"

# Configurable constants
CV_FOLDS = 5
SCORING_METRIC = 'neg_mean_squared_error'


def train_model():
    # Load training data
    df = pd.read_csv(DATA_PATH)

    # Ensure 'cells_to_remove' exists
    if 'cells_to_remove' not in df.columns:
        raise ValueError("Column 'cells_to_remove' is required for regression training.")

    # Features and target
    X = df[['time_taken', 'mistakes_made', 'hints_used', 'cells_filled_by_user', 'solved_successfully']]
    y = df['cells_to_remove']

    # Split for evaluation
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Define the model
    model = RandomForestRegressor(random_state=42)

    # Define hyperparameters grid for GridSearchCV
    param_grid = {
        'n_estimators': [300, 500],
        'max_depth': [5, 7, 10],
        'min_samples_split': [10, 20],
        'min_samples_leaf': [10, 20],
        'max_features': ['sqrt', 'log2', 1]  # Mixed adaptive + fixed
    }

    # Set up GridSearchCV
    grid_search = GridSearchCV(
        estimator=model,
        param_grid=param_grid,
        cv=CV_FOLDS,
        n_jobs=-1,
        scoring=SCORING_METRIC,
        verbose=1  # Show progress logs
    )

    # Time the search
    start = time.time()
    grid_search.fit(X_train, y_train)
    elapsed = time.time() - start
    print("Grid search took", elapsed, "seconds")

    # Best model from grid search
    best_model = grid_search.best_estimator_
    best_params = grid_search.best_params_
    best_cv_mse = -grid_search.best_score_

    print(f"[✅] Best parameters found: {best_params}")
    print(f"[✅] Best cross-validation MSE: {best_cv_mse:.2f}")

    # Evaluate on test set
    predictions = best_model.predict(X_test)
    test_mse = mean_squared_error(y_test, predictions)
    test_rmse = sqrt(test_mse)
    print(f"[✅] Model trained. MSE on test set: {test_mse:.2f}")
    print(f"[📏] RMSE on test set: {test_rmse:.2f} cells")

    # Save model + metadata
    model_info = {
        "best_params": best_params,
        "cv_mse": best_cv_mse,
        "test_mse": test_mse,
        "test_rmse": test_rmse,
        "rows_trained": len(df)
    }

    joblib.dump((best_model, model_info), MODEL_PATH)
    print(f"[💾] Model and metadata saved to {MODEL_PATH}")


if __name__ == "__main__":
    train_model()