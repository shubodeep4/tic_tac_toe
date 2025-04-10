import os
from colorama import Fore, Style, init
import math

init(autoreset=True)

GAME_STATE_FILE = "game_state.txt"
SCOREBOARD_FILE = "scoreboard.txt"

def display_board(board):
    symbol_color = {'X': Fore.RED, 'O': Fore.BLUE, '-': Fore.WHITE}
    print("\nCurrent Board:")
    for i in range(3):
        row_display = ' | '.join([symbol_color[cell] + cell + Style.RESET_ALL for cell in board[i]])
        print(" " + row_display)
        if i < 2:
            print("---+---+---")

def check_winner(board, symbol):
    for i in range(3):
        if all([cell == symbol for cell in board[i]]) or all([board[j][i] == symbol for j in range(3)]):
            return True
    if all([board[i][i] == symbol for i in range(3)]) or all([board[i][2 - i] == symbol for i in range(3)]):
        return True
    return False

def board_full(board):
    return all(cell != '-' for row in board for cell in row)

def save_game(board, player_turn, is_vs_ai):
    with open(GAME_STATE_FILE, 'w') as f:
        for row in board:
            f.write(','.join(row) + '\n')
        f.write(f"Player Turn: {player_turn}\n")
        f.write(f"Vs AI: {is_vs_ai}\n")
    print(Fore.YELLOW + "\nGame state saved!\n")

def load_game():
    if not os.path.exists(GAME_STATE_FILE):
        return None, None, None
    with open(GAME_STATE_FILE, 'r') as f:
        lines = f.readlines()
        board = [line.strip().split(',') for line in lines[:3]]
        player_turn = int(lines[3].split(":")[1].strip())
        is_vs_ai = lines[4].split(":")[1].strip().lower() == 'true'
    print(Fore.GREEN + "\nPrevious game loaded!\n")
    return board, player_turn, is_vs_ai

def get_move(board, player):
    while True:
        try:
            move = int(input(f"Player {player}, enter your move (1-9): "))
            if move < 1 or move > 9:
                raise ValueError
            row = (move - 1) // 3
            col = (move - 1) % 3
            if board[row][col] != '-':
                print(Fore.RED + "Cell already taken. Try again.")
            else:
                return row, col
        except ValueError:
            print(Fore.RED + "Invalid input. Enter a number between 1 and 9.")

def minimax(board, depth, is_maximizing, ai_symbol, human_symbol):
    if check_winner(board, ai_symbol):
        return 10 - depth
    elif check_winner(board, human_symbol):
        return depth - 10
    elif board_full(board):
        return 0

    if is_maximizing:
        best = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == '-':
                    board[i][j] = ai_symbol
                    score = minimax(board, depth + 1, False, ai_symbol, human_symbol)
                    board[i][j] = '-'
                    best = max(score, best)
        return best
    else:
        best = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == '-':
                    board[i][j] = human_symbol
                    score = minimax(board, depth + 1, True, ai_symbol, human_symbol)
                    board[i][j] = '-'
                    best = min(score, best)
        return best

def ai_move(board, ai_symbol, human_symbol):
    best_score = -math.inf
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == '-':
                board[i][j] = ai_symbol
                score = minimax(board, 0, False, ai_symbol, human_symbol)
                board[i][j] = '-'
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move

def update_scoreboard(winner):
    if winner:
        with open(SCOREBOARD_FILE, 'a') as f:
            f.write(f"{winner} wins\n")

def display_scoreboard():
    if os.path.exists(SCOREBOARD_FILE):
        print(Fore.CYAN + "\nScoreboard:")
        with open(SCOREBOARD_FILE, 'r') as f:
            scores = f.readlines()
            for score in scores:
                print(score.strip())

def start_game():
    print(Fore.YELLOW + "Welcome to Tic Tac Toe!")
    print("1. Player vs Player")
    print("2. Player vs AI")
    mode = input("Choose mode (1/2): ").strip()
    is_vs_ai = (mode == '2')

    if os.path.exists(GAME_STATE_FILE):
        choice = input("Load previous saved game? (y/n): ").lower()
        if choice == 'y':
            board, player_turn, is_vs_ai = load_game()
            if board is None:
                board = [['-' for _ in range(3)] for _ in range(3)]
                player_turn = 1
        else:
            board = [['-' for _ in range(3)] for _ in range(3)]
            player_turn = 1
    else:
        board = [['-' for _ in range(3)] for _ in range(3)]
        player_turn = 1

    symbols = {1: 'X', 2: 'O'}
    human_symbol = symbols[1]
    ai_symbol = symbols[2]

    while True:
        display_board(board)

        if is_vs_ai and player_turn == 2:
            print("AI is making a move...")
            row, col = ai_move(board, ai_symbol, human_symbol)
        else:
            row, col = get_move(board, player_turn)

        board[row][col] = symbols[player_turn]

        if check_winner(board, symbols[player_turn]):
            display_board(board)
            if is_vs_ai and player_turn == 2:
                print(Fore.RED + "AI wins!")
                update_scoreboard("AI")
            else:
                print(Fore.GREEN + f"Player {player_turn} ({symbols[player_turn]}) wins!")
                update_scoreboard(f"Player {player_turn}")
            os.remove(GAME_STATE_FILE) if os.path.exists(GAME_STATE_FILE) else None
            break

        if board_full(board):
            display_board(board)
            print(Fore.MAGENTA + "It's a draw!")
            update_scoreboard("Draw")
            os.remove(GAME_STATE_FILE) if os.path.exists(GAME_STATE_FILE) else None
            break

        player_turn = 2 if player_turn == 1 else 1

        if not (is_vs_ai and player_turn == 2):
            save = input("Save and exit game? (y/n): ").lower()
            if save == 'y':
                save_game(board, player_turn, is_vs_ai)
                break

    display_scoreboard()

if __name__ == "__main__":
    start_game()
