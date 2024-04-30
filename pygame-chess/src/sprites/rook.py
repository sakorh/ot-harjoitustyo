import pygame
from ui.load_image import load_image


class Rook(pygame.sprite.Sprite):
    def __init__(self, color, square_size, x=0, y=0):
        super().__init__()

        self.color = color
        self.image = load_image("rook", color, square_size)

        self.directions = [(0, square_size), (0, -square_size),
                           (-square_size, 0), (square_size, 0)]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
