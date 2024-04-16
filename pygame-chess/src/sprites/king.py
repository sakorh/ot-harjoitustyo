import pygame
from load_image import load_image


class King(pygame.sprite.Sprite):
    def __init__(self, color, x=0, y=0):
        super().__init__()

        self.color = color
        self.image = load_image("king", color)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def show_options(self, x=0, y=0):
        options = [(x, y+80), (x, y-80), (x+80, y), (x-80, y),
                   (x-80, y-80), (x-80, y+80), (x+80, y-80), (x+80, y+80)]
        return [o for o in options if 0 <= o[0] <= 560 and 0 <= o[1] <= 560]
