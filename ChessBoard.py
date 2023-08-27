import pygame as py
import chess

class BoardDisplay():

    def __init__(self, _board):

        # Biến chung
        self.is_run = False
        self.introduce = True
        self.fail = False
        self.dimension = 500
        self.board_position = {}
        self.board_layout = {}
        self.display_eligal_move = []
        self.choose_square = None
        self.square_can_move_2 = None
        self.color_player = None
        self.time = py.time.Clock()
        self.board_state = _board
        self.fen_notation = _board.fen()

        # Input text variables
        self.input_box = py.Rect(160, 460, 200, 32)
        self.color_inactive = py.Color('lightskyblue3')
        self.color_active = py.Color('dodgerblue2')
        self.color = self.color_inactive
        self.active = False
        self.text = ''
        self.font = py.font.init()
        self.font = py.font.Font(None, 32)
        self.elo_text = self.font.render("elo", True, (0, 0, 0))
        self.elo_val = None



        # Tổng hợp pygame ban đầu

        py.init()
        self.window = py.display.set_mode((self.dimension, self.dimension))
        py.display.set_caption("Chess")
        # Tự tạo bề mặt cho bàn cờ
        self.chessBoard = py.image.load("Image/Board.png").convert_alpha()
        self.chessBoard = py.transform.scale(self.chessBoard, (self.dimension, self.dimension))

        self.display_moves_surf = py.Surface((50, 50), py.SRCALPHA, 32)
        py.draw.circle(self.display_moves_surf, (0, 200, 0, 100), (25, 25), 20, 0)

        self.board_layout_init()

        #Thiết lập chỉ được chạy một lần để thiết lập ban đầu
        self.setup_update(self.board_state)


    def board_layout_init(self):

        # Khởi tạo lệnh boardLayout
        for x in range(8):
            for y in range(8):
                # board_position Khởi tạo một lần chỉ lưu dữ liệu tọa độ về vị trí của các khối thực tế
                self.board_position[str(chr(97 + x) + str(y + 1))] = [x * 51.5 + 46, 405 - y * 51]

                # Lưu vị trí trong Ký hiệu Cờ vua nơi đặt các quân cờ khác nhau sẽ thay đổi linh hoạt mỗi nước đi.
                # Điều này chỉ khởi tạo tên của các mục khác nhau trong Từ điển
                self.board_layout[str(chr(97 + x) + str(y + 1))] = None

    def setup_update(self, original_board):
        # Xóa boardLayout Dict để có thể tạo cái mới
        for x in range(8):
            for y in range(8):
                self.board_layout[str(chr(97 + x) + str(y + 1))] = None

        self.board_state = original_board
        self.fen_notation = original_board.fen()

        #Loại bỏ dữ liệu không cần thiết ở cuối chuỗi
        board_string = str(self.fen_notation)[0:str(self.fen_notation).find(' ')]
        board_string = board_string + '/'

        #Thao tác chuỗi cơ bản để xác định vị trí của mọi quân cờ trên bảng
        for y in range(8, 0, -1):
            dash = board_string.find('/')
            rawCode = board_string[0:dash]
            board_string = board_string[dash + 1:len(board_string)]

            alphabet_counter = 97
            for char in rawCode:
                if char.isdigit():
                    alphabet_counter += int(char)
                else:
                    self.board_layout[str(chr(alphabet_counter)) + str(y)] = self.pieceData(char)
                    alphabet_counter +=1
        self.function_update_screen()


    def function_update_screen(self):
        # Chức năng này cập nhật màn hình sẽ được chạy mỗi khi có thay đổi về trạng thái bảng
        self.window.blit(self.chessBoard, (0, 0))
        # Hiển thị tất cả các phần trong BoardLayout
        for num in self.board_layout:
            if self.board_layout[num] != None:
                self.window.blit(self.board_layout[num].render(), (self.board_position[num][0], self.board_position[num][1]))
        # Hiển thị các vòng tròn hiển thị các bước di chuyển có thể
        if self.display_eligal_move != []:
            for num in self.display_eligal_move:
                self.window.blit(self.display_moves_surf, (num[0], num[1]))

        py.display.update()
        self.time.tick(10)

    def update_possible_moves(self):
        # This functions updates where the littler circles appear that show player where certain piece can move
        if self.choose_square != None:
            self.display_eligal_move.clear()
            lg = self.board_state.legal_moves
            for pos in lg:
                if str(pos)[0:2] == self.choose_square:
                    self.display_eligal_move.append((self.board_position[str(pos)[2:4]][0], self.board_position[str(pos)[2:4]][1]))

    def pieceData(self, piece):

        # This class gets referenced when initializing new Pieces using Pieces class
        if piece == 'p': return Piece("Pawn_piece", "B")
        elif piece == 'r': return Piece("Rook_piece", "B")
        elif piece == 'n': return Piece("Knight_piece", "B")
        elif piece == 'b': return Piece("Bishop_piece", "B")
        elif piece == 'k': return Piece("King", "B")
        elif piece == 'q': return Piece("Queen_piece", "B")

        elif piece == 'P': return Piece("Pawn_piece", "W")
        elif piece == 'R': return Piece("Rook_piece", "W")
        elif piece == 'N': return Piece("Knight_piece", "W")
        elif piece == 'B': return Piece("Bishop_piece", "W")
        elif piece == 'K': return Piece("King", "W")
        elif piece == 'Q': return Piece("Queen_piece", "W")


    # If the player Left Click on block the piece on that block is the one to be moved.
    # If there was a piece already selected  the second  click is the block the selected piece should move to.
    # Except if the second click is on a Piece of same cloro then that piece becomes the Pieced to be movesd
    def square_select(self, pos):
        x_board_pos = ((pos[0] - 45) // 50)
        y_board_pos = -((pos[1] - 405) // 50) + 1
        # Set piece to be moved
        if self.choose_square == None:
            self.square_can_move_2 = None
            self.choose_square = str(chr(97 + x_board_pos) + str(y_board_pos))
            self.update_possible_moves()
            return None

        else:
            self.square_can_move_2 = str(chr(97 + x_board_pos) + str(y_board_pos))
            result = str(self.choose_square + self.square_can_move_2)
            for move in self.board_state.legal_moves:
                if str(move) == str(result + "q"):
                    self.remove_square_select()
                    return str(result + "q")
                elif str(move) == result:
                    self.remove_square_select()
                    return result

            if self.board_layout[str(chr(97 + x_board_pos) + str(y_board_pos))] != None:
                self.square_can_move_2 = None
                self.choose_square = str(chr(97 + x_board_pos) + str(y_board_pos))
                self.update_possible_moves()
                return None

    # If RightClick the current selected Piece is set to None.
    def remove_square_select(self):
        self.choose_square = None
        self.square_can_move_2 = None
        self.display_eligal_move = []


############################################################################################################################
# From here is only UI stuff to display menus and click_buttons ect.

    def menu_main(self):

        red = (200, 0, 0)
        color_for_white = (210,220,230)
        color_for_black = (80,130,170)

        background_red = (255, 0, 0)

        while self.introduce:
            for _event in py.event.get():
                # print(_event)
                if _event.type == py.QUIT:
                    py.quit()
                if _event.type == py.MOUSEBUTTONDOWN:
                    if self.input_box.collidepoint(_event.pos):
                        self.active = not self.active
                    else:
                        self.active = False
                    self.color = self.color_active if self.active else self.color_inactive
                if _event.type == py.KEYDOWN:
                    if self.active:
                        if _event.key == py.K_RETURN:
                            # Do something with the input text here
                            self.elo_val = int(self.text)
                            # print(self.text)
                            self.text = ''
                        elif _event.key == py.K_BACKSPACE:
                            self.text = self.text[:-1]
                        else:
                            self.text += _event.unicode
                            
                            
            self.window.fill((255,255,255))
            hello_text = py.font.SysFont("comicsansms", 100)
            text_surf, text_rect = self.text_obj("Play Chess", hello_text)
            text_rect.center = ((self.dimension / 2), (self.dimension / 2 - 100))
            self.window.blit(text_surf, text_rect)


            self.window.blit(self.elo_text, (self.input_box.x - self.elo_text.get_width() - 10, self.input_box.y + 5))
            txt_surface = self.font.render(self.text, True, self.color)
            width = max(200, txt_surface.get_width()+10)
            self.input_box.w = width
            self.window.blit(txt_surface, (self.input_box.x+5, self.input_box.y+5))
            py.draw.rect(self.window, self.color, self.input_box, 2)


            self.click_button("White", 50, 300, 100, 50, color_for_white, color_for_black, 1)
            self.click_button("Black", 350, 300, 100, 50, color_for_black, color_for_white, 2)
            self.click_button("Quit", 225, 400, 80, 50, red, background_red, 3)

            py.display.update()
            self.time.tick(15)

    def game_over_menu(self):

        red = (200, 0, 0)
        green = (0, 200, 0)

        background_red = (255, 0, 0)
        background_green = (0, 255, 0)

        while self.fail:
            for event in py.event.get():
                # print(event)
                if event.type == py.QUIT:
                    py.quit()

            self.window.fill((255,255,255,100))
            largeText = py.font.SysFont("comicsansms", 90)
            mediumText = py.font.SysFont("comicsansms", 50)
            TextSurfMian, TextRectMain = self.text_obj("Game Over", largeText)
            TextRectMain.center = ((self.dimension / 2), (self.dimension / 2 - 120))
            self.window.blit(TextSurfMian, TextRectMain)

            if self.board_state.turn == chess.WHITE:
                TextSurf, TextRect = self.text_obj("Black Won", mediumText)
            else:
                TextSurf, TextRect = self.text_obj("White Won", mediumText)

            TextRect.center = ((self.dimension / 2), (self.dimension / 2) - 20)
            self.window.blit(TextSurf, TextRect)

            self.click_button("Play Again", 225, 300, 100, 50, green, background_green, 4)
            self.click_button("Quit", 225, 400, 100, 50, red, background_red, 3)

            py.display.update()
            self.time.tick(15)

    def click_button(self, message, x, y, w, h, ic, ac, action=None):
        mouse_event = py.mouse.get_pos()
        click = py.mouse.get_pressed()
        if x + w > mouse_event[0] > x and y + h > mouse_event[1] > y:
            py.draw.rect(self.window, ac, (x, y, w, h))

            if click[0] == 1 and action != None:
                if action == 1:
                    self.color_player = "W"
                    self.is_run = True
                    self.introduce = False
                    self.fail = False
                elif action == 2:
                    self.color_player = "B"
                    self.is_run = True
                    self.introduce = False
                    self.fail = False
                elif action == 3:
                    py.quit()
                elif action == 4:
                    self.is_run = False
                    self.introduce = True
                    self.fail = False

        else:
            py.draw.rect(self.window, ic, (x, y, w, h))

        smallText = py.font.SysFont("comicsansms", 20)
        text_surf, text_rect = self.text_obj(message, smallText)
        text_rect.center = ((x + (w / 2)), (y + (h / 2)))
        self.window.blit(text_surf, text_rect)

    def text_obj(self, text, font):
        text_surface = font.render(text, True, (0,0,0))
        return text_surface, text_surface.get_rect()

# This class is used to create Pieces and assign a Surface and Image to them
class Piece():

    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.dimension = 45

        if (self.color == "W") or (self.color == "White"):
            if self.name != "Knight_piece":
                self.pieceSurface = py.image.load("Image/Chess_"+self.name.lower()[0]+"lt60.png")
            else:
                self.pieceSurface = py.image.load("Image/Chess_nlt60.png")
        else:
            if self.name != "Knight_piece":
                self.pieceSurface = py.image.load("Image/Chess_" + self.name.lower()[0] + "dt60.png")
            else:
                self.pieceSurface = py.image.load("Image/Chess_ndt60.png")

        self.pieceSurface = py.transform.scale(self.pieceSurface, (self.dimension, self.dimension))


    def render(self):
        return self.pieceSurface
