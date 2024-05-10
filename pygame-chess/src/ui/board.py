import pygame
from sprites.pawn import Pawn
from sprites.rook import Rook
from sprites.knight import Knight
from sprites.bishop import Bishop
from sprites.king import King
from sprites.queen import Queen


class Board:
    """Nappuloiden luomisesta ja sovelluksen eri näkymien/nappuloiden piirtämisestä vastaava luokka.
    """

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
        self.error_message = ""
        self.new_game = None
        self.begin = True
        self._fen_pieces = []
        self.user_text = ""
        self.fen = None
        self.input_fen = False
        self.input_name = False
        self.save_board = None
        self.choose_fen = None
        self.fens = []
        self.fen_options = []
        self.load_more = None
        self.previous = None
        self.fens_page = 0
        self._green = (0, 255, 0)
        self._black = (0, 0, 0)

    def board_to_fen(self, turn):
        """Palauttaa FEN-notaation sen hetkisestä pelilaudan asetelmasta ja lisää sen pelin alkunäkymän
        Choose FEN -valikon vaihtoehtoihin.

        Args:
            turn: merkkijonoarvo, joka kertoo, kenen pelaajan vuoroon tallennettava asetelma jäi.

        Returns:
            Palauttaa pelilaudan asetelman FEN-merkkijonona.
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

        self.error_message = ""
        if turn == "white":
            fen += " w"
        else:
            fen += " b"

        return fen

    def draw_pieces_from_fen(self, fen=None):
        """Alustaa pelilaudan annetusta FEN-asetelmasta.

        Args:
            fen:
                Vapaaehtoinen, oletusarvona None.
                Merkkijonoarvo, joka sisältää FEN-asetelman, jonka mukaan pelilauta alustetaan.

        Returns:
            None, jos annettu asetelma ei ole kirjoitettu oikein.
            Muutoin palauttaa merkkijonoarvon, joka kertoo, kenen vuorolla pelaaminen asetelmasta aloitetaan.
        """
        if not fen:
            fen = self.user_text
        try:
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

        except:
            self.error_message = "Incorrect notation. Try again."
            return None

        self._fen_pieces = board
        self.input_fen = False
        self.error_message = ""
        self.user_text = ""
        self.start_game()
        if turn == "w":
            return "white"
        return "black"

    def load_fen_view(self, display):
        """Piirtää näkymän, jossa pelaaja voi syöttää oman FEN-asetelmansa.

        Args:
            display: pygame-elementti, jonka sisälle pelilauta piirretään.
        """
        if self.error_message != "Incorrect notation. Try again.":
            self.error_message = ""
        base_font = pygame.font.Font(None, 32)
        x = y = 8*self.square_size
        input_fen_rect = pygame.Rect(200, 200, 7*self.square_size, 40)
        input_fen_rect.center = (x // 2, y // 2)
        pygame.draw.rect(display, self._green, input_fen_rect)
        text_surface = base_font.render(self.user_text, True, (255, 255, 255))
        display.blit(text_surface, (input_fen_rect.x +
                     5, input_fen_rect.y+5))
        input_fen_rect.w = max(100, text_surface.get_width()+10)
        self._draw_load_fen_text(display, x // 2, 5*self.square_size // 2, 32)
        self._draw_new_game_text(
            display, "Go Back", 2*self.square_size, self.square_size, 32)

    def load_name_view(self, display):
        """Piirtää näkymän, jossa pelaaja voi syöttää tallennettavalle asetelmalle nimen.

        Args:
            display: pygame-elementti, jonka sisälle pelilauta piirretään.
        """
        font = pygame.font.Font('freesansbold.ttf', 22)
        base_font = pygame.font.Font(None, 32)
        x = 18*self.square_size
        y = 3*self.square_size
        x = y = 8*self.square_size
        enter_name_text = font.render(
            "Enter a name (max 50 characters):", True, self._green, self._black)
        enter_name_rect = enter_name_text.get_rect()
        enter_name_rect.center = (8*self.square_size // 2, 3*self.square_size)
        display.blit(enter_name_text, enter_name_rect)
        input_name_rect = pygame.Rect(200, 200, 7*self.square_size, 40)
        input_name_rect.center = (x // 2, y // 2)
        pygame.draw.rect(display, self._green, input_name_rect)
        text_surface = base_font.render(self.user_text, True, (255, 255, 255))
        display.blit(text_surface, (input_name_rect.x +
                     5, input_name_rect.y+5))
        input_name_rect.w = max(100, text_surface.get_width()+10)

    def _draw_load_fen_text(self, display, x, y, font_size):
        """Piirtää nappulan Load FEN -tekstillä.
        """
        font = pygame.font.Font('freesansbold.ttf', font_size)
        fen_text = font.render(
            'Load FEN', True, self._green, self._black)
        self.fen = fen_text.get_rect()
        self.fen.center = (x, y)
        display.blit(fen_text, self.fen)

    def _draw_new_game_text(self, display, text, x, y, font_size):
        """Piirtää nappulan, jota klikkaamalla voi aloittaa uuden pelin.
        """
        font = pygame.font.Font('freesansbold.ttf', font_size)
        new_game_text = font.render(text, True, self._green, self._black)
        self.new_game = new_game_text.get_rect()
        self.new_game.center = (x // 2, y)
        display.blit(new_game_text, self.new_game)

    def _draw_choose_fen_text(self, display, x, y, font_size):
        """Piirtää nappulan, jota klikkaamalla saa näkyviin tietokantaan tallennetut asetelmat.
        """
        font = pygame.font.Font('freesansbold.ttf', font_size)
        choose_fen_text = font.render(
            "Choose FEN", True, self._green, self._black)
        self.choose_fen = choose_fen_text.get_rect()
        self.choose_fen.center = (x // 2, y)
        display.blit(choose_fen_text, self.choose_fen)

    def choose_fen_view(self, display):
        """Piirtää näkymän, jossa näkyy aina neljä tietokannasta haettua asetelmaa kerrallaan.
        Jos asetelmia on enemmän kuin neljä, tulee näkyviin Load More -nappi, jota painamalla saa yhden
        uuden asetelman näkyviin. Jos asetelmissa on liikkunut Load More -napilla eteenpäin, tulee näkyviin
        myös Load Previous -nappi, jota painamalla voi palata aiemmin näytettyihin asetelmiin yksi kerrallaan.
        Näkymien nimien viereen piirretään myös Delete -nappi, jota painamalla asetelman voi poistaa tietokannasta.
        """
        font = pygame.font.Font('freesansbold.ttf', 24)
        idx = self.fens_page
        self.fen_options = []
        x = 8*self.square_size
        if self.fens_page > 0 and len(self.fens) > 4:
            previous_text = font.render(
                "Load Previous", True, (255, 255, 0), self._black)
            self.previous = previous_text.get_rect()
            self.previous.midright = self.load_more.midleft
            display.blit(previous_text, self.previous)
        if len(self.fens[idx:]) > 4:
            fens = self.fens[idx:idx+4]
            load_more_text = font.render(
                "Load More", True, (255, 255, 0), self._black)
            self.load_more = load_more_text.get_rect()
            self.load_more.midleft = (x // 2, 7.5*self.square_size)
            display.blit(load_more_text, self.load_more)
        else:
            fens = self.fens[idx:]
        for fen in fens:
            fen_text = font.render(fen, True, self._green, self._black)
            fen_text_rect = fen_text.get_rect()
            fen_text_rect.center = (
                x // 2, 5.5*self.square_size+len(self.fen_options)*0.5*self.square_size)
            delete_text = font.render(
                "Delete", True, (255, 0, 0), self._black)
            delete_text_rect = delete_text.get_rect()
            delete_text_rect.topleft = fen_text_rect.topright
            self.fen_options.append((fen_text_rect, fen, delete_text_rect))
            display.blit(fen_text, fen_text_rect)
            display.blit(delete_text, delete_text_rect)

    def begin_view(self, display):
        """Piirtää sovelluksen alkunäkymän.
        """
        if self.error_message != "You have no FENs saved.":
            self.error_message = ""
        self._kill_all_sprites()
        self._fen_pieces.clear()
        self.fen_options.clear()
        self.input_name = False
        x = 8*self.square_size
        y = 2.5*self.square_size
        self._draw_new_game_text(display, "Start Game", x, y, 32)
        self._draw_load_fen_text(display, x // 2, 3.5*self.square_size, 32)
        self._draw_choose_fen_text(display, x, 4.5*self.square_size, 32)

    def end_game(self, display):
        """Piirtää pelin päättymisnäkymän.
        """
        font = pygame.font.Font('freesansbold.ttf', 32)
        self._kill_all_sprites()
        self._fen_pieces.clear()
        text = font.render('Game Over', True, self._green, self._black)
        text_rect = text.get_rect()
        x = 8*self.square_size
        y = 2.5*self.square_size
        text_rect.center = (x // 2, y)
        display.blit(text, text_rect)
        self._draw_new_game_text(
            display, "Start New Game", x, 3.5*self.square_size, 32)
        self._draw_choose_fen_text(display, x, 4.5*self.square_size, 32)

    def _draw_save_board_text(self, display, text, x, y, font_size):
        """Piirtää Save Board -tekstin, jota klikkaamalla voi tallentaa pelilaudan asetelman.
        """
        font = pygame.font.Font('freesansbold.ttf', font_size)
        save_board_text = font.render(
            text, True, self._green, self._black)
        self.save_board = save_board_text.get_rect()
        self.save_board.center = (x // 2, y)
        display.blit(save_board_text, self.save_board)

    def draw_error_message(self, display):
        """Piirtää virheilmoituksen.

        Args:
            display: pygame-elementti, jonka sisälle pelilauta piirretään.
        """
        font = pygame.font.Font('freesansbold.ttf', 24)
        error_text = font.render(
            self.error_message, True, (255, 0, 0), self._black)
        error_text_rect = error_text.get_rect()
        error_text_rect.center = (
            8*self.square_size // 2, 5.5*self.square_size)
        display.blit(error_text, error_text_rect)

    def game_view(self, display):
        """Kutsuu pelilaudan vierelle piirrettävien nappuloiden, joista voi palata takaisin alkunäkymään tai tallentaa
        pelilaudan asetelman, metodeja.

        Args:
            display: pygame-elementti, jonka sisälle pelilauta piirretään.
        """
        self._draw_save_board_text(
            display, "Save Board", 18*self.square_size, 2.5*self.square_size, 22)
        self._draw_new_game_text(
            display, "Start New Game", 18*self.square_size, 2*self.square_size, 22)

    def start_game(self):
        """Poistaa kaikki mahdolliset edellisen pelin nappulat ja virheilmoitukset, peruuttaa mahdolliset 
        pelaajan syötteiden perusteella tehdyt alkunäkymän muutokset ja kutsuu metodia, joka luo uudet nappulat.
        """
        self.error_message = ""
        self.begin = False
        self.input_fen = False
        self._kill_all_sprites()
        self._initialize_pieces()
        self.fen_options.clear()
        self.fens.clear()
        self.fens_page = 0

    def _initialize_pieces(self):
        """Alustaa pelin nappulat joko normaalin shakin aloitusasetelmaan, tai pelaajan syöttämään/valitsemaan
        asetelmaan.
        """
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

        Args:
            display: pygame-elementti, jonka sisälle näkymä piirretään.
            options: valitun nappulan siirtovaihtoehdot.
        """
        for option in options:
            pygame.draw.circle(display, (0, 255, 0),
                               (option[0]+self.square_size//2, option[1]+self.square_size//2), 5)

    def draw_current_square(self, display, x, y):
        """Piirtää vihreät reunat sen ruudun ympärille, jossa pelaaja on näppäimistöllä liikkuessa,
        tai jota pelaaja on klikannut viimeksi hiirellä.

        Args:
            display: pygame-elementti, jonka sisälle näkymä piirretään.
            x,y: pelaajan koordinaatit.
        """
        pygame.draw.rect(display, (0, 255, 0), (
            x, y, self.square_size, self.square_size), 4)

    def initialize_board(self, display, board):
        """Piirtää tyhjän pelilaudan.

        Args:
            display: pygame-elementti, jonka sisälle pelilauta piirretään.
            board: tyhjä pelilauta, jonka pohjalta ruutujen värit valitaan.
        """
        display.fill((0, 0, 0))
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
