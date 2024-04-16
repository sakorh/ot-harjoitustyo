import pygame
from load_image import load_image


class Queen(pygame.sprite.Sprite):
    def __init__(self, color, x=0, y=0):
        super().__init__()

        self.color = color
        self.image = load_image("queen", color)

        i = 80
        self.directions = [(i, i), (i, -i), (-i, -i), (-i, i),
                           (0, i), (0, -i), (-i, 0), (i, 0)]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
