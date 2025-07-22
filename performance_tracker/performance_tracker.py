import time

class GameTracker:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.mistakes = 0
        self.time_taken = 0

    def start_game(self):
        self.start_time = time.time()

    def end_game(self):
        self.end_time = time.time()
        self.time_taken = self.end_time - self.start_time  # Time taken in seconds

    def add_mistake(self):
        self.mistakes += 1

    def reset(self):
        self.mistakes = 0
        self.time_taken = 0
        self.start_time = None
        self.end_time = None
