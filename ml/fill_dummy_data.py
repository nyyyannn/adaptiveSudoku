import random
from tracker.logger import log_game_result

def simulate_game(player_type):
    if player_type == "pro":
        return {
            "time_taken": random.randint(80, 150),
            "mistakes_made": random.randint(0, 1),
            "hints_used": 0,
            "cells_filled_by_user": random.randint(48, 54),
            "solved_successfully": 1,
            "cells_to_remove": random.randint(22, 35)  # Higher difficulty
        }
    elif player_type == "average":
        return {
            "time_taken": random.randint(150, 300),
            "mistakes_made": random.randint(2, 4),
            "hints_used": random.randint(0, 2),
            "cells_filled_by_user": random.randint(38, 47),
            "solved_successfully": random.choice([1, 1, 0]),
            "cells_to_remove": random.randint(14, 21)
        }
    elif player_type == "struggler":
        return {
            "time_taken": random.randint(300, 700),
            "mistakes_made": random.randint(5, 10),
            "hints_used": random.randint(2, 5),
            "cells_filled_by_user": random.randint(20, 37),
            "solved_successfully": random.choice([0, 0, 1]),
            "cells_to_remove": random.randint(5, 13)  # Easier puzzle
        }

# Fill up training data
for _ in range(200):
    log_game_result(simulate_game("pro"))

for _ in range(200):
    log_game_result(simulate_game("average"))

for _ in range(200):
    log_game_result(simulate_game("struggler"))

print("[🚀] Dummy data generation complete.")
