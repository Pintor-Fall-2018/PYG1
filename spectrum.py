# Spectrum.py
import pygame, sys, os
from menu import *

RESOLUTION = (600, 400)  # width x height
FRAMES = 60   # Frames per second
TITLE = "Spectrum v1.0"
DEBUG = 0   #Debug Mode 1 == On 0 == Off

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

    def shutdown(self):
        pygame.quit()
        sys.exit()

    def drawScreen(self):
        self.screen.fill((255,255,255))
        self.sprites.draw(self.screen)
        pygame.display.flip()

    def getCommands(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:       #check if QUIT event. Return status false to terminate game
                self.status = False
            else:
                self.status = True
            if event.type == pygame.KEYDOWN:        #Hold Keys for fluid movement
                if event.key == pygame.K_RIGHT:
                    self.spec.forward = True
                if event.key == pygame.K_LEFT:
                    self.spec.backward = True
                if event.key == pygame.K_UP:
                    self.spec.jump = True
                if event.key == pygame.K_ESCAPE:
                    menu.pauseScreen()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.spec.forward = False
                if event.key == pygame.K_LEFT:
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
        pass


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
        print(self.step)
        self.step += 1
        if self.step > 39:
            self.step = 0
        self.image = self.animations[int(self.step/10)]

    def resting(self):
        self.image = self.resting_img


game = Game()
menu = Menu(game.screen, RESOLUTION[0], RESOLUTION[1], time, FRAMES)
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

    #debugging info
    if DEBUG:
        if len(events) > 0:
            print(events)



game.shutdown()
