import streamlit as st
import random

# Set the title
st.title("Sergio's Tics & Tacs")

# Initialize session state variables if they don't exist.
if "board" not in st.session_state:
    st.session_state.board = [""] * 9
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "result" not in st.session_state:
    st.session_state.result = ""

# Helper functions
def check_win(board, marker):
    wins = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),   # rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),   # columns
        (0, 4, 8), (2, 4, 6)              # diagonals
    ]
    for a, b, c in wins:
        if board[a] == board[b] == board[c] == marker:
            return True
    return False

def check_draw(board):
    return all(cell in ["X", "O"] for cell in board)

def computer_move():
    available = [i for i in range(9) if st.session_state.board[i] == ""]
    if available:
        move = random.choice(available)
        st.session_state.board[move] = "O"

# Function to reset the game.
def reset_game():
    st.session_state.board = [""] * 9
    st.session_state.game_over = False
    st.session_state.result = ""
    st.experimental_rerun()

# Display the board as a 3x3 grid using columns.
st.write("**Game Board**")
for row in range(3):
    cols = st.columns(3)
    for col in range(3):
        idx = row * 3 + col
        cell = st.session_state.board[idx]
        with cols[col]:
            # If the cell is already filled, display its value.
            if cell != "":
                st.markdown(f"<h1 style='text-align: center;'>{cell}</h1>", unsafe_allow_html=True)
            else:
                # Only allow a move if the game is not over.
                if not st.session_state.game_over:
                    if st.button(" ", key=f"cell_{idx}", help=f"Cell {idx+1}"):
                        st.session_state.board[idx] = "X"
                        # Check if the player wins with this move.
                        if check_win(st.session_state.board, "X"):
                            st.session_state.game_over = True
                            st.session_state.result = "win"
                        elif check_draw(st.session_state.board):
                            st.session_state.game_over = True
                            st.session_state.result = "draw"
                        else:
                            # Let the computer make its move.
                            computer_move()
                            if check_win(st.session_state.board, "O"):
                                st.session_state.game_over = True
                                st.session_state.result = "loss"
                            elif check_draw(st.session_state.board):
                                st.session_state.game_over = True
                                st.session_state.result = "draw"
                        st.experimental_rerun()  # Rerun to update the board

# Show game over messages if the game has ended.
if st.session_state.game_over:
    st.markdown("---")
    if st.session_state.result == "win":
        st.image("win_image.png", width=150)
        st.success("OMG, you won! Congratulatioooons!!!")
    elif st.session_state.result == "loss":
        st.image("loss_image.png", width=150)
        st.error("Aw, too bad! You lost. Try again next time <3")
    else:
        st.warning("It's a draw!")

# Reset game button
if st.button("Reset Game"):
    reset_game()
