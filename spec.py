import pygame

class Spec(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #sprite constructor
        #self.image = pygame.Surface((30,30)) #width x height
        #self.image.fill((100,100,0))
        self.step = 0
        self.resting_spec = pygame.image.load('images/spec0.png').convert()
        self.resting_spec.set_colorkey([34,177,76])
        self.animations = []
        self.animations.append(pygame.image.load('images/spec1.png').convert())
        self.animations.append(pygame.image.load('images/spec2.png').convert())
        self.animations.append(pygame.image.load('images/spec3.png').convert())
        self.animations.append(pygame.image.load('images/spec4.png').convert())
        for animation in self.animations:
            animation.set_colorkey([34,177,76])
        self.image = self.resting_spec
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 200
        self.forward = False  #sprite forward movement
        self.backward = False #sprite backward movement
        self.slowForward = False  #slowing forward movement
        self.slowBackward = False  #slowing backward movement
        self.falling = True
        self.jumpTimer = 40
        self.jumpThreshold = 20 #two-stage jump height
        self.fallTimer = 0
        self.jump = False
        self.jumpTimeElapsed = 0
        self.speed = [0,0]  #[forward, backward]

    def update(self):
        if self.falling:  #gravity increases velocity
            self.rect.y += self.fallTimer
            self.fallTimer += .5
            if self.fallTimer > 6:
                self.fallTimer = 6
        if self.forward:  #speeds up sprite in right direction
            self.rect.x += self.speed[0]
            self.speedlimiter('forward')
            self.animate()
        elif self.backward: #speeds up sprite in left direction
            self.rect.x -= self.speed[1]
            self.speedlimiter('backward')
            self.animate()
        elif self.slowForward:  #slows down sprite in right direction
            self.speed[0] -= .5
            self.rect.x += self.speed[0]
            if self.speed[0] < 0:
                self.slowForward = False
                self.speed[0] = 0
        elif self.slowBackward:  #slows down sprite in left direction
            self.speed[1] -= .5
            self.rect.x -= self.speed[1]
            if self.speed[1] < 0:
                self.slowBackward = False
                self.speed[1] = 0
        else:  #sprite at rest
            self.resting()
            self.speed = [0,0]

        #Jump mechanics
        if self.jump == True and self.jumpTimer > self.jumpThreshold:  #upward arc
            self.rect.y -= self.jumpTimer / 5
            self.jumpTimer -= 1
        elif self.jump == True:  #downward arc
            self.falling = True
            self.jump = False
            self.jumpTimer = 40  # reset timer
            self.jumpThreshold = 20
        if self.jump == False: #constant downward pull
            self.falling = True

    #Sprite acceleration & deceleration
    def speedlimiter(self, direction):
        if direction == 'forward':
            self.speed[0] += .25
            if self.speed[0] > 6:
                self.speed[0] = 6
        if direction == 'backward':
            self.speed[1] += .25
            if self.speed[1] > 6:
                self.speed[1] = 6

    def animate(self):
        self.step += 1
        if self.step > 39:
            self.step = 0
        self.image = self.animations[int(self.step/10)]

    def resting(self):
        self.image = self.resting_spec
