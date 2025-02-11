import streamlit as st

# Initialize session state variables on first run
if "initialized" not in st.session_state:
    st.session_state.grid = [[" " for _ in range(3)] for _ in range(3)]
    st.session_state.turn_player1 = True  # True means Player 1's turn; False means Player 2's turn
    st.session_state.game_active = True
    st.session_state.winner = None
    st.session_state.initialized = True
    st.session_state.player_setup_done = False

# A simple function to check for a win given a grid and a symbol.
def check_win(grid, symbol):
    # Check rows
    for r in range(3):
        if grid[r][0] == grid[r][1] == grid[r][2] == symbol:
            return True
    # Check columns
    for c in range(3):
        if grid[0][c] == grid[1][c] == grid[2][c] == symbol:
            return True
    # Check diagonals
    if grid[0][0] == grid[1][1] == grid[2][2] == symbol:
        return True
    if grid[0][2] == grid[1][1] == grid[2][0] == symbol:
        return True
    return False

# If the players have not been set up, show a form to input their names and symbols.
if not st.session_state.player_setup_done:
    st.markdown("# Sergio's TicTacs")
    st.markdown("## Welcome to Tic Tac Toe!")
    with st.form("player_info"):
        player1 = st.text_input("Please enter name of player 1:")
        player1_symbol = st.text_input("Please enter symbol of player 1 (default ❌):")
        player2 = st.text_input("Please enter name of player 2:")
        player2_symbol = st.text_input("Please enter symbol of player 2 (default ⭘):")
        submitted = st.form_submit_button("Start Game")
        if submitted:
            st.session_state.player1 = player1 if player1 != "" else "Player 1"
            st.session_state.player1_symbol = player1_symbol if player1_symbol != "" else "❌"
            st.session_state.player2 = player2 if player2 != "" else "Player 2"
            st.session_state.player2_symbol = player2_symbol if player2_symbol != "" else "⭕"
            st.session_state.player_setup_done = True

# Main game interface once setup is complete
if st.session_state.player_setup_done:
    st.markdown("# Sergio's TicTacs")
    st.markdown("## Let's play an epic game of Tic Tac Toe! 🚀")
    
    # Show current turn if game is still active
    if st.session_state.game_active:
        current_player = st.session_state.player1 if st.session_state.turn_player1 else st.session_state.player2
        st.markdown(f"### It's **{current_player}**'s turn!")
    
    # Draw the game grid using 3 columns per row
    board = st.session_state.grid
    for i in range(3):
        cols = st.columns(3)
        for j in range(3):
            cell_val = board[i][j]
            cell_number = i * 3 + j + 1  # Numbering cells from 1 to 9
            # If cell is empty and game is active, create a clickable button.
            if st.session_state.game_active and cell_val == " ":
                if cols[j].button(str(cell_number), key=f"cell_{i}_{j}"):
                    # Place the symbol for the current player if the cell is free.
                    if board[i][j] == " ":
                        if st.session_state.turn_player1:
                            board[i][j] = st.session_state.player1_symbol
                        else:
                            board[i][j] = st.session_state.player2_symbol
                        
                        # Check for a win using the current player's symbol.
                        current_symbol = st.session_state.player1_symbol if st.session_state.turn_player1 else st.session_state.player2_symbol
                        if check_win(board, current_symbol):
                            st.session_state.game_active = False
                            st.session_state.winner = st.session_state.player1 if st.session_state.turn_player1 else st.session_state.player2
                        else:
                            # Check for a full grid (tie)
                            full = all(cell != " " for row in board for cell in row)
                            if full:
                                st.session_state.game_active = False
                                st.session_state.winner = None
                            else:
                                # Toggle to the other player's turn
                                st.session_state.turn_player1 = not st.session_state.turn_player1
                    st.experimental_rerun()
            else:
                # Display the cell's content in large font if not empty or if the game is over.
                cols[j].markdown(f"<h1 style='text-align: center;'>{cell_val}</h1>", unsafe_allow_html=True)
    
    # Show game result if the game has ended
    if not st.session_state.game_active:
        if st.session_state.winner is None:
            st.markdown("## 🤝 It's a tie! Great game!")
        else:
            winner = st.session_state.winner
            st.markdown(f"## 🎉 OMG, {winner} won! Congratulaaaaaations!!!")
            # Determine the loser and display the losing message.
            loser = st.session_state.player1 if winner == st.session_state.player2 else st.session_state.player2
            st.markdown(f"### 😢 Aww, too bad. {loser} lost. Better luck next time <3")
    
    # Button to reset the game (does not reset player names)
    if st.button("Reset Game"):
        st.session_state.grid = [[" " for _ in range(3)] for _ in range(3)]
        st.session_state.turn_player1 = True
        st.session_state.game_active = True
        st.session_state.winner = None
        st.experimental_rerun()
