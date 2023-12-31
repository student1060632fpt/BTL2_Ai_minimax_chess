from ChessBoard import BoardDisplay
from MiniMax import minimax_algorithm
from Evaluation import Evalualtion
import chess
import pygame as py
from CalElo import CalElo

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
                make_move_black(player_possible_move, is_late_game)
            else:
                make_move_black(player_possible_move, is_late_game)
                make_white_move(player_possible_move, is_late_game)
        except:
            print("Invalid Move")

def make_white_move(move, state_is_late_game):

    if board_display.color_player == "W":
        chess_board.push_uci(move)
    else:
        # Thuộc tính deep_tree phải là số lẻ
        if state_is_late_game:
            white = minimax_algorithm(depth_tree + 1, True, MIN_INPUT, MAX_INPUT, chess_board, True)
        else:
            white = minimax_algorithm(depth_tree + 1, True, MIN_INPUT, MAX_INPUT, chess_board, True)

        chess_board.push(white)

    board_display.setup_update(chess_board)

def make_move_black(move, state_is_late_game):

    if board_display.color_player == "B":
        chess_board.push_uci(move)
    else:
        # The depth_tree attribute has to be even
        if state_is_late_game:
            black = minimax_algorithm(depth_tree + 2, False, MIN_INPUT, MAX_INPUT, chess_board, True)
        else:
            black = minimax_algorithm(depth_tree, False, MIN_INPUT, MAX_INPUT, chess_board, True)
        chess_board.push(black)

    board_display.setup_update(chess_board)

def is_game_over(chess_board):
    if chess_board.is_game_over():
        if chess_board.turn == chess.WHITE:
            if board_display.player_color == "W":
                d = 2
            else:
                d = 1
        else: #den thang
            if board_display.player_color == "W":
                d = 1
            else:
                d = 2
        # else:
        #     d = 2
        with open('elo.txt', 'r') as file:
            bot = file.read()
            bot = int(bot)  # Đọc nội dung của tệp và lưu vào biến content
        print(bot)
        gess = board_display.elo_val
        print(gess)

        elo_new = CalElo(bot,gess,30,d)
        elo_new.EloRating()

        with open("elo.txt", "w") as file:
            file.write(str(int(round(elo_new.Ra))))
        print ("ok")

        board_display.run = False
        board_display.game_over = True
        board_display.game_over_menu()

def run_game():

    if board_display.color_player == "B":
        make_white_move(None, False)

    while board_display.is_run:
        events = py.event.get()
        for event_mouse in events:
            if event_mouse.type == py.QUIT:
                exit()

            if event_mouse.type == py.MOUSEBUTTONDOWN and event_mouse.button == 1:
                move()
            elif event_mouse.type == py.MOUSEBUTTONDOWN and event_mouse.button == 3:
                board_display.remove_square_select()

        board_display.function_update_screen()
        is_game_over(chess_board)

while run_game:
    setup_game()

py.quit()


