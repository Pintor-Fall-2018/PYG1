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
        # Create Groups()
        self.sprites = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()

        # Create Game Objects and add to their Groups()
        self.spec = Spec()
        self.sprites.add(self.spec)

        #Initialize blocks by picking from BLOCK_LIST to use from settings and add to Groups
        for block in BLOCK_LIST:
            b = Block(*block) # explode list from block in BLOCK_LIST
            self.sprites.add(b)
            self.blocks.add(b)


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

        collisions = pygame.sprite.spritecollide(self.spec, self.blocks, False)
        if len(collisions) != 0:
            self.spec.falling = False
            if DEBUG:
                print(collisions)
        else:
            if self.spec.jump == False:
                self.spec.falling = True

        # Scrolling happens in the updateSprites part of game
        if self.spec.rect.x == WIDTH - 50:
            #self.spec.rect.y -= 100
            self.spec.rect.x -= 50
            #self.block.rect.y -=100
            for block in self.blocks:
                block.rect.x -= 50

        self.timeSinceInit = pygame.time.get_ticks()
        if self.timeSinceInit % 1000 == 0:
            print("time: ", self.timeSinceInit)


    def checkStatus(self):
        if pygame.event.get(pygame.QUIT): #check if QUIT event. Return status false to terminate game
            self.status = False

class Spec(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #sprite constructor
        self.image = pygame.Surface((20,20)) #width x height
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
        self.forward = False
        self.backward = False
        self.falling = True
        self.jumpTimer = 40
        self.jump = False

    def update(self):
        if self.falling:
            self.rect.y += 5
        if self.forward:
            self.rect.x += 5
            self.animate()
        elif self.backward:
            self.rect.x -= 5
            self.animate()
        else:
            self.resting()

        #jump mechanics (crude)
        if self.jump == True and self.jumpTimer > 20:
            self.rect.y -= 5
            self.jumpTimer -= 1
        elif self.jump == True and self.jumpTimer > 0:
            self.falling = True
            self.jump = False
            self.jumpTimer = 40


    def animate(self):
        self.step += 1
        if self.step > 39:
            self.step = 0
        self.image = self.animations[int(self.step/10)]

    def resting(self):
        self.image = self.resting_spec

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, color):
        pygame.sprite.Sprite.__init__(self) #sprite constructor
        self.image = pygame.Surface([w, h]) #width x height
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


game = Game()

# Load Menu images
bl_light_img = pygame.image.load('images/blueLight.png').convert()
rd_light_img = pygame.image.load('images/redLight.png').convert()
gr_light_img = pygame.image.load('images/greenLight.png').convert()

menu_imgs = []
menu_imgs.extend((bl_light_img, rd_light_img, gr_light_img))

# Create menu object
menu = Menu(game.screen, time, menu_imgs)

menu.startScreen()
game.startup()

active = True

# Main Game Loop
while(active):

    #increment time
    time.tick(FRAMES)
    #print (time.tick(FRAMES)) prints how many frames of seconds has been passed

    game.checkStatus()
    active = game.status #check if game is still active based on game status

    #obtain keyboard inputs
    game.getCommands()

    #update sprites
    game.updateSprites()

    #print to screen
    game.drawScreen()


game.shutdown()
