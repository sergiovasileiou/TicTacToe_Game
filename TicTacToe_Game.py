import streamlit as st
#!/usr/bin/env python3
import math

# Define our markers and the empty slot representation
human = "❌"
comp = "⭕"
empty = " "  # Empty cell

def print_board(board):
    """Prints the current game board with decorative spacing."""
    # Create a board display that shows numbers for empty spots
    display = []
    for i, cell in enumerate(board):
        if cell == empty:
            display.append(str(i + 1))
        else:
            display.append(cell)
    print("\n")
    print("         {}      |      {}      |      {}".format(display[0], display[1], display[2]))
    print("   ---------------+---------------+---------------")
    print("         {}      |      {}      |      {}".format(display[3], display[4], display[5]))
    print("   ---------------+---------------+---------------")
    print("         {}      |      {}      |      {}".format(display[6], display[7], display[8]))
    print("\n")

def is_winner(board, marker):
    """Checks for winning conditions for specified marker."""
    win_conditions = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6)
    ]
    for (a, b, c) in win_conditions:
        if board[a] == board[b] == board[c] == marker:
            return True
    return False

def is_draw(board):
    """Determines if the board is full (a draw)."""
    return all(cell != empty for cell in board)

def minimax(board, depth, is_maximizing):
    """Minimax algorithm to choose the best move for the computer."""
    if is_winner(board, comp):
        return 1
    elif is_winner(board, human):
        return -1
    elif is_draw(board):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if board[i] == empty:
                board[i] = comp
                score = minimax(board, depth + 1, False)
                board[i] = empty
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if board[i] == empty:
                board[i] = human
                score = minimax(board, depth + 1, True)
                board[i] = empty
                best_score = min(score, best_score)
        return best_score

def best_move(board):
    """Determines the best move for the computer using minimax."""
    best_score = -math.inf
    move = None
    for i in range(9):
        if board[i] == empty:
            board[i] = comp
            score = minimax(board, 0, False)
            board[i] = empty
            if score > best_score:
                best_score = score
                move = i
    return move

def display_title():
    """Displays a big, fun title for Sergio's TicTacs."""
    print("**************************************************")
    print("*           Welcome to Sergio's TicTacs!         *")
    print("*         Let's play an epic game of TicTacToe!   *")
    print("**************************************************\n")

def main():
    board = [empty for _ in range(9)]
    display_title()
    print("You are playing as {} and the computer is {}.".format(human, comp))
    print("Choose a position by entering a number between 1-9 corresponding to:")
    print("\n 1 | 2 | 3 ")
    print("-----------")
    print(" 4 | 5 | 6 ")
    print("-----------")
    print(" 7 | 8 | 9 \n")
    
    while True:
        print_board(board)
        
        if is_winner(board, human):
            print("**************************************************")
            print("🎉 OMG, you won! Congratulaaaaaations!!! 🎉")
            print("**************************************************")
            break
        if is_winner(board, comp):
            print("**************************************************")
            print("😢 Aww, too bad. You lost. Better luck next time <3")
            print("**************************************************")
            break
        if is_draw(board):
            print("**************************************************")
            print("🤝 It's a tie! Great game!")
            print("**************************************************")
            break
        
        # Human turn
        valid_move = False
        while not valid_move:
            try:
                move = int(input("Your move (1-9): ")) - 1
                if move < 0 or move > 8:
                    print("❗ Invalid position. Choose a number between 1 and 9.")
                elif board[move] != empty:
                    print("❗ That spot is already taken. Try another!")
                else:
                    board[move] = human
                    valid_move = True
            except ValueError:
                print("❗ Please enter a valid number.")
        
        # Check if the game ended after the human move
        if is_winner(board, human) or is_draw(board):
            continue

        # Computer turn
        comp_index = best_move(board)
        if comp_index is not None:
            board[comp_index] = comp
            print("Computer placed {} in position {}".format(comp, comp_index + 1))

if __name__ == '__main__':
    main()

