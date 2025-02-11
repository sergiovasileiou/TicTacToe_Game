import pygame
import sys
import random

# Initialize PyGame.
pygame.init()

# Set up display constants.
WIDTH, HEIGHT = 300, 350  # 300x300 for board and extra space for messages.
BOARD_SIZE = 300
CELL_SIZE = BOARD_SIZE // 3

# Set up the game window.
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sergio's Tics & Tacs")

# Define board state.
board = [""] * 9  # 9 cells initialized as empty.
player = "X"       # Human is 'X'
computer = "O"     # Computer is 'O'

# Define colors.
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Set up fonts.
marker_font = pygame.font.SysFont(None, 60)
msg_font = pygame.font.SysFont(None, 28)

# Load images for win and loss screens.
# Ensure that these image files are available in the same directory.
win_img = pygame.image.load("win_image.png")
loss_img = pygame.image.load("loss_image.png")
# Optionally, scale images to the desired dimensions.
win_img = pygame.transform.scale(win_img, (100, 100))
loss_img = pygame.transform.scale(loss_img, (100, 100))

def draw_board():
    """Draws the Tic Tac Toe board and any placed markers."""
    screen.fill(WHITE)
    # Draw vertical grid lines.
    pygame.draw.line(screen, BLACK, (CELL_SIZE, 0), (CELL_SIZE, BOARD_SIZE), 2)
    pygame.draw.line(screen, BLACK, (CELL_SIZE * 2, 0), (CELL_SIZE * 2, BOARD_SIZE), 2)
    # Draw horizontal grid lines.
    pygame.draw.line(screen, BLACK, (0, CELL_SIZE), (BOARD_SIZE, CELL_SIZE), 2)
    pygame.draw.line(screen, BLACK, (0, CELL_SIZE * 2), (BOARD_SIZE, CELL_SIZE * 2), 2)
    
    # Draw markers in each cell.
    for idx in range(9):
        col = idx % 3
        row = idx // 3
        x = col * CELL_SIZE + CELL_SIZE // 2
        y = row * CELL_SIZE + CELL_SIZE // 2
        if board[idx] == "X":
            text = marker_font.render("X", True, RED)
            screen.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))
        elif board[idx] == "O":
            text = marker_font.render("O", True, BLUE)
            screen.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))
    
    pygame.display.update()

def check_win(mark):
    """Checks if the specified mark ('X' or 'O') has any winning combination."""
    wins = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
        (0, 4, 8), (2, 4, 6)              # diagonals
    ]
    for a, b, c in wins:
        if board[a] == board[b] == board[c] == mark:
            return True
    return False

def check_draw():
    """Checks if the board is completely filled resulting in a draw."""
    return all(cell in ["X", "O"] for cell in board)

def computer_move():
    """Makes a random valid move for the computer."""
    available = [i for i in range(9) if board[i] == ""]
    if available:
        move = random.choice(available)
        board[move] = computer

def game_over_screen(result):
    """Displays the game over screen with relevant image and message.
    
    The result parameter should be:
      - 'win' if the player wins,
      - 'loss' if the computer wins,
      - 'draw' for a draw.
    """
    screen.fill(WHITE)
    if result == "win":
        message = "OMG, you won! Congratulatioooons!!!"
        # Blit the win image.
        screen.blit(win_img, ((WIDTH - win_img.get_width()) // 2, 50))
    elif result == "loss":
        message = "Aw, too bad! You lost. Try again next time <3"
        # Blit the loss image.
        screen.blit(loss_img, ((WIDTH - loss_img.get_width()) // 2, 50))
    else:
        message = "It's a draw!"
    
    # Render and blit the message.
    text_surface = msg_font.render(message, True, BLACK)
    screen.blit(text_surface, ((WIDTH - text_surface.get_width()) // 2, 170))
    pygame.display.update()
    
    # Wait for a few seconds before exiting.
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

def main():
    running = True
    game_over = False
    draw_board()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Process mouse clicks when the game has not ended.
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x, y = pygame.mouse.get_pos()
                # Ensure the click is within the board area.
                if y < BOARD_SIZE:
                    col = x // CELL_SIZE
                    row = y // CELL_SIZE
                    idx = row * 3 + col
                    if board[idx] == "":
                        board[idx] = player
                        draw_board()
                        if check_win(player):
                            game_over_screen("win")
                            game_over = True
                        elif check_draw():
                            game_over_screen("draw")
                            game_over = True
                        else:
                            # Let the computer take its move.
                            computer_move()
                            draw_board()
                            if check_win(computer):
                                game_over_screen("loss")
                                game_over = True
                            elif check_draw():
                                game_over_screen("draw")
                                game_over = True
        pygame.display.update()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
