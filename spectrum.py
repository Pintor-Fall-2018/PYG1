# Spectrum.py
import pygame, sys, os
from menu import *

RESOLUTION = (600, 400)  # width x height
FRAMES = 60   # Frames per second
TITLE = "Spectrum v1.0"
DEBUG = 1   #Debug Mode 1 == On 0 == Off

pygame.init()
pygame.display.set_caption(TITLE)
time = pygame.time.Clock()


class Game:
    def __init__(self):
        #sets up screen resolution
        self.status = True
        self.screen = pygame.display.set_mode(RESOLUTION, pygame.RESIZABLE)
        pass

    def startup(self):
        pass

    def shutdown(self):
        pygame.quit()
        sys.exit()

    def drawScreen(self, sprites):
        self.screen.fill((255,255,255))
        sprites.draw(self.screen)
        pygame.display.flip()

    def getCommands(self, events):
        for event in events:
            if event.type == pygame.QUIT:       #check if QUIT event. Return status false to terminate game
                self.status = False
            else:
                self.status = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    spec.rect.x += 5

    def updateSprites(self):
        pass

    def checkStatus(self, events):
        pass


class Spec(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #sprite constructor
        self.image = pygame.Surface((20,20)) #width x height
        self.image.fill((100,100,0))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 200



game = Game()
menu = Menu(game.screen, RESOLUTION[0], RESOLUTION[1], time, FRAMES)
spec = Spec()

sprites = pygame.sprite.Group()
sprites.add(spec)

menu.startScreen()
game.startup()

active = True

while(active):
    #increment time
    time.tick(FRAMES)

    events = pygame.event.get()
    game.checkStatus(events)
    active = game.status #check if game is still active based on game status

    #obtain keyboard inputs
    game.getCommands(events)

    #update sprites
    game.updateSprites()

    #print to screen
    game.drawScreen(sprites)

    #debugging info
    if DEBUG:
        if len(events) > 0:
            print(events)



game.shutdown()
