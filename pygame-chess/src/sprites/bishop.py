import pygame
from ui.load_image import load_image


class Bishop(pygame.sprite.Sprite):
    def __init__(self, color, x=0, y=0):
        super().__init__()

        self.color = color

        i = 80
        self.directions = [(i, i), (i, -i), (-i, -i), (-i, i)]

        self.image = load_image("bishop", color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
