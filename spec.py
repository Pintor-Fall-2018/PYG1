import pygame

class Spec(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #sprite constructor
        #self.image = pygame.Surface((20,20)) #width x height
        #self.image.fill((100,100,0))
        self.step = 0
        self.resting_spec = pygame.image.load('images/spec0.png').convert()
        self.resting_spec_powerup = pygame.image.load('images/spec_powerup_animations/spec0_powerup.png').convert()
        self.resting_spec.set_colorkey([34,177,76])
        self.resting_spec_powerup.set_colorkey([34,177,76])
        self.animations = []
        self.animations.append(pygame.image.load('images/spec1.png').convert())
        self.animations.append(pygame.image.load('images/spec2.png').convert())
        self.animations.append(pygame.image.load('images/spec3.png').convert())
        self.animations.append(pygame.image.load('images/spec4.png').convert())
        for animation in self.animations:
            animation.set_colorkey([34,177,76])
        self.animations_powerup = []
        self.animations_powerup.append(pygame.image.load('images/spec_powerup_animations/spec1_powerup.png').convert())
        self.animations_powerup.append(pygame.image.load('images/spec_powerup_animations/spec2_powerup.png').convert())
        self.animations_powerup.append(pygame.image.load('images/spec_powerup_animations/spec3_powerup.png').convert())
        self.animations_powerup.append(pygame.image.load('images/spec_powerup_animations/spec4_powerup.png').convert())
        for animation_powerup in self.animations_powerup:
            animation_powerup.set_colorkey([34,177,76])
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
        self.shadow = {"top":0.0, "bottom":0.0, "left":0.0, "right":0.0}

    def update(self, powerUp, sprites, mobs):
        self.snapShot()  #capture position from last frame
        self.rect.x += self.speedCalc() #calculate sprite direction and speed
        if self.falling:  #gravity increases velocity
            self.rect.y += self.vertical[19-self.fallTimer]
            self.fallTimer += 1
            if self.fallTimer > len(self.vertical) - 1:
                self.fallTimer = len(self.vertical) - 1
        if self.forward:  #speeds up sprite in right direction
            self.speedControl(powerUp)
            self.animate(powerUp)
        elif self.speed[0] is not 0: #decelerate in forward direction
            self.speed[0] -= .35
            if self.speed[0] < 0:
                self.speed[0] = 0
        if self.backward: #speeds up sprite in left direction
            self.speedControl(powerUp)
            self.animate(powerUp)
        elif self.speed[1] is not 0:  #decelerate in backward direction
            self.speed[1] -= .35
            if self.speed[1] < 0:
                self.speed[1] = 0
        if not self.forward and not self.backward:  #sprite at rest
            self.resting(powerUp)
        if self.jump == True and self.jumpTimer < self.jumpThreshold:  #upward arc
            self.rect.y -= self.vertical[self.jumpTimer]
            self.jumpTimer += 1
        elif self.jump == True:  #downward arc
            self.falling = True
            self.jump = False
            self.jumpTimer = 0  # reset timer
            self.jumpThreshold = 20

        # Print properties
        #self.printSpecProperties()

    #Returns difference between forward and backward speeds
    def speedCalc(self):
        return self.speed[0] - self.speed[1]

    #Sprite acceleration
    def speedControl(self, powerUp):
        if powerUp == True:
            print("Using Power Up")
            if self.forward and self.speed[1] == 0: #speedup if no backward momentum
                self.speed[0] += .4
                if self.speed[0] > 6:
                    self.speed[0] = 6
            if self.backward and self.speed[0] == 0: #speedup if no forward momentum
                self.speed[1] += .4
                if self.speed[1] > 6:
                    self.speed[1] = 6
        else:
            if self.forward and self.speed[1] == 0: #speedup if no backward momentum
                self.speed[0] += .25
                if self.speed[0] > 4:
                    self.speed[0] = 4
            if self.backward and self.speed[0] == 0: #speedup if no forward momentum
                self.speed[1] += .25
                if self.speed[1] > 4:
                    self.speed[1] = 4

    def animate(self, powerUp):
        self.step += 1
        if self.step > 39:
            self.step = 0
        if powerUp == True:
            self.image = self.animations_powerup[int(self.step/10)]
        else:
            self.image = self.animations[int(self.step/10)]

    def resting(self, powerUp):
        if powerUp == True:
            self.image = self.resting_spec_powerup
        else:
            self.image = self.resting_spec

    #captures position of last frame into dictionary
    def snapShot(self):
        self.shadow["top"] = self.rect.top
        self.shadow["bottom"] = self.rect.bottom
        self.shadow["right"] = self.rect.right
        self.shadow["left"] = self.rect.left

    #Print spec properties from spec.update()
    def printSpecProperties(self):
        print ("self.speed[0]: ", self.speed[0])
        print ("self.speed[1]: ", self.speed[1])
        print("Speed: " + str(self.speedCalc()))
        print("FWD: " + str(self.forward))
        print("BWD: " + str(self.backward))
        print()
