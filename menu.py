import pygame
class Menu:
    def __init__(self, screen, window_width, window_height, time, fps):
        self.screen = screen
        self.width = window_width
        self.height = window_height
        self.time = time
        self.fps = fps
        self.fontName = pygame.font.match_font('arial')
        self.titleText = "Spectrum"
        self.authors = "Created by Jarret Edelen, Shane Klumpp, and Tiffany Warner"
        self.promptMsg = "Press Enter to Start"

    def startScreen(self):
        textSize = 50
        self.generateText(self.screen, self.titleText, textSize,
        (self.width/2), (int(self.height/4)) )
        self.generateText(self.screen, self.authors, 20,
        (self.width/2), (int(self.height/2)) )
        self.generateText(self.screen, self.promptMsg, 24,
        (self.width/2), (int(self.height/1.5)) )

        pygame.display.flip()
        self.runMenu()

    def runMenu(self):
        openMenu = True
        while openMenu:
            self.time.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        openMenu = False
    def gameoverScreen(self):
        pass

    def generateText(self, textWindow, text, textSize, x_coord, y_coord):
        antialias = True
        font = pygame.font.Font(self.fontName, textSize)
        textDisplay = font.render(text, antialias, ((255,255,255)))
        textRect = textDisplay.get_rect()
        textRect.midtop = (x_coord, y_coord)
        textWindow.blit(textDisplay, textRect)
