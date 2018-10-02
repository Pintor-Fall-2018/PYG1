import pygame
from settings import *
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
        self.quitText = "Press Escape to quit"
        self.helpText = "Press H to access help tutorial"


    def startScreen(self):
        textSize = 50
        self.generateText(self.screen, self.titleText, WHITE, textSize,
        (self.width/2), (int(self.height/4)) )
        self.generateText(self.screen, self.authors, WHITE, 20,
        (self.width/2), (int(self.height/2)) )
        self.generateText(self.screen, self.promptMsg, WHITE, 24,
        (self.width/2), (int(self.height/1.5)) )

        pygame.display.flip()
        self.runMenu()

    def pauseScreen(self):
        self.screen.fill((0,0,0))
        pygame.draw.rect(self.screen, RED, (350, 250, 100, 50))
        pygame.draw.rect(self.screen, GREEN,(150, 250, 100, 50))
        pygame.display.flip()
        self.runPauseMenu()

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

    def button(self, text, active_color, inactive_color, width, height, x_coord, y_coord):
        mouse_pos = pygame.mouse.get_pos()
        outline = pygame.Rect(x_coord, y_coord, width, height)
        btn_click = pygame.mouse.get_pressed()
        if x_coord < mouse_pos[0] < (x_coord + width) and y_coord < mouse_pos[1] < (y_coord + height):
            #draw.rect(x, y, width, height)
            pygame.draw.rect(self.screen, active_color,
                            (x_coord, y_coord, width, height))
            pygame.draw.rect(self.screen, WHITE, outline, 5)
            if btn_click[0] == 1:
                return True
        else:
            pygame.draw.rect(self.screen, inactive_color,
                            (x_coord, y_coord, width, height))
            pygame.draw.rect(self.screen, WHITE, outline, 5)
        self.generateText(self.screen, text, BLACK, 20, (x_coord + 50), (y_coord + 10))

    def runPauseMenu(self):
        openMenu = True
        menuFPS = 20
        while openMenu:
            self.time.tick(menuFPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            mouse_pos = pygame.mouse.get_pos()
            btnWidth = 100
            btnHeight = 50
            resume_btn_x = 150
            resume_btn_y = 250
            quit_btn_x = 350
            quit_btn_y = 250
            resume = self.button("Resume", LIGHT_GREEN, GREEN, btnWidth, btnHeight, resume_btn_x, resume_btn_y)
            if resume:
                openMenu = False
            quit = self.button("Quit", LIGHT_RED, RED, btnWidth, btnHeight, quit_btn_x, quit_btn_y)
            if quit:
                pygame.quit()
            pygame.display.flip()


    def gameoverScreen(self):
        pass

    def generateText(self, textWindow, text, color,  textSize, x_coord, y_coord):
        antialias = True
        font = pygame.font.Font(self.fontName, textSize)
        textDisplay = font.render(text, antialias, color)
        textRect = textDisplay.get_rect()
        textRect.midtop = (x_coord, y_coord)
        textWindow.blit(textDisplay, textRect)
