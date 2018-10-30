import pygame

class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self) #sprite constructor
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

    def update(self):
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

class Ultraviolet(Mob):
    def __init__(self, x, y):
        Mob.__init__(self, x, y)
