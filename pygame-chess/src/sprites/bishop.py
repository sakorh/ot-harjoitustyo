import pygame
from ui.load_image import load_image


class Bishop(pygame.sprite.Sprite):
    """Lähettinappulan luova luokka.
    """

    def __init__(self, color, square_size, x=0, y=0):
        super().__init__()

        self.color = color

        self.directions = [(square_size, square_size), (square_size, -square_size),
                           (-square_size, -square_size), (-square_size, square_size)]

        self.image = load_image("bishop", color, square_size)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
