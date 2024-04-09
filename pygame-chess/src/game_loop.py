import pygame

class GameLoop:
    def __init__(self, board, square_size, display):
        self._clock = pygame.time.Clock()
        self._board = board
        self._square_size = square_size
        self._display = display
        self._selected_piece = None
        self._options = []
        self._turn = "white"

    def start(self):
        while True:
            if self._handle_events() == False:
                break
            self._render()
            self._clock.tick(60)

    def _handle_events(self):
        self._board.initialize_board(self._display, self._board.empty_board)

        if self._selected_piece:
            for option in self._selected_piece.show_options(self._selected_piece.rect.x,self._selected_piece.rect.y):
                self._options.append(option)
                self._board.draw_options(self._display, option[0], option[1])
            
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for p in self._board.all_sprites:
                    if p.rect.collidepoint(x,y) and p.color == self._turn:
                        self._selected_piece = p

                if self._options:
                    for option in self._options:
                        opt = pygame.Rect(option[0], option[1], self._square_size, self._square_size)
                        if opt.collidepoint(x,y) and self._selected_piece.color == self._turn:
                            if not self._board.move_piece(self._selected_piece, dx=option[0]-self._selected_piece.rect.x, dy=option[1]-self._selected_piece.rect.y):
                                continue
                            self._options.clear()
                            if self._selected_piece.color == "white":
                                self._turn = "black"
                                self._selected_piece = None
                            else:
                                self._turn = "white"
                                self._selected_piece = None
                            break

            elif event.type == pygame.QUIT:
                return False

    def _render(self):
        self._board.all_sprites.draw(self._display)
        pygame.display.flip()
        pygame.display.update()


                