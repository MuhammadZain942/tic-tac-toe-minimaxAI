def minimax(minimax_board, depth, is_maximizing):
    if check_win(2, minimax_board):  # AI wins
        return float('inf')
    elif check_win(1, minimax_board):  # Human wins
        return float('-inf')
    if all(minimax_board[row][col] != 0 for row in range(BOARD_ROWS) for col in range(BOARD_COLS)):
        return 0
    if is_maximizing:
        best_score = -1000
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 2
                    score = minimax(minimax_board, depth + 1, is_maximizing=False)
                    minimax_board[row][col] = 0
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = 1000
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 1
                    score = minimax(minimax_board, depth + 1, is_maximizing=True)
                    minimax_board[row][col] = 0
                    best_score = min(score, best_score)
        return best_score

# AI determines the best move
def best_move():
    best_score = -1000
    move = (-1, -1)
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                board[row][col] = 2
                score = minimax(board, 0, is_maximizing=False)
                board[row][col] = 0
                if score > best_score:
                    best_score = score
                    move = (row, col)
    if move != (-1, -1):
        mark_square(move[0], move[1], 2)