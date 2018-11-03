import pygame
from settings import *
class Light(pygame.sprite.Sprite):
    def __init__(self, light_images):
        pygame.sprite.Sprite.__init__(self) #sprite constructor
        self.images = light_images
        self.index = 0
        self.image = self.images[self.index]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = MAX_RIGHT_WIDTH     # put it at the end of the level
        self.rect.y = 200
        self.animation_frames = 0

    def animate(self):
        self.index = (self.index + 1)
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]
        self.image.set_colorkey(BLACK)

    def update(self):
        self.animation_frames += 1
        if self.animation_frames > 10:
            self.animation_frames = 0
            self.animate()
