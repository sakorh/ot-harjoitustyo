import pygame


def load_image(name, color, square_size):
    image = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
    image.fill((255, 255, 255))

    image_loaded = pygame.image.load(f"src/assets/{name}_{color}.png")
    image_loaded = pygame.transform.smoothscale(
        image_loaded, (square_size, square_size), dest_surface=image)
    return image_loaded
