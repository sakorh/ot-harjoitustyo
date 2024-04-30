import pygame
from sprites.pawn import Pawn
from sprites.rook import Rook
from sprites.knight import Knight
from sprites.bishop import Bishop
from sprites.king import King
from sprites.queen import Queen


class Board:
    def __init__(self, empty_board, square_size, pieces):
        self.empty_board = empty_board
        self.square_size = square_size
        self._pieces = pieces
        self.pawns = pygame.sprite.Group()
        self.bishops = pygame.sprite.Group()
        self.rooks = pygame.sprite.Group()
        self.knights = pygame.sprite.Group()
        self.queens = pygame.sprite.Group()
        self.kings = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.new_game = None
        self.begin = True
        self._fen_pieces = []
        self.user_text = ""
        self.fen = None
        self.input_fen = False

    def board_to_fen(self, turn, name):
        """Palauttaa FEN-notaation sen hetkisestä pelilaudan asetelmasta ja lisää sen dropdown-valikon
        vaihtoehtoihin.
        """
        fen = ""
        empty_squares = 0
        for y in range(8):
            for x in range(8):
                piece_in_square = False
                for piece in self.all_sprites:
                    pos_x = piece.rect.x // self.square_size
                    pos_y = piece.rect.y // self.square_size
                    if (x, y) == (pos_x, pos_y):
                        piece_in_square = True
                        if empty_squares:
                            fen += str(empty_squares)
                            empty_squares = 0
                        if piece in self.pawns and piece.color == "black":
                            fen += "p"
                        elif piece in self.pawns and piece.color == "white":
                            fen += "P"
                        elif piece in self.rooks and piece.color == "black":
                            fen += "r"
                        elif piece in self.rooks and piece.color == "white":
                            fen += "R"
                        elif piece in self.knights and piece.color == "black":
                            fen += "n"
                        elif piece in self.knights and piece.color == "white":
                            fen += "N"
                        elif piece in self.bishops and piece.color == "black":
                            fen += "b"
                        elif piece in self.bishops and piece.color == "white":
                            fen += "B"
                        elif piece in self.queens and piece.color == "black":
                            fen += "q"
                        elif piece in self.queens and piece.color == "white":
                            fen += "Q"
                        elif piece in self.kings and piece.color == "black":
                            fen += "k"
                        elif piece in self.kings and piece.color == "white":
                            fen += "K"
                if not piece_in_square:
                    empty_squares += 1
            if empty_squares:
                fen += str(empty_squares)
                empty_squares = 0
            if y < 7:
                fen += "/"

        if turn == "white":
            fen += " w"
        else:
            fen += " b"

        return fen

    def draw_pieces_from_fen(self):
        """Alustaa pelilaudan annetusta FEN-asetelmasta.
        """
        fen = self.user_text
        fen = fen.replace("\n", "")
        fen = fen.split(" ")
        pieces = fen[0]
        turn = fen[1]
        rows = pieces.split("/")
        board = []
        pieces_encoding = {"p": 1, "P": 0, "r": 7, "R": 6, "n": 3,
                           "N": 2, "b": 5, "B": 4, "q": 9, "Q": 8, "k": 11, "K": 10}

        for row in rows:
            pieces_in_row = []
            for piece in row:
                if piece.isdigit():
                    for _ in range(int(piece)):
                        pieces_in_row.append(-1)
                else:
                    pieces_in_row.append(pieces_encoding[piece])
            board.append(pieces_in_row)

        self._fen_pieces = board
        self.input_fen = False
        self.start_game()
        if turn == "w":
            return "white"
        return "black"

    def load_fen_view(self, display):
        base_font = pygame.font.Font(None, 32)
        x = y = 8*self.square_size
        self.input_fen_rect = pygame.Rect(200, 200, 7*self.square_size, 40)
        self.input_fen_rect.center = (x // 2, y // 2)
        color = (0, 255, 0)
        green = (0, 255, 0)
        pygame.draw.rect(display, color, self.input_fen_rect)
        text_surface = base_font.render(self.user_text, True, (255, 255, 255))
        display.blit(text_surface, (self.input_fen_rect.x +
                     5, self.input_fen_rect.y+5))
        self.input_fen_rect.w = max(100, text_surface.get_width()+10)
        black = (0, 0, 0)
        font = pygame.font.Font('freesansbold.ttf', 32)
        fen_text = font.render('Load FEN', True, green, black)
        x = y = 8*self.square_size
        self.fen.center = (x // 2, 2*self.square_size)
        display.blit(fen_text, self.fen)

    def _draw_load_fen_text(self, display, font):
        green = (0, 255, 0)
        black = (0, 0, 0)
        fen_text = font.render('Load FEN', True, green, black)
        self.fen = fen_text.get_rect()
        x = y = 8*self.square_size
        self.fen.center = (x // 2, y // 2)
        display.blit(fen_text, self.fen)

    def _draw_new_game_text(self, display, font, text):
        green = (0, 255, 0)
        black = (0, 0, 0)
        x = y = 8*self.square_size
        new_game_text = font.render(text, True, green, black)
        self.new_game = new_game_text.get_rect()
        self.new_game.center = (x // 2, 3*self.square_size)
        display.blit(new_game_text, self.new_game)
        pygame.draw.rect(display, (0, 255, 0), self.new_game, 4)

    def begin_view(self, display):
        font = pygame.font.Font('freesansbold.ttf', 32)
        self._draw_load_fen_text(display, font)
        self._draw_new_game_text(display, font, "Start Game")

    def end_game(self, display):
        self._kill_all_sprites()
        self._fen_pieces.clear()
        green = (0, 255, 0)
        black = (0, 0, 0)
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('Game Over', True, green, black)
        text_rect = text.get_rect()
        x = 8*self.square_size
        text_rect.center = (x // 2, 2.5*self.square_size)
        display.blit(text, text_rect)
        self._draw_new_game_text(display, font, "Start New Game")

    def start_game(self):
        self.begin = False
        self._kill_all_sprites()
        self._initialize_pieces()

    def _initialize_pieces(self):
        if self._fen_pieces:
            pieces = self._fen_pieces
        else:
            pieces = self._pieces
        for y in range(8):
            for x in range(8):
                square = pieces[y][x]
                normalized_x = x*self.square_size
                normalized_y = y*self.square_size

                if square == 1:
                    self.pawns.add(Pawn("black", self.square_size,
                                        normalized_x, normalized_y))
                elif square == 0:
                    self.pawns.add(Pawn("white", self.square_size,
                                        normalized_x, normalized_y))
                elif square == 7:
                    self.rooks.add(Rook("black", self.square_size,
                                        normalized_x, normalized_y))
                elif square == 6:
                    self.rooks.add(Rook("white", self.square_size,
                                        normalized_x, normalized_y))
                elif square == 3:
                    self.knights.add(
                        Knight("black", self.square_size, normalized_x, normalized_y))
                elif square == 2:
                    self.knights.add(
                        Knight("white", self.square_size, normalized_x, normalized_y))
                elif square == 5:
                    self.bishops.add(Bishop("black", self.square_size,
                                            normalized_x, normalized_y))
                elif square == 4:
                    self.bishops.add(Bishop("white", self.square_size,
                                            normalized_x, normalized_y))
                elif square == 9:
                    self.queens.add(Queen("black", self.square_size,
                                          normalized_x, normalized_y))
                elif square == 11:
                    self.kings.add(King("black", self.square_size,
                                        normalized_x, normalized_y))
                elif square == 8:
                    self.queens.add(Queen("white", self.square_size,
                                          normalized_x, normalized_y))
                elif square == 10:
                    self.kings.add(King("white", self.square_size,
                                        normalized_x, normalized_y))
        self.all_sprites.add(self.pawns, self.rooks, self.knights,
                             self.bishops, self.queens, self.kings)

    def _kill_all_sprites(self):
        """Poistaa kaikki nappulat.
        """
        for sprite in self.all_sprites:
            sprite.kill()

    def draw_options(self, display, options):
        """Piirtää valitun nappulan siirtovaihtoehdot pelilaudalle.
        """
        for option in options:
            pygame.draw.circle(display, (0, 255, 0),
                               (option[0]+self.square_size//2, option[1]+self.square_size//2), 5)

    def draw_current_square(self, display, x, y):
        pygame.draw.rect(display, (0, 255, 0), (
            x, y, self.square_size, self.square_size), 4)

    def initialize_board(self, display, board):
        height = width = len(board)
        black = (100, 100, 100)
        white = (255, 255, 255)

        for y in range(height):
            for x in range(width):
                square = board[y][x]
                normalized_x = x*self.square_size
                normalized_y = y*self.square_size

                if square == 0:
                    pygame.draw.rect(
                        display, white, (normalized_x, normalized_y,
                                         self.square_size, self.square_size))
                elif square == 1:
                    pygame.draw.rect(
                        display, black, (normalized_x, normalized_y,
                                         self.square_size, self.square_size))
