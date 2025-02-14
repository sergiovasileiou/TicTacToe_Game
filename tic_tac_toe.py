import streamlit as st
import math
import time

# Define markers and board values
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
if "player_mode" not in st.session_state:
    st.session_state.player_mode = None
if "current_turn" not in st.session_state:
    st.session_state.current_turn = HUMAN

def is_winner(board, marker):
    win_conditions = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),   # rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),   # cols
        (0, 4, 8), (2, 4, 6)               # diagonals
    ]
    return any(board[a] == board[b] == board[c] == marker for a, b, c in win_conditions)

def is_draw(board):
    return all(cell != EMPTY for cell in board)

def minimax(board, is_maximizing):
    if is_winner(board, COMP):
        return 1
    if is_winner(board, HUMAN):
        return -1
    if is_draw(board):
        return 0
    
    scores = []
    moves = []
    for i in range(9):
        if board[i] == EMPTY:
            board[i] = COMP if is_maximizing else HUMAN
            score = minimax(board, not is_maximizing)
            board[i] = EMPTY
            scores.append(score)
            moves.append(i)
    return max(scores) if is_maximizing else min(scores)

def best_move():
    best_score = -math.inf
    move = None
    for i in range(9):
        if st.session_state.board[i] == EMPTY:
            st.session_state.board[i] = COMP
            score = minimax(st.session_state.board, False)
            st.session_state.board[i] = EMPTY
            if score > best_score:
                best_score, move = score, i
    return move
    
def handle_move(index):
    board = st.session_state.board
    if board[index] == EMPTY and not st.session_state.game_over:
        board[index] = st.session_state.current_turn
        
        if is_winner(board, st.session_state.current_turn):
            st.session_state.result_message = f"🎉 {st.session_state.current_turn} WINS! Congratulations!"
            st.session_state.game_over = True
        elif is_draw(board):
            st.session_state.result_message = "🤝 It's a tie! Well played!"
            st.session_state.game_over = True
        else:
            if st.session_state.player_mode == "1 Player" and st.session_state.current_turn == HUMAN:
                st.session_state.current_turn = COMP
                st.rerun()  # Rerun before AI move for smooth UI update
                computer_move()
            else:
                st.session_state.current_turn = HUMAN if st.session_state.current_turn == COMP else COMP
        
        st.rerun()  # Ensure UI refresh after move

def computer_move():
    move = best_move()
    if move is not None:
        st.session_state.board[move] = COMP
    if is_winner(st.session_state.board, COMP):
        st.session_state.result_message = "😢 You lost! Better luck next time!"
        st.session_state.game_over = True
    elif is_draw(st.session_state.board):
        st.session_state.result_message = "🤝 It's a tie!"
        st.session_state.game_over = True
    else:
        st.session_state.current_turn = HUMAN  # Only switch turns if the game isn't over

    st.rerun()  # Refresh UI immediately after the move


st.title("🔥 Ultimate Tic-Tac-Toe 🔥")
st.subheader("Let's battle it out! 🚀")
st.markdown("---")

if st.session_state.player_mode is None:
    st.session_state.player_mode = st.radio("Select game mode:", ["1 Player", "2 Players"])
    st.session_state.current_turn = HUMAN
    st.session_state.board = [EMPTY for _ in range(9)]
    st.session_state.game_over = False
    st.session_state.result_message = ""
    st.stop()

if st.button("Reset Game"):
    st.session_state.board = [EMPTY for _ in range(9)]
    st.session_state.game_over = False
    st.session_state.result_message = ""
    st.session_state.current_turn = HUMAN
    st.session_state.player_mode = None
    st.rerun()

board = st.session_state.board
for row in range(3):
    cols = st.columns(3)
    for col in range(3):
        index = row * 3 + col
        cell = board[index]
        if cell == EMPTY and not st.session_state.game_over:
            if cols[col].button(f" ", key=f"btn_{index}"):
                handle_move(index)
        else:
            cols[col].markdown(f"<h1 style='text-align: center;'>{cell}</h1>", unsafe_allow_html=True)

if st.session_state.game_over:
    st.subheader(st.session_state.result_message)
