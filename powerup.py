import pygame
from settings import *

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        pygame.sprite.Sprite.__init__(self)
        self.image = image_path
        self.image.set_colorkey([255,255,255])  #sets white to transparent
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
