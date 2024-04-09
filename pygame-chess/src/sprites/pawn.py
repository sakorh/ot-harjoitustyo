import pygame


class Pawn(pygame.sprite.Sprite):
        def __init__(self, color, x=0, y=0):
            super().__init__()
        
            self.color = color
            self.image = pygame.Surface((80,80), pygame.SRCALPHA)
            self.image.fill((255,255,255))

            self.image_loaded = pygame.image.load(f"src/assets/pawn_{color}.png")
            self.image_loaded = pygame.transform.smoothscale(self.image_loaded, (80,80), dest_surface=self.image)

            self.rect = self.image_loaded.get_rect()
            self.rect.x = x
            self.rect.y = y

        def show_options(self, x=0, y=0):
            if self.color == "black" and 0 <= y <= 80:
                 return [(x,y+80), (x, y+160)]
            elif self.color == "black":
                 return [(x, y+80)]
            elif self.color == "white" and 560 >= y >= 480:
                 return [(x,y-80), (x,y-160)]
            elif self.color == "white":
                return [(x,y-80)]
            
                    


              
