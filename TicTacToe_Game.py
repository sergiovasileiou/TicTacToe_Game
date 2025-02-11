import streamlit as st
import math

# Define markers
HUMAN = "❌"
COMP = "⭕"
EMPTY = " "

# Initialize session state variables if not already set
if "board" not in st.session_state:
    st.session_state.board = [EMPTY for _ in range(9)]
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "result_message" not in st.session_state:
    st.session_state.result_message = ""

def is_winner(board, marker):
    win_conditions = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # horizontal
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # vertical
        (0, 4, 8), (2, 4, 6)              # diagonal
    ]
    for (a, b, c) in win_conditions:
        if board[a] == board[b] == board[c] == marker:
            return True
    return False

def is_draw(board):
    return all(cell != EMPTY for cell in board)

def minimax(board, depth, is_maximizing):
    if is_winner(board, COMP):
        return 1
    elif is_winner(board, HUMAN):
        return -1
    elif is_draw(board):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if board[i] == EMPTY:
                board[i] = COMP
                score = minimax(board, depth + 1, False)
                board[i] = EMPTY
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if board[i] == EMPTY:
                board[i] = HUMAN
                score = minimax(board, depth + 1, True)
                board[i] = EMPTY
                best_score = min(score, best_score)
        return best_score

def best_move(board):
    best_score = -math.inf
    move = None
    for i in range(9):
        if board[i] == EMPTY:
            board[i] = COMP
            score = minimax(board, 0, False)
            board[i] = EMPTY
            if score > best_score:
                best_score = score
                move = i
    return move

def computer_move():
    board = st.session_state.board
    move = best_move(board)
    if move is not None:
        board[move] = COMP
        if is_winner(board, COMP):
            st.session_state.result_message = "😢 Aww, too bad. You lost. Better luck next time <3"
            st.session_state.game_over = True
        elif is_draw(board):
            st.session_state.result_message = "🤝 It's a tie! Great game!"
            st.session_state.game_over = True

def handle_move(index):
    board = st.session_state.board
    # Only allow a move if the cell is empty and the game is not over
    if board[index] == EMPTY and not st.session_state.game_over:
        board[index] = HUMAN
        if is_winner(board, HUMAN):
            st.session_state.result_message = "🎉 OMG, you won! Congratulaaaaaations!!!"
            st.session_state.game_over = True
        elif is_draw(board):
            st.session_state.result_message = "🤝 It's a tie! Great game!"
            st.session_state.game_over = True
        else:
            computer_move()

# Display title and instructions
st.markdown("# Sergio's TicTacs")
st.markdown("## Let's play an epic game of Tic Tac Toe! 🚀")
st.markdown("You are **❌**, while the computer is **⭕**.")
st.write("### Board Positions:")
st.write("1 | 2 | 3")
st.write("4 | 5 | 6")
st.write("7 | 8 | 9")

# Draw the game board as a 3x3 grid
board = st.session_state.board
for row in range(3):
    cols = st.columns(3)
    for col in range(3):
        index = row * 3 + col
        cell = board[index]
        # If cell is empty and game is still on, show a button; otherwise, display the marker.
        if cell == EMPTY and not st.session_state.game_over:
            if cols[col].button(str(index + 1), key=f"btn_{index}"):
                handle_move(index)
                st.experimental_rerun()
        else:
            cols[col].markdown(f"<h1 style='text-align: center;'>{cell}</h1>", unsafe_allow_html=True)

if st.session_state.game_over:
    st.markdown(f"## {st.session_state.result_message}")

# Reset button to restart the game
if st.button("Reset Game"):
    st.session_state.board = [EMPTY for _ in range(9)]
    st.session_state.game_over = False
    st.session_state.result_message = ""
    st.experimental_rerun()
