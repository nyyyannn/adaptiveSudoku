import random

def is_safe(board, row, col, num):
    # Check row and column
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False

    # Check 3x3 grid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False

    return True

def find_empty(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return row, col
    return None

def fill_board(board):
    empty = find_empty(board)
    if not empty:
        return True  # Board is full
    row, col = empty

    nums = list(range(1, 10))
    random.shuffle(nums)  # Add randomness to generate different boards

    for num in nums:
        if is_safe(board, row, col, num):
            board[row][col] = num
            if fill_board(board):
                return True
            board[row][col] = 0  # Backtrack

    return False

def generate_full_board():
    board = [[0 for _ in range(9)] for _ in range(9)]
    if fill_board(board):
        return board
    else:
        raise Exception("Something went wrong during board generation.")
