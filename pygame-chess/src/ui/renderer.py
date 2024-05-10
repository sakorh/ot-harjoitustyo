import pygame


class Renderer:
    """Pelinäkymän päivittämisestä vastaava luokka.
    """

    def __init__(self, display, board):
        """Luokan konstruktori.
        """
        self._display = display
        self._board = board

    def render(self, options, game_over, x, y):
        """Kutsuu Board-luokan eri näkymiä piirtäviä metodeja pelaajan syötteiden mukaan.

        Args:
            options: kullakin hetkellä valittuna olevan nappulan siirtovaihtoehdot.
            game_over: Boolean-arvo, kuvaa onko peli päättynyt.
            x, y: koordinaatit, joita pelaaja on klikkanut, tai joihin pelaaja on liikkunut
            pelissä näppäimistöllä.
        """
        self._board.initialize_board(self._display, self._board.empty_board)
        self._board.all_sprites.draw(self._display)
        if self._board.error_message:
            self._board.draw_error_message(self._display)
        if self._board.begin:
            self._board.begin_view(self._display)
            if self._board.fens:
                self._board.choose_fen_view(self._display)
        elif self._board.input_fen:
            self._board.load_fen_view(self._display)
        elif self._board.input_name:
            self._board.load_name_view(self._display)
            self._board.game_view(self._display)
        elif game_over:
            self._board.end_game(self._display)
            if self._board.fens:
                self._board.choose_fen_view(self._display)
        else:
            self._board.game_view(self._display)
            if 0 <= x < 8*self._board.square_size and 0 <= y < 8*self._board.square_size:
                self._board.draw_current_square(self._display, x, y)

            if options:
                self._board.draw_options(self._display, options)

        pygame.display.update()
