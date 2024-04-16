import pygame
from load_image import load_image


class Knight(pygame.sprite.Sprite):
    def __init__(self, color, x=0, y=0):
        super().__init__()

        self.color = color

        self.image = load_image("knight", color)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def show_options(self, x=0, y=0):
        options = [(x-80, y+160), (x+80, y+160), (x-160, y-80), (x-160, y+80),
                   (x+160, y+80), (x+160, y-80), (x-80, y-160), (x+80, y-160)]
        return [o for o in options if 0 <= o[0] <= 560 and 0 <= o[1] <= 560]
