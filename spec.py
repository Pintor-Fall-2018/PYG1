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
        self.falling = True
        self.jumpTimer = 0
        self.jumpThreshold = 20 #two-stage jump height
        self.fallTimer = 0
        self.jump = False
        self.jumpTimeElapsed = 0
        self.speed = [0,0]  # [forward, backward]
        self.vertical = [8,8,7,7,6,6,5,5,4.5,4.5,4.5,4.5,3.5,2.5,2.5,2,1.5,1.5,1,1]

    def update(self):
        self.rect.x += self.speedCalc() #calculate sprite direction and speed
        if self.falling:  #gravity increases velocity
            self.rect.y += self.vertical[19-self.fallTimer]
            self.fallTimer += 1
            if self.fallTimer > len(self.vertical) - 1:
                self.fallTimer = len(self.vertical) - 1
        if self.forward:  #speeds up sprite in right direction
            self.speedControl()
            self.animate()
        elif self.speed[0] is not 0: #decelerate in forward direction
            self.speed[0] -= .35
            if self.speed[0] < 0:
                self.speed[0] = 0
        if self.backward: #speeds up sprite in left direction
            self.speedControl()
            self.animate()
        elif self.speed[1] is not 0:  #decelerate in backward direction
            self.speed[1] -= .35
            if self.speed[1] < 0:
                self.speed[1] = 0
        if not self.forward and not self.backward:  #sprite at rest
            self.resting()
        if self.jump == True and self.jumpTimer < self.jumpThreshold:  #upward arc
            self.rect.y -= self.vertical[self.jumpTimer]
            self.jumpTimer += 1
        elif self.jump == True:  #downward arc
            self.falling = True
            self.jump = False
            self.jumpTimer = 0  # reset timer
            self.jumpThreshold = 20
        if self.jump == False: #constant downward pull
            self.falling = True

        # Print properties
        #self.printSpecProperties()

    #Returns difference between forward and backward speeds
    def speedCalc(self):
        return self.speed[0] - self.speed[1]

    #Sprite acceleration
    def speedControl(self):
        if self.forward and self.speed[1] == 0: #speedup if no backward momentum
            self.speed[0] += .25
            if self.speed[0] > 4:
                self.speed[0] = 4
        if self.backward and self.speed[0] == 0: #speedup if no forward momentum
            self.speed[1] += .25
            if self.speed[1] > 4:
                self.speed[1] = 4

    def animate(self):
        self.step += 1
        if self.step > 39:
            self.step = 0
        self.image = self.animations[int(self.step/10)]

    def resting(self):
        self.image = self.resting_spec

    #Print spec properties from spec.update()
    def printSpecProperties(self):
        print ("self.speed[0]: ", self.speed[0])
        print ("self.speed[1]: ", self.speed[1])
        print("Speed: " + str(self.speedCalc()))
        print("FWD: " + str(self.forward))
        print("BWD: " + str(self.backward))
        print()
