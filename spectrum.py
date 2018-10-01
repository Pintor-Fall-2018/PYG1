# Spectrum.py
import pygame

RESOLUTION = (600, 400)  # width x height

pygame.init()
screen = pygame.display.set_mode(RESOLUTION, pygame.RESIZABLE)



class Menu:
    pass

class Game:
    def __init__(self):
        pass

    def startup(self):
        pass

    def shutdown(self):
        pass


menu = Menu()
game = Game()

menu.
game.startup()

while(1):
    #obtain keyboard inputs
    game.getCommands()

    #update sprites
    game.updateSprites()

    #print to screen
    game.printScreen()


game.shutdown()
