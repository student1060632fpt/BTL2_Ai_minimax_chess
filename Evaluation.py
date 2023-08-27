from Piece_Development_Values import ValuesBoard

class Evalualtion():

    def __init__(self, _board, _color):
        self.state_board = _board
        self.color_type = _color
        self.values_board = ValuesBoard()
        self.late_game_white = False
        self.late_game_black = False

        #Tạo danh sách BoardLayout trống từ đó có thể thực hiện so sánh.
        self.layout_board = [None] * 64

        # Trên thực tế, hãy điền board_layout với dữ liệu từ board_string.
        self.list_position_of_piece()

    def list_position_of_piece(self):

        board_string = self.state_board.fen()

        # Loại bỏ dữ liệu không cần thiết ở cuối chuỗi
        board_string = board_string[0:board_string.find(' ')]
        board_string = board_string + '/'

        # Thao tác chuỗi cơ bản để xác định vị trí của mọi quân cờ trên bảng
        num_counter = 0

        for y in range(8):
            dashes = board_string.find('/')
            raw_code = board_string[0:dashes]
            board_string = board_string[dashes + 1:len(board_string)]

            for character in raw_code:
                if character.isdigit():
                    num_counter += int(character)
                else:
                    self.layout_board[num_counter] = character
                    num_counter += 1

    def material_comp(self):
        total_point = 0
        board_string = self.state_board.fen()

        # Loại bỏ dữ liệu không cần thiết ở cuối chuỗi
        board_string = board_string[0:board_string.find(' ')]

        # Thao tác chuỗi cơ bản để xác định vị trí của mọi quân cờ trên bảng
        for i in board_string:
            if str(i) == "P": total_point += 100
            elif str(i) == "N": total_point += 320
            elif str(i) == "B": total_point += 330
            elif str(i) == "R": total_point += 500
            elif str(i) == "Q": total_point += 900
            elif str(i) == "K": total_point += 20000

            elif str(i) == "p": total_point -= 100
            elif str(i) == "n": total_point -= 320
            elif str(i) == "b": total_point -= 330
            elif str(i) == "r": total_point -= 500
            elif str(i) == "q": total_point -= 900
            elif str(i) == "k": total_point -= 20000
            else: pass

        return total_point

    def develope(self):
        total_point = 0
        num_counter = 0
        # GamePos xác định việc sớm hay muộn trận đấu sẽ quyết định mức độ hung hãn của nhà vua.
        # 1 nghĩa là Trò chơi muộn và 0 nghĩa là Trò chơi sớm đến giữa.

        number_of_minor_pieces_white = 0
        number_of_minor_pieces_black = 0

        for piece_val in self.layout_board:
            if piece_val != None:
                if str(piece_val) == "P":
                    total_point += self.values_board.Pawn_piece[-(num_counter-63)]
                elif str(piece_val) == "N":
                    total_point += self.values_board.Knight_piece[-(num_counter-63)]
                    number_of_minor_pieces_white += 1
                elif str(piece_val) == "B":
                    total_point += self.values_board.Bishop_piece[-(num_counter-63)]
                    number_of_minor_pieces_white += 1
                elif str(piece_val) == "R":
                    total_point += self.values_board.Rook_piece[-(num_counter-63)]
                    number_of_minor_pieces_white += 1
                elif str(piece_val) == "Q":
                    total_point += self.values_board.Queen_piece[-(num_counter-63)]
                    number_of_minor_pieces_white += 1

                #######################################################################

                elif str(piece_val) == "p":
                    total_point -= self.values_board.Pawn_piece[num_counter]
                elif str(piece_val) == "n":
                    total_point += self.values_board.Knight_piece[num_counter]
                    number_of_minor_pieces_black += 1
                elif str(piece_val) == "b":
                    total_point += self.values_board.Bishop_piece[num_counter]
                    number_of_minor_pieces_black += 1
                elif str(piece_val) == "r":
                    total_point += self.values_board.Rook_piece[num_counter]
                    number_of_minor_pieces_black += 1
                elif str(piece_val) == "q":
                    total_point += self.values_board.Queen_piece[num_counter]
                    number_of_minor_pieces_black += 1

            num_counter += 1

        num_counter = 0
        for piece_val in self.layout_board:
            if piece_val != None:
                # Nếu đúng thì đó vẫn là trò chơi đầu.
                if str(piece_val) == "k":
                    if (number_of_minor_pieces_black >= 3):
                        total_point += self.values_board.King_early[num_counter]
                    else:
                        total_point += self.values_board.King_late[num_counter]
                        self.late_game_black = True
                        print("Black Late")

                # Nếu đúng thì đó vẫn là trò chơi đầu.
                elif str(piece_val) == "K":
                    if (number_of_minor_pieces_white >= 3):
                        total_point += self.values_board.King_early[-(num_counter - 63)]
                    else:
                        total_point += self.values_board.King_late[-(num_counter - 63)]
                        self.late_game_white = True

            num_counter += 1

        return total_point

    def checkmate(self):

        total_point = 0

        if self.state_board.is_checkmate:
            if self.color_type == "W":
                total_point += 50000
            else:
                total_point -= 50000

        return total_point

    def is_late_game(self):
        self.develope()
        if (self.late_game_black) and (self.late_game_white):
            return True
        else:
            return False

    def result(self):
        total_point = 0

        #1 Material Comp đưa ra giá trị int cho bảng tùy theo những phần còn lại trên bảng
        total_point += self.material_comp()

        #2 Develompent cung cấp int val cho bảng tùy theo vị trí của các phần trên bảng sử dụng Piece_Development_Values.py
        total_point += self.develope()

        #3 Cung cấp giá trị int nếu nước đi hiện tại có thể đưa người chơi đối diện vào thế chiếu tướng
        total_point += self.checkmate()

        return total_point

