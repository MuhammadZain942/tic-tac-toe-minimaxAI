import sys
import pygame
import numpy as np

pygame.init()

# defining colors
WHITE = (255, 255, 255) 
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
GREEN = (0, 255, 0)   

# sizes
WIDTH = 300
HEIGHT = 300
LINE_WIDTH = 5
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25

# initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC TAC TOE MINIMAX AI')
screen.fill(BLACK)

# initial state
board = np.zeros((BOARD_ROWS, BOARD_COLS))

# draw lines for the grid
def draw_lines(color=WHITE):
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, color, (0, SQUARE_SIZE * i), (WIDTH, SQUARE_SIZE * i), LINE_WIDTH)  # horizontal
        pygame.draw.line(screen, color, (SQUARE_SIZE * i, 0), (SQUARE_SIZE * i, HEIGHT), LINE_WIDTH)  # vertical

# draw the symbols (O for human, X for AI)
def draw_figures(color=WHITE):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:  # Player 1 (circle)
                pygame.draw.circle(screen, color, 
                    (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)),
                    CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 2:  # Player 2 (cross)
                pygame.draw.line(screen, color, 
                    (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4), 
                    (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4), 
                    CROSS_WIDTH)
                pygame.draw.line(screen, color, 
                    (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4), 
                    (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4), 
                    CROSS_WIDTH)

# marking the board
def mark_square(row, col, player):
    board[row][col] = player

# check if a square is available
def available_square(row, col):
    return board[row][col] == 0

# check if board is full
def is_board_full(check_board=board):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if check_board[row][col] == 0:
                return False
    return True

# check if a player has won
def check_win(player, check_board=board):
    for col in range(BOARD_COLS):
        if check_board[0][col] == player and check_board[1][col] == player and check_board[2][col] == player:
            return True
    for row in range(BOARD_ROWS):
        if check_board[row][0] == player and check_board[row][1] == player and check_board[row][2] == player:
            return True
    if check_board[0][0] == player and check_board[1][1] == player and check_board[2][2] == player:
        return True
    if check_board[0][2] == player and check_board[1][1] == player and check_board[2][0] == player:
        return True
    return False

# minimax algorithm for AI decision-making
def minimax(minimax_board, depth, is_maximizing):
    # base case
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

# restart game
def restart_game():
    screen.fill(BLACK)
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = 0

# Calling function
draw_lines()
player = 1
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        # Human's turn
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0] // SQUARE_SIZE
            mouseY = event.pos[1] // SQUARE_SIZE
            if available_square(mouseY, mouseX):
                mark_square(mouseY, mouseX, player)
                if check_win(player):
                    game_over = True
                else:
                    player = 2

        # AI's turn
        if player == 2 and not game_over:
            best_move()
            if check_win(2):
                game_over = True
            else:
                player = 1

        # Handle restart
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            restart_game()
            game_over = False
            player = 1

    # Drawing figures
    draw_figures()

    # Show game over display
    if game_over:
        if check_win(1):
            draw_figures(GREEN)
            draw_lines(GREEN)
        elif check_win(2):
            draw_figures(RED)
            draw_lines(RED)
        else:
            draw_figures(GRAY)
            draw_lines(GRAY)

    pygame.display.update()
