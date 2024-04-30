import pygame


def load_image(name, color, square_size):
    """Nappuloiden kuvien lataamisesta vastaava luokka.
    """
    image = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
def load_image(name, color):
    image = pygame.Surface((80, 80), pygame.SRCALPHA)
    image.fill((255, 255, 255))

    image_loaded = pygame.image.load(f"src/assets/{name}_{color}.png")
    image_loaded = pygame.transform.smoothscale(
        image_loaded, (80, 80), dest_surface=image)
    return image_loaded
