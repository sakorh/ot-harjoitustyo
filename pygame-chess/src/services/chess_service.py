import pygame


class ChessService:
    """Pelin logiikasta vastaava luokka. 
    """

    def __init__(self, board):
        self.king_in_check = False
        self._board = board
        self._turn = "white"
        self.selected_piece = None
        self.options = []
        self.game_over = False
        self._check_game_over()

    def initialize_game(self):
        self._turn = "white"
        self._board.start_game()
        self.game_over = False
        self.king_in_check = False
        self.options.clear()

    def _change_turn(self):
        """Vaihtaa vuoron toiselle pelaajalle. 
        """
        if self._turn == "white":
            self._turn = "black"
        else:
            self._turn = "white"

    def choose_piece(self, x, y):
        """Käy läpi nappuloita ja tarkistaa valitsiko pelaaja jonkin nappulan. 
        Jos käyttäjän on klikannut nappulaa, tallennetaan valittu nappula, ja kaikki
        mahdolliset ruudut, joihin se voi liikkua. 

        Args:
        x, y: käyttäjän klikkaamat koordinaatit.
        """
        for piece in self._board.all_sprites:
            if piece.rect.collidepoint(x, y) and piece.color == self._turn:
                self.selected_piece = piece
                options = self.get_moves(self.selected_piece)
                if self.king_in_check == self._turn:
                    king = [
                        king for king in self._board.kings if king.color == self.king_in_check][0]
                else:
                    king = [
                        king for king in self._board.kings if king.color == piece.color][0]
                options = self._filter_moves_preventing_check(
                    options, self.selected_piece, king)
                self.options = options

    def _filter_moves_preventing_check(self, options, piece, king):
        """Käy läpi pelaajan valitseman nappulan siirtovaihtoehdot, ja palauttaa niistä vain ne,
        joiden jälkeen saman armeijan kuningas ei ole uhattuna. 

        Args:
            options: valitun nappulan siirtovaihtoehdot.
            piece: nappula, jonka siirtovaihtoehtoja halutaan tarkastella.
            king: kuningas, jonka shakkiuhka halutaan estää.
        """
        filtered_moves = []
        for move in options:
            dx, dy = (move[0]-piece.rect.x, move[1]-piece.rect.y)
            _, can_eat = self._check_move(piece, dx, dy)
            check = self.king_in_check
            piece.rect.move_ip(dx, dy)
            if can_eat:
                collide = self._check_collision(piece)
                enemy = collide[0]
                self._board.all_sprites.remove(enemy)
            self._check_king_moves(king)
            if self.king_in_check != king.color:
                filtered_moves.append(move)
            if can_eat:
                self._board.all_sprites.add(enemy)
            piece.rect.move_ip(-dx, -dy)
            self.king_in_check = check

        return filtered_moves

    def choose_option(self, x, y):
        """Käy läpi aiemmin valitun nappulan siirtovaihtoehtoja, ja tarkistaa
        onko pelaajan valitsema siirto laillinen. Jos on, pelaajan valitsema
        nappula siirretään ruutuun.

        Args:
            x,y: valitun ruudun koordinaatit, johon pelaaja haluaisi nappulansa
            siirtää.
        """
        for option in self.options:
            if self._is_valid_option(option, x, y):
                self.move_piece(
                    self.selected_piece, dx=option[0] -
                    self.selected_piece.rect.x,
                    dy=option[1]-self.selected_piece.rect.y)
                self.options.clear()
                self.selected_piece = None

    # AI-generated code begins
    def _is_valid_option(self, option, x, y):
        opt = pygame.Rect(
            option[0], option[1], self._board.square_size, self._board.square_size)
        return opt.collidepoint(x, y) and self.selected_piece.color == self._turn
    # AI-generated code ends

    def _check_game_over(self):
        """Tarkistaa onko sen pelaajan kuninkaalla siirtovaihtoehtoja, jonka vuoro on.
        Jos ei ole, tarkistetaan onko kyseinen kuningas shakissa.
        Jos ei, tarkistetaan onko pelitilanne patti tai shakkimatti, jolloin peli päättyy.
        """
        if self._board.kings:
            king = [king for king in self._board.kings if king.color == self._turn][0]

            moves = self.get_moves(king)
            if not moves and self._king_in_check(king) is False:
                if self._stalemate(king):
                    self.game_over = True
            if self._king_in_check(king) and not moves:
                if self._checkmate(king):
                    self.game_over = True

    # function refactored using AI
    def _stalemate(self, king):
        """Tarkistaa onko peli pattitilanteessa.
        """
        return not any(self._filter_moves_preventing_check(self.get_moves(piece), piece, king)
                       for piece in self._board.all_sprites if piece.color == king.color)

    # function refactored using AI
    def _checkmate(self, king):
        """Tarkistaa onko pelitilanne shakkimatti.
        """
        check = not any(
            self._filter_moves_preventing_check(
                self.get_moves(piece), piece, king)
            for piece in self._board.all_sprites
            if piece.color == king.color and piece not in self._board.kings
        )
        return check

    def _get_options(self, sprite):
        """Palauttaa kaikki pelilaudalle mahtuvat ruudut parametrina annetun nappulan 
        liikkumissuunnista.
        """
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

    def move_piece(self, piece, dx, dy):
        """Siirtää parametrina annettua nappulaa parametreissä annetun matkan.
        Jos siirron yhteydessä nappula syö vastustajan nappulan, tämä poistetaan pelilaudalta.
        Lopuksi vuoro vaihtuu toiselle pelaajalle, ja tarkistetaan päättikö siirto pelin.
        """
        _, can_eat = self._check_move(piece, dx, dy)
        piece.rect.move_ip(dx, dy)
        if can_eat:
            self._board.all_sprites.remove(piece)
            collide = self._check_collision(piece)
            collide[0].kill()
            self._board.all_sprites.add(piece)

        self._change_turn()
        self._check_game_over()

        return True

    # function refactored using AI
    def _check_move(self, sprite, dx, dy):
        """Tarkistaa voiko parametrina annettu nappula siirtyä parametreina
        annetun siirron ja törmääkö nappula ruudussa vastustajan nappulaan.
        """
        can_eat = False
        can_move = True

        sprite.rect.move_ip(dx, dy)

        collide = self._check_collision(sprite)
        if collide:
            for piece in collide:
                if piece.color != sprite.color and (
                        piece in self._board.kings):
                    self.king_in_check = piece.color
                if piece.color != sprite.color:
                    can_eat = True
                    break
                can_move = False
        sprite.rect.move_ip(-dx, -dy)

        return can_move, can_eat

    def _pawn_can_move(self, sprite, dx, dy):
        """Tarkistaa voiko sotilasnappula liikkua eteenpäin.
        """
        sprite.rect.move_ip(dx, dy)
        self._board.all_sprites.remove(sprite)

        collide = self._check_collision(sprite)
        can_move = not collide

        self._board.all_sprites.add(sprite)
        sprite.rect.move_ip(-dx, -dy)

        return can_move

    def _check_collision(self, sprite):
        """Tarkistaa törmääkö parametrina annettu nappula toiseen.
        """
        self._board.all_sprites.remove(sprite)
        collide = pygame.sprite.spritecollide(
            sprite, self._board.all_sprites, False)
        self._board.all_sprites.add(sprite)
        return collide

    def get_moves(self, sprite):
        """Palauttaa parametrina annetun nappulan mahdolliset ruudut joihin se voi siirtyä.
        Args:
            sprite: nappula, jonka siirtovaihtoehtoja haetaan.
        """
        if sprite in self._board.pawns:
            return self._get_pawn_moves(sprite)
        if sprite in self._board.bishops or (
                sprite in self._board.rooks or sprite in self._board.queens):
            options = self._check_movement_directions(sprite)
        elif sprite in self._board.kings:
            options = self._check_king_moves(sprite)
        elif sprite in self._board.knights:
            all_options = sprite.show_options(sprite.rect.x, sprite.rect.y)
            return [square for square in all_options if self._check_move(
                sprite, square[0]-sprite.rect.x, square[1]-sprite.rect.y)[0]]

        return options

    def _check_movement_directions(self, sprite):
        """Tarkistaa ja palauttaa lähettien, tornien ja kuningattarien siirtovaihtoehdot.
        """
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
        """Palauttaa parametrina annetun sotilasnappulan kaikki mahdolliset siirtovaihtoehdot.
        """
        enemy_squares = sprite.check_for_enemy(
            sprite.rect.x, sprite.rect.y)
        options = [square for square in enemy_squares if self._check_move(
            sprite, square[0]-sprite.rect.x, square[1]-sprite.rect.y)[1]]
        free_squares = sprite.show_options(sprite.rect.x, sprite.rect.y)
        for square in free_squares:
            can_move = self._pawn_can_move(
                sprite, square[0]-sprite.rect.x, square[1]-sprite.rect.y)
            if not can_move:
                break
            options.append(square)
        return options

    def _king_in_check(self, king):
        """Tarkistaa onko parametrina annettu kuningas nappula shakissa.
        """
        self.king_in_check = False
        for piece in self._board.all_sprites:
            if piece.color != king.color and piece not in self._board.kings:
                self.get_moves(piece)
        return self.king_in_check

    def _check_king_moves(self, king):
        """Tarkistaa onko parametrina annetulla kuninkaalla yhtään laillisia siirtoja,
        ja palauttaa ne.
        """
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
