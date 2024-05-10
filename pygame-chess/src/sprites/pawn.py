import pygame
from ui.load_image import load_image


class Pawn(pygame.sprite.Sprite):
    """Sotilasnappulan luova luokka.
    """

    def __init__(self, color, square_size, x=0, y=0):
        super().__init__()
        self.color = color
        self.image = load_image("pawn", color, square_size)
        self._square_size = square_size

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def check_for_enemy(self, x=0, y=0):
        """Palauttaa parametreinä annettujen koordinaattien kohdalta katsottuna ne ruudut,
        joista vastustajan nappulan voi syödä.
        """
        black = [(x-self._square_size, y+self._square_size),
                 (x+self._square_size, y+self._square_size)]
        white = [(x-self._square_size, y-self._square_size),
                 (x+self._square_size, y-self._square_size)]

        if self.color == "black":
            return [option for option in black if (
                0 <= option[0] <= 7*self._square_size and option[1] <= 7*self._square_size)]

        return [option for option in white if (
            0 <= option[0] <= 7*self._square_size and 0 <= option[1])]

    def show_options(self, x=0, y=0):
        """Palauttaa listan niiden ruutujen koordinaateista, joihin sotilasnappula voi siirtyä.
        """
        if self.color == "black" and 0 <= y <= self._square_size:
            return [(x, y+self._square_size), (x, y+2*self._square_size)]
        if self.color == "black":
            return [(x, y+self._square_size)]
        if self.color == "white" and 7*self._square_size >= y >= 6*self._square_size:
            return [(x, y-self._square_size), (x, y-2*self._square_size)]
        return [(x, y-self._square_size)]
