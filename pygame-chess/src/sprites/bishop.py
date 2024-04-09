import pygame

class Bishop(pygame.sprite.Sprite):
    def __init__(self, color, x=0, y=0):
            super().__init__()

            self.color = color
        
            self.image = pygame.Surface((80,80), pygame.SRCALPHA)
            self.image.fill((255,255,255))

            self.image_loaded = pygame.image.load(f"src/assets/bishop_{color}.png")
            self.image_loaded = pygame.transform.smoothscale(self.image_loaded, (80,80), dest_surface=self.image)

            self.rect = self.image_loaded.get_rect()
            self.rect.x = x
            self.rect.y = y

    def show_options(self, x=0, y=0):
        options = []
        for i in range (80,561, 80):
            for option in [(x+i,y+i),(x+i,y-i),(x-i,y-i),(x-i,y+i)]:
                options.append(option)
        
        return [o for o in options if 0 <= o[0] <= 560 and 0<=o[1]<=560]