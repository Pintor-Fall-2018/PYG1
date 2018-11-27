import pygame
#Tiled blocks build environment
class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_path).convert()
        #self.image = pygame.transform.scale(self.image, (20,20))  #testing
        self.image.set_colorkey([255,255,255])  #sets white to transparent
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.moving_left = False
        self.moving_right = False
