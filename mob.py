import pygame
from random import randint
from settings import *

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

    def update(self, powerUp, sprites, mobs):
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
        self.starting_y = y
        self.wiggled_x = 0

    def update(self, powerUp, sprites, mobs):
        if self.step is 80:
            self.recent_x = self.rect.x
        if self.step > 80 and self.step < 100 and self.step % 2 == 0:
            wiggle_x = randint(-4,4)
            self.rect.x += wiggle_x
            self.wiggled_x += wiggle_x
            self.rect.y -= randint(-4,4)
            if self.rect.y > self.starting_y:
                self.rect.y = self.starting_y
            if self.rect.y < self.starting_y - 10:
                self.rect.y = self.starting_y - 10
        if self.step == 0:
            self.rect.y = self.starting_y
            self.rect.x -= self.wiggled_x
            self.wiggled_x = 0
        self.animate(sprites, mobs)

    def animate(self, sprites, mobs):
        self.step += 1
        if self.step == 100:
            self.left = not self.left
            self.image = self.animations[self.left]
            self.step = 0
            ray = Projectile (self.rect.x, self.rect.centery, self.left)
            sprites.add(ray)
            mobs.add(ray)

class Infrared(Mob):
    def __init__(self, x, y):
        super().__init__(x,y)
        self.step = 0
        self.animations = []
        self.animations.append(pygame.image.load('images/mob_infrared1.png').convert())
        self.animations.append(pygame.image.load('images/mob_infrared2.png').convert())
        for animation in self.animations:
            animation.set_colorkey([34,177,76])
        self.image = self.animations[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.starting_y = y
        self.jump = False
        self.jump_count = 0
        self.vertical = [3.5,3.5,3.5,3,3,3,2,2,1.5,1.5,1.5,1,1,1,1,1,1,.5,.5,.5,.5,.5]

    def update(self, powerUp, sprites, mobs):
        self.step += 1
        if self.jump:
            self.image = self.animations[1]
            self.rect.y -= self.vertical[self.jump_count]
            self.jump_count += 1
            if self.jump_count > 21:
                self.jump = False
                self.jump_count -= 1
        else:
            self.image = self.animations[0]
            self.rect.y += self.vertical[self.jump_count]
            self.jump_count -= 1
            if self.rect.y > self.starting_y:
                self.rect.y = self.starting_y
            if self.jump_count < 0:
                self.jump_count = 0
        if self.step == 100:
            self.jump = True
            self.step = 0

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, left):
        pygame.sprite.Sprite.__init__(self) #sprite constructor
        self.image = pygame.Surface((5,5)) #width x height
        self.image.fill((255,242,0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.left = left
        self.timer = 0

    def update(self, powerUp, sprites, mobs):
        self.animate()
        self.timer += 1
        if self.timer < 125:
            if self.left:
                self.rect.x += 3
            else:
                self.rect.x -= 3
        else:
            self.kill()

    def animate(self):
        if self.timer % 2 == 0:
            self.image.fill((255,242,0))
        else:
            self.image.fill(LIGHT_RED)
