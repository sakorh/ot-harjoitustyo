import pygame


class ChessService:
    def __init__(self, board):
        self.king_in_check = False
        self._board = board

    def choose_piece(self, turn, x, y):
        for piece in self._board.all_sprites:
            if piece.rect.collidepoint(x, y) and piece.color == turn:
                return piece
        return None

    def check_options(self, sprite, options, turn, x, y):
        for option in options:
            opt = pygame.Rect(
                option[0], option[1], self._board.square_size, self._board.square_size)
            if opt.collidepoint(x, y) and sprite.color == turn:
                if self.move_piece(sprite, dx=option[0]-sprite.rect.x, dy=option[1]-sprite.rect.y):
                    return True
        return False

    def checkmate(self):
        for king in self._board.kings:
            moves = self.get_moves(king)
            if self.king_in_check and not moves:
                return True
        return False

    def end_game(self, display):
        self._board.all_sprites.empty()
        green = (0, 255, 0)
        black = (0, 0, 0)
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('Game Over', True, green, black)
        text_rect = text.get_rect()
        x = y = 640
        text_rect.center = (x // 2, y // 2)
        display.blit(text, text_rect)

    def _get_options(self, sprite):
        options = []
        directions = sprite.directions
        # generated code starts
        for direction in directions:
            squares = []
            x_delta, y_delta = direction
            x_temp, y_temp = sprite.rect.x, sprite.rect.y
            while 0 <= x_temp+x_delta <= 560 and 0 <= y_temp+y_delta <= 560:
                squares.append((x_temp+x_delta, y_temp+y_delta))
                x_temp += x_delta
                y_temp += y_delta
            options.append(squares)
        # generated code ends

        return options

    def move_piece(self, sprite, dx, dy):
        can_move, can_eat = self._check_move(sprite, dx, dy)
        if not can_move:
            return False
        sprite.rect.move_ip(dx, dy)
        if can_eat:
            self._board.all_sprites.remove(sprite)
            collide = pygame.sprite.spritecollide(
                sprite, self._board.all_sprites, False)
            self._board.all_sprites.remove(collide[0])
            self._board.all_sprites.add(sprite)

        return True

    def _check_move(self, sprite, dx, dy):
        can_eat = False

        sprite.rect.move_ip(dx, dy)
        self._board.all_sprites.remove(sprite)

        collide = pygame.sprite.spritecollide(
            sprite, self._board.all_sprites, False)
        if collide and collide[0].color != sprite.color:
            can_move = True
            can_eat = True
            if collide[0] in self._board.kings:
                self.king_in_check = True
        else:
            can_move = not collide
        self._board.all_sprites.add(sprite)
        sprite.rect.move_ip(-dx, -dy)

        return can_move, can_eat

    def get_moves(self, sprite):
        if sprite in self._board.pawns:
            options = self._get_pawn_moves(sprite)
        elif sprite in self._board.bishops or (
                sprite in self._board.rooks or sprite in self._board.queens):
            options = []
            directions = self._get_options(sprite)
            for direction in directions:
                for square in direction:
                    can_move, can_eat = self._check_move(
                        sprite, square[0]-sprite.rect.x, square[1]-sprite.rect.y)
                    if not can_move:
                        break
                    options.append(square)
                    if can_eat:
                        break
        elif sprite in self._board.kings:
            options = self._check_king_moves(sprite)
        else:
            return sprite.show_options(sprite.rect.x, sprite.rect.y)

        return options

    def _get_pawn_moves(self, sprite):
        enemy_squares = sprite.check_for_enemy(
            sprite.rect.x, sprite.rect.y)
        enemies = [square for square in enemy_squares if self._check_move(
            sprite, square[0]-sprite.rect.x, square[1]-sprite.rect.y)[1]]
        free_squares = sprite.show_options(sprite.rect.x, sprite.rect.y)
        options = [square for square in free_squares if not self._check_move(
            sprite, square[0]-sprite.rect.x, square[1]-sprite.rect.y)[1]]
        options.extend(enemies)
        return options

    def _check_king_moves(self, sprite):
        options = []

        squares = sprite.show_options(sprite.rect.x, sprite.rect.y)
        for square in squares:
            self.king_in_check = False
            dx, dy = square[0]-sprite.rect.x, square[1]-sprite.rect.y
            can_move, can_eat = self._check_move(sprite, dx, dy)
            sprite.rect.move_ip(dx, dy)
            for piece in self._board.all_sprites:
                if piece.color != sprite.color and piece not in self._board.kings:
                    self.get_moves(piece)
            if not self.king_in_check and (can_move or can_eat):
                options.append(square)
            sprite.rect.move_ip(-dx, -dy)

        return options
