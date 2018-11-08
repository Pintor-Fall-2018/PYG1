import pygame
from random import randint

class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self) #sprite constructor
        self.parent_variable = 12345

class Ultraviolet(Mob):
    def __init__(self, x, y):
        super().__init__(x,y)
        self.step = 0
        self.animations = []
        self.animations.append(pygame.image.load('images/uv0.png').convert())
        self.animations.append(pygame.image.load('images/uv1.png').convert())
        for animation in self.animations:
            animation.set_colorkey([34,177,76])
        self.image = self.animations[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.left = True  #True is left, False is right

    def update(self, powerUp):
        if self.left:
            self.rect.x -= 1
            self.image = self.animations[0]
        else:
            self.rect.x += 1
            self.image = self.animations[1]
        self.animate()

    def animate(self):
        self.step += 1
        if self.step == 100:
            self.left = not self.left
            self.step = 0

class Gamma(Mob):
    def __init__(self, x, y):
        super().__init__(x,y)
        self.step = 0
        self.animations = []
        self.animations.append(pygame.image.load('images/mob_gamma0.png').convert())
        self.animations.append(pygame.image.load('images/mob_gamma1.png').convert())
        for animation in self.animations:
            animation.set_colorkey([34,177,76])
        self.image = self.animations[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.left = True  #True is left, False is right
        self.starting_y = y #self.rect.y

    def update(self, powerUp):
        if self.step > 80 and self.step < 100 and self.step % 2 == 0:
            self.rect.x += randint(0,4)
            self.rect.x -= randint(0,4)
            self.rect.y -= randint(0,3)
            self.rect.y += randint(0,3)
            if self.rect.y > 320:
                self.rect.y = 320
            if self.rect.y < 310:
                self.rect.y = 310
        if self.step == 0:
            self.rect.y = self.starting_y
        self.animate()

    def animate(self):
        self.step += 1
        if self.step == 100:
            self.left = not self.left
            self.image = self.animations[self.left]
            self.step = 0
