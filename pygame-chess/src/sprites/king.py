import pygame
from ui.load_image import load_image


class King(pygame.sprite.Sprite):
    """Kuningasnappulan luova luokka.
    """

    def __init__(self, color, square_size, x=0, y=0):
        super().__init__()

        self.color = color
        self.image = load_image("king", color, square_size)
        self._square_size = square_size

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def show_options(self, x=0, y=0):
        """Palauttaa listan ruuduista, joihin kuningasnappulaa voi mahdollisesti siirtää.
        """
        options = [(x, y+self._square_size), (x, y-self._square_size), (x+self._square_size, y),
                   (x-self._square_size, y), (x -
                                              self._square_size, y-self._square_size),
                   (x-self._square_size, y+self._square_size),
                   (x+self._square_size, y-self._square_size),
                   (x+self._square_size, y+self._square_size)]
        return [o for o in options if (
            0 <= o[0] <= 7*self._square_size and 0 <= o[1] <= 7*self._square_size)]
