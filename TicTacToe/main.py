import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 300, 300
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Game variables
BOARD_SIZE = 3
CELL_SIZE = WIDTH // BOARD_SIZE

# Initialize the board
board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

def draw_board():
    SCREEN.fill(WHITE)
    for i in range(1, BOARD_SIZE):
        pygame.draw.line(SCREEN, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), 2)
        pygame.draw.line(SCREEN, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), 2)

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == 'X':
                pygame.draw.line(SCREEN, RED, (col * CELL_SIZE + 20, row * CELL_SIZE + 20),
                                 ((col + 1) * CELL_SIZE - 20, (row + 1) * CELL_SIZE - 20), 2)
                pygame.draw.line(SCREEN, RED, ((col + 1) * CELL_SIZE - 20, row * CELL_SIZE + 20),
                                 (col * CELL_SIZE + 20, (row + 1) * CELL_SIZE - 20), 2)
            elif board[row][col] == 'O':
                pygame.draw.circle(SCREEN, BLUE, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2),
                                   CELL_SIZE // 2 - 20, 2)

def check_winner():
    # Check rows, columns, and diagonals
    for i in range(BOARD_SIZE):
        if board[i][0] == board[i][1] == board[i][2] != ' ':
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != ' ':
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return board[0][2]
    return None

def is_board_full():
    return all(board[i][j] != ' ' for i in range(BOARD_SIZE) for j in range(BOARD_SIZE))

def computer_move():
    empty_cells = [(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE) if board[i][j] == ' ']
    if empty_cells:
        row, col = random.choice(empty_cells)
        board[row][col] = 'X'

def play_game():
    global board
    board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    game_over = False
    winner = None

    computer_move()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x, y = event.pos
                col = x // CELL_SIZE
                row = y // CELL_SIZE
                if board[row][col] == ' ':
                    board[row][col] = 'O'
                    winner = check_winner()
                    if winner or is_board_full():
                        game_over = True
                    else:
                        computer_move()
                        winner = check_winner()
                        if winner or is_board_full():
                            game_over = True

        draw_board()
        pygame.display.flip()

        if game_over:
            font = pygame.font.Font(None, 36)
            if winner:
                text = font.render(f"{winner} wins!", True, BLACK)
            else:
                text = font.render("It's a tie!", True, BLACK)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            SCREEN.blit(text, text_rect)
            pygame.display.flip()
            pygame.time.wait(2000)

            play_again_text = font.render("Play again? (Y/N)", True, BLACK)
            play_again_rect = play_again_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
            SCREEN.blit(play_again_text, play_again_rect)
            pygame.display.flip()

            waiting_for_input = True
            while waiting_for_input:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_y:
                            return True
                        elif event.key == pygame.K_n:
                            return False

    return True

def main():
    while play_game():
        pass
    pygame.quit()

if __name__ == "__main__":
    main()