import pygame
from ui.load_image import load_image


class Pawn(pygame.sprite.Sprite):
    def __init__(self, color, x=0, y=0):
        super().__init__()
        self.color = color
        self.image = load_image("pawn", color)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def check_for_enemy(self, x=0, y=0):
        black = [(x-80, y+80), (x+80, y+80)]
        white = [(x-80, y-80), (x+80, y-80)]

        if self.color == "black":
            return [option for option in black if 0 <= option[0] <= 560 and option[1] <= 560]

        return [option for option in white if 0 <= option[0] <= 560 and 0 <= option[1]]

    def show_options(self, x=0, y=0):
        if self.color == "black" and 0 <= y <= 80:
            return [(x, y+80), (x, y+160)]
        if self.color == "black":
            return [(x, y+80)]
        if self.color == "white" and 560 >= y >= 480:
            return [(x, y-80), (x, y-160)]
        return [(x, y-80)]
