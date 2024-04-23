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

    def choose_option(self, sprite, options, turn, x, y):
        for option in options:
            if self._is_valid_option(sprite, option, turn, x, y):
                return self.move_piece(
                    sprite, dx=option[0]-sprite.rect.x, dy=option[1]-sprite.rect.y)
        return False

    # AI-generated code begins
    def _is_valid_option(self, sprite, option, turn, x, y):
        opt = pygame.Rect(
            option[0], option[1], self._board.square_size, self._board.square_size)
        return opt.collidepoint(x, y) and sprite.color == turn
    # AI-generated code ends

    def game_over(self):
        for king in self._board.kings:
            moves = self.get_moves(king)
            if not moves and self.king_in_check is False:
                return self._stalemate(king.color)
            if self.king_in_check and not moves:
                return self._checkmate(king)
        return False

    # function refactored using AI
    def _stalemate(self, color):
        return not any(
            self.get_moves(piece) for piece in self._board.all_sprites if piece.color == color)

    # function refactored using AI
    def _checkmate(self, king):
        check = all(
            (self._king_safety(move, piece, king)
             for move in self.get_moves(piece))
            for piece in self._board.all_sprites
            if piece.color == king.color and piece not in self._board.kings
        )
        return check

    def _king_safety(self, move, piece, king):
        king_is_safe = False
        dx, dy = (move[0]-piece.rect.x, move[1]-piece.rect.y)
        piece.rect.move_ip(dx, dy)
        if self._king_in_check(king) is False:
            king_is_safe = True
        piece.rect.move_ip(-dx, -dy)
        return not king_is_safe

    def _get_options(self, sprite):
        options = []
        directions = sprite.directions
        # AI-generated code begins
        for direction in directions:
            squares = []
            x_delta, y_delta = direction
            x_temp, y_temp = sprite.rect.x, sprite.rect.y
            while 0 <= x_temp+x_delta <= 7*self._board.square_size and (
                    0 <= y_temp+y_delta <= 7*self._board.square_size):
                squares.append((x_temp+x_delta, y_temp+y_delta))
                x_temp += x_delta
                y_temp += y_delta
            options.append(squares)
        # AI-generated code ends

        return options

    def move_piece(self, sprite, dx, dy):
        can_move, can_eat = self._check_move(sprite, dx, dy)
        if not can_move:
            return False
        sprite.rect.move_ip(dx, dy)
        if can_eat:
            self._board.all_sprites.remove(sprite)
            collide = self._check_collision(sprite)
            collide[0].kill()
            self._board.all_sprites.add(sprite)

        return True

    def _check_move(self, sprite, dx, dy):
        can_eat = False

        sprite.rect.move_ip(dx, dy)
        self._board.all_sprites.remove(sprite)

        collide = self._check_collision(sprite)
        if collide:
            for piece in collide:
                if piece.color != sprite.color and (
                        piece in self._board.kings):
                    self.king_in_check = True
                if piece.color != sprite.color:
                    can_move = True
                    can_eat = True
                    break
                if piece.color == sprite.color:
                    can_move = False
        else:
            can_move = not collide
        self._board.all_sprites.add(sprite)
        sprite.rect.move_ip(-dx, -dy)

        return can_move, can_eat

    def _pawn_can_move(self, sprite, dx, dy):

        sprite.rect.move_ip(dx, dy)
        self._board.all_sprites.remove(sprite)

        collide = self._check_collision(sprite)
        can_move = not collide

        self._board.all_sprites.add(sprite)
        sprite.rect.move_ip(-dx, -dy)

        return can_move

    def _check_collision(self, sprite):
        return pygame.sprite.spritecollide(
            sprite, self._board.all_sprites, False)

    def get_moves(self, sprite):
        if sprite in self._board.pawns:
            return self._get_pawn_moves(sprite)
        if sprite in self._board.bishops or (
                sprite in self._board.rooks or sprite in self._board.queens):
            options = self._check_movement_directions(sprite)
        elif sprite in self._board.kings:
            options = self._check_king_moves(sprite)
        else:
            all_options = sprite.show_options(sprite.rect.x, sprite.rect.y)
            return [square for square in all_options if self._check_move(
                sprite, square[0]-sprite.rect.x, square[1]-sprite.rect.y)[0]]

        return options

    def _check_movement_directions(self, sprite):
        options = []
        directions = self._get_options(sprite)
        for direction in directions:
            for square in direction:
                can_move, can_eat = self._check_move(
                    sprite, square[0]-sprite.rect.x, square[1]-sprite.rect.y)
                if can_move:
                    options.append(square)
                if not can_move or can_eat:
                    break
        return options

    def _get_pawn_moves(self, sprite):
        enemy_squares = sprite.check_for_enemy(
            sprite.rect.x, sprite.rect.y)
        options = [square for square in enemy_squares if self._check_move(
            sprite, square[0]-sprite.rect.x, square[1]-sprite.rect.y)[1]]
        free_squares = sprite.show_options(sprite.rect.x, sprite.rect.y)
        for square in free_squares:
            can_move = self._pawn_can_move(
                sprite, square[0]-sprite.rect.x, square[1]-sprite.rect.y)
            if can_move:
                options.append(square)
        return options

    def _king_in_check(self, king):
        for piece in self._board.all_sprites:
            if piece.color != king.color and piece not in self._board.kings:
                self.get_moves(piece)
        return self.king_in_check

    def _check_king_moves(self, king):
        options = []

        check = self._king_in_check(king)

        squares = king.show_options(king.rect.x, king.rect.y)
        for square in squares:
            self.king_in_check = False
            dx, dy = square[0]-king.rect.x, square[1]-king.rect.y
            can_move, _ = self._check_move(king, dx, dy)
            if not can_move:
                continue
            king.rect.move_ip(dx, dy)
            if not self._king_in_check(king):
                options.append(square)
            king.rect.move_ip(-dx, -dy)

        self.king_in_check = check

        return options
