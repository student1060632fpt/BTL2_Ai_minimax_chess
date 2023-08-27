from ChessBoard import BoardDisplay
from MiniMax import minimax
from Evaluation import Evalualtion
import chess
import pygame as py

# Biến chung
MAX_INPUT, MIN_INPUT = 100000, -100000
depth_tree = 4

chess_board = chess.Board()
board_display = BoardDisplay(chess_board)

# Chức năng này có thể được chạy bất cứ lúc nào và có thể thiết lập lại hoàn toàn trò chơi.
def setup_game():
    chess_board.reset_board()
    board_display.menu_main()
    board_display.setup_update(chess_board)
    run_game()

def move():
    player_possible_move = board_display.square_select(py.mouse.get_pos())
    if player_possible_move != None:
        try:
            eval = Evalualtion(chess_board, board_display.color_player)
            is_late_game = eval.is_late_game()

            if board_display.color_player == "W":
                make_white_move(player_possible_move, is_late_game)
                makeMoveBlack(player_possible_move, is_late_game)
            else:
                makeMoveBlack(player_possible_move, is_late_game)
                make_white_move(player_possible_move, is_late_game)
        except:
            print("Invalid Move")

def make_white_move(move, state_is_late_game):

    if board_display.color_player == "W":
        chess_board.push_uci(move)
    else:
        # Thuộc tính deep_tree phải là số lẻ
        if state_is_late_game:
            white = minimax(depth_tree + 1, True, MIN_INPUT, MAX_INPUT, chess_board, True)
        else:
            white = minimax(depth_tree + 1, True, MIN_INPUT, MAX_INPUT, chess_board, True)

        chess_board.push(white)

    board_display.setup_update(chess_board)

def makeMoveBlack(move, state_is_late_game):

    if board_display.color_player == "B":
        chess_board.push_uci(move)
    else:
        # The depth_tree attribute has to be even
        if state_is_late_game:
            black = minimax(depth_tree + 2, False, MIN_INPUT, MAX_INPUT, chess_board, True)
        else:
            black = minimax(depth_tree, False, MIN_INPUT, MAX_INPUT, chess_board, True)
        chess_board.push(black)

    board_display.setup_update(chess_board)

def is_game_over(chess_board):
    if chess_board.is_game_over():
        board_display.is_run = False
        board_display.fail = True
        board_display.game_over_menu()

def run_game():

    if board_display.color_player == "B":
        make_white_move(None, False)

    while board_display.is_run:
        events = py.event.get()
        for event in events:
            if event.type == py.QUIT:
                exit()

            if event.type == py.MOUSEBUTTONDOWN and event.button == 1:
                move()
            elif event.type == py.MOUSEBUTTONDOWN and event.button == 3:
                board_display.remove_square_select()

        board_display.function_update_screen()
        is_game_over(chess_board)

while run_game:
    setup_game()

py.quit()


