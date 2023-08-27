from ChessBoard import BoardDisplay
from MiniMax import minimax
from Evaluation import Evalualtion
import chess
import pygame as py

# General variables
MAX_INPUT, MIN_INPUT = 100000, -100000
depth_tree = 4

chess_board = chess.Board()
board_display = BoardDisplay(chess_board)

# Tis function can be run at anytime and wit completely reset the game.
def game_setup():
    chess_board.reset_board()
    board_display.main_menu()
    board_display.update(chess_board)
    run_game()

def move():
    player_possible_move = board_display.square_select(py.mouse.get_pos())
    if player_possible_move != None:
        try:
            eval = Evalualtion(chess_board, board_display.player_color)
            is_late_game = eval.is_late_game()

            if board_display.player_color == "W":
                makeMoveWhite(player_possible_move, is_late_game)
                makeMoveBlack(player_possible_move, is_late_game)
            else:
                makeMoveBlack(player_possible_move, is_late_game)
                makeMoveWhite(player_possible_move, is_late_game)
        except:
            print("Invalid Move")

def makeMoveWhite(move, is_late_game):

    if board_display.player_color == "W":
        chess_board.push_uci(move)
    else:
        # The depth_tree attribute has to be odd
        if is_late_game:
            white = minimax(depth_tree + 1, True, MIN_INPUT, MAX_INPUT, chess_board, True)
        else:
            white = minimax(depth_tree + 1, True, MIN_INPUT, MAX_INPUT, chess_board, True)

        chess_board.push(white)

    board_display.update(chess_board)

def makeMoveBlack(move, is_late_game):

    if board_display.player_color == "B":
        chess_board.push_uci(move)
    else:
        # The depth_tree attribute has to be even
        if is_late_game:
            black = minimax(depth_tree + 2, False, MIN_INPUT, MAX_INPUT, chess_board, True)
        else:
            black = minimax(depth_tree, False, MIN_INPUT, MAX_INPUT, chess_board, True)
        chess_board.push(black)

    board_display.update(chess_board)

def is_game_over(chess_board):
    if chess_board.is_game_over():
        board_display.is_run = False
        board_display.fail = True
        board_display.game_over_menu()

def run_game():

    if board_display.player_color == "B":
        makeMoveWhite(None, False)

    while board_display.is_run:
        events = py.event.get()
        for event in events:
            if event.type == py.QUIT:
                exit()

            if event.type == py.MOUSEBUTTONDOWN and event.button == 1:
                move()
            elif event.type == py.MOUSEBUTTONDOWN and event.button == 3:
                board_display.remove_square_select()

        board_display.update_screen()
        is_game_over(chess_board)

while run:
    game_setup()

py.quit()


