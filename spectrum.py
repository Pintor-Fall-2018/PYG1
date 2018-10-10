# Spectrum.py
import pygame, sys, os
import random
from settings import *
from menu import *


pygame.init()   #initialize imported pygame modules
pygame.display.set_caption(TITLE)
pygame.mouse.set_visible(1)   # Mouse visible == 1
time = pygame.time.Clock()

class Game:
    def __init__(self):
        #sets up screen resolution
        self.status = True
        self.screen = pygame.display.set_mode(RESOLUTION, pygame.RESIZABLE)   #display settings

    def startup(self):
        self.spec = Spec()
        self.sprites = pygame.sprite.Group()
        self.sprites.add(self.spec)
        if DEBUG:
            print('Pygame Version: ' + pygame.version.ver)
            print('Platform: ' + sys.platform)

    def shutdown(self):
        pygame.quit()
        sys.exit()

    def drawScreen(self):
        self.screen.fill(BLACK)
        self.sprites.draw(self.screen)
        pygame.display.flip()

    def getCommands(self):
        #Hold Keys for fluid movement
        for event in pygame.event.get(pygame.KEYDOWN):   # gets events and clears queue
            if event.key == pygame.K_RIGHT:  #273
                self.spec.forward = True
            if event.key == pygame.K_LEFT:   #275
                self.spec.backward = True
            if event.key == pygame.K_UP:
                self.spec.jump = True
            if event.key == pygame.K_ESCAPE:
                menu.pauseScreen()

        for event in pygame.event.get(pygame.KEYUP):
            if event.key == pygame.K_RIGHT:  #273
                self.spec.forward = False
            if event.key == pygame.K_LEFT:   #275
                self.spec.backward = False

    def updateSprites(self):
        self.sprites.update()

        #jump mechanics (crude)
        if self.spec.jump == True and self.spec.jumpTimer > 20:
            self.spec.rect.y -= 5
            self.spec.jumpTimer -= 1
        elif self.spec.jump == True and self.spec.jumpTimer > 0:
            self.spec.rect.y += 5
            self.spec.jumpTimer -= 1
        elif self.spec.jump == True and self.spec.jumpTimer == 0:
            self.spec.jump = False
            self.spec.jumpTimer = 40


    def checkStatus(self):
        if pygame.event.get(pygame.QUIT): #check if QUIT event. Return status false to terminate game
            self.status = False

class Spec(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #sprite constructor
        self.image = pygame.Surface((20,20)) #width x height
        #self.image.fill((100,100,0))
        self.step = 0
        self.resting_img = pygame.image.load('images/spec0.png').convert()
        self.animations = []
        self.animations.append(pygame.image.load('images/spec1.png').convert())
        self.animations.append(pygame.image.load('images/spec2.png').convert())
        self.animations.append(pygame.image.load('images/spec3.png').convert())
        self.animations.append(pygame.image.load('images/spec4.png').convert())
        self.image = self.resting_img
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 200
        self.forward = False
        self.backward = False
        self.jumpTimer = 40
        self.jump = False

    def update(self):
        if self.forward:
            self.rect.x += 5
            self.animate()
        elif self.backward:
            self.rect.x -= 5
            self.animate()
        else:
            self.resting()

    def animate(self):
        self.step += 1
        if self.step > 39:
            self.step = 0
        self.image = self.animations[int(self.step/10)]

    def resting(self):
        self.image = self.resting_img


game = Game()

# Load Menu images
bl_light_img = pygame.image.load('images/blueLight.png').convert()
rd_light_img = pygame.image.load('images/redLight.png').convert()
gr_light_img = pygame.image.load('images/greenLight.png').convert()

menu_imgs = []
menu_imgs.extend((bl_light_img, rd_light_img, gr_light_img))

# Create menu object
menu = Menu(game.screen, time, menu_imgs)

#spec = Spec()

#sprites = pygame.sprite.Group()
#sprites.add(spec)

menu.startScreen()
game.startup()

active = True

# Main Game Loop
while(active):

    #increment time
    time.tick(FRAMES)

    game.checkStatus()
    active = game.status #check if game is still active based on game status

    #obtain keyboard inputs
    game.getCommands()

    #update sprites
    game.updateSprites()

    #print to screen
    game.drawScreen()


game.shutdown()
