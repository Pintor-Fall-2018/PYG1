import pygame
from settings import *
class Light(pygame.sprite.Sprite):
    def __init__(self, bl_light_images):
        pygame.sprite.Sprite.__init__(self) #sprite constructor
        self.bl_images = bl_light_images
        self.index = 0
        self.image = self.bl_images[self.index]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = MAX_RIGHT_WIDTH - 500  # put it at the end of the level
        self.rect.y = 320

        def animate(self):
            self.index = (self.index + 1)
            if self.index >= len(self.bl_images):
                self.index = 0
            self.image = self.bl_images[self.index]
            self.rect.x -= 1

        def update(self):
            print("Calling animate")
            self.animate()
