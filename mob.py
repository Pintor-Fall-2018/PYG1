import pygame
from random import randint
from settings import *

class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, mob_sounds):
        pygame.sprite.Sprite.__init__(self) #sprite constructor
        self.parent_variable = 12345
        self.mob_sounds = mob_sounds

    #Returns true if spec is within earshot, evaluates whether to play sound.
    def withinEarshot(self, spec_x):
        if self.rect.x - spec_x < 400:
            return True
        else:
            return False

class Ultraviolet(Mob):
    def __init__(self, x, y, mob_sounds):
        super().__init__(x,y, mob_sounds)
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

    def update(self, powerUp, sprites, mobs, spec_x):
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
    def __init__(self, x, y, mob_sounds):
        super().__init__(x,y, mob_sounds)
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

    def update(self, powerUp, sprites, mobs, spec_x):
        if self.step is 80:
            self.recent_x = self.rect.x
        if self.step > 80 and self.step < 100 and self.step % 2 == 0:
            wiggle_x = randint(-3,3)
            self.rect.x += wiggle_x
            self.wiggled_x += wiggle_x
            self.rect.y -= randint(-2,4)
            if self.rect.y > self.starting_y:
                self.rect.y = self.starting_y
            if self.rect.y < self.starting_y - 10:
                self.rect.y = self.starting_y - 10
        if self.step == 0:
            self.rect.y = self.starting_y
            self.rect.x -= self.wiggled_x
            self.wiggled_x = 0
        self.animate(sprites, mobs, spec_x)

    def animate(self, sprites, mobs, spec_x):
        self.step += 1
        if self.step == 100:
            self.left = not self.left
            self.image = self.animations[self.left]
            self.step = 0
            if self.withinEarshot(spec_x):
                self.mob_sounds[0].play()
                ray = Projectile (self.rect.x, self.rect.centery, self.left)
                sprites.add(ray)
                mobs.add(ray)

class Infrared(Mob):
    def __init__(self, x, y, mob_sounds):
        super().__init__(x,y, mob_sounds)
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

    def update(self, powerUp, sprites, mobs, spec_x):
        self.step += 1
        if self.jump:
            if self.step == 1:
                if self.withinEarshot(spec_x):
                    self.mob_sounds[1].play()
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

class BlackHole(Mob):
    def __init__(self, x, y, mob_sounds):
        super().__init__(x,y, mob_sounds)
        self.step = 0
        self.animations = []
        self.animations.append(pygame.image.load('images/black_hole1.png').convert())
        self.animations.append(pygame.image.load('images/black_hole2.png').convert())
        for animation in self.animations:
            animation.set_colorkey(BLACK)
        self.image = self.animations[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.left = True  #True is left, False is right

    def update(self, powerUp, sprites, mobs, spec_x):
        if self.left:
            self.rect.x -= 1
            self.image = self.animations[0]
        else:
            self.rect.x += 1
            self.image = self.animations[1]
        self.animate()

    def animate(self):
        self.step += 1
        if self.step == 5:
            self.left = not self.left
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

    def update(self, powerUp, sprites, mobs, spec_x):
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
