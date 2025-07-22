from tracker.logger import log_game_result
from ml.model_trainer import train_model
from ml.predictor import predict_cells_to_remove

def get_int_input(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("⚠️ Enter a valid number.")

def cli():
    print("\n🎮 Sudoku Adaptive Difficulty CLI 🎮")
    while True:
        print("\nChoose an option:")
        print("1. Log a new game result")
        print("2. Train the model")
        print("3. Predict cells to remove for next puzzle")
        print("4. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            time_taken = get_int_input("🕒 Time taken (in seconds): ")
            mistakes = get_int_input("❌ Mistakes made: ")
            hints = get_int_input("💡 Hints used: ")
            cells_filled = get_int_input("✍️ Cells filled by user: ")
            success = get_int_input("✅ Solved successfully? (1 for yes, 0 for no): ")
            cells_to_remove = get_int_input("🎯 How many cells were removed in this game? ")

            game_data = {
                "time_taken": time_taken,
                "mistakes_made": mistakes,
                "hints_used": hints,
                "cells_filled_by_user": cells_filled,
                "solved_successfully": success,
                "cells_to_remove": cells_to_remove
            }

            log_game_result(game_data)

        elif choice == "2":
            try:
                train_model()
            except Exception as e:
                print(f"[❌] Model training failed: {e}")

        elif choice == "3":
            print("\nEnter your recent game stats:")
            time_taken = get_int_input("🕒 Time taken (in seconds): ")
            mistakes = get_int_input("❌ Mistakes made: ")
            hints = get_int_input("💡 Hints used: ")
            cells_filled = get_int_input("✍️ Cells filled by user: ")
            success = get_int_input("✅ Solved successfully? (1 for yes, 0 for no): ")

            user_metrics = {
                "time_taken": time_taken,
                "mistakes_made": mistakes,
                "hints_used": hints,
                "cells_filled_by_user": cells_filled,
                "solved_successfully": success
            }

            try:
                prediction = predict_cells_to_remove(user_metrics)
                print(f"\n[🎯] Recommended cells to remove for next puzzle: **{prediction}**")
            except Exception as e:
                print(f"[❌] Prediction failed: {e}")

        elif choice == "4":
            print("👋 Exiting CLI.")
            break
        else:
            print("❌ Invalid choice. Try again.")

if __name__ == "__main__":
    cli()
