import pygame, sys, os
from settings import *
import random as rand
class Menu:
    def __init__(self, screen, time, images):
        self.screen = screen
        self.time = time
        self.fps = FRAMES
        self.images = images
        self.fontName = pygame.font.match_font('arial')
        self.titleText = "Spectrum"
        self.authors = "(c) 2018 Jarret Edelen, Shane Klumpp, and Tiffany Warner"
        self.quitText = "Press Escape to quit"
        self.helpText = "Press H to access help tutorial"
        self.bl_light = images[0]
        self.bl_light.set_colorkey(BLACK)
        self.rd_light = images[1]
        self.rd_light.set_colorkey(BLACK)
        self.gr_light = images[2]
        self.gr_light.set_colorkey(BLACK)
        self.bl_x_y_Spawn = (-30, 100)
        self.rd_x_y_Spawn = (-30, 250)
        self.gr_x_y_Spawn = (RESOLUTION[0] + 30, 50)


    def startScreen(self):
        openMenu = True
        # Faster y-speed gives lights "bouncy" effect
        x_speed, y_speed = (3, 8)

        # Get Spawn Points for each light
        bl_x, bl_y = self.bl_x_y_Spawn
        rd_x, rd_y = self.rd_x_y_Spawn
        gr_x, gr_y = self.gr_x_y_Spawn

        # Begin loop for animations
        while openMenu:
            # Cover old screen
            self.screen.fill(BLACK)

            # Generate text
            titleFont = os.path.join("fonts", "VT323-Regular.ttf")
            self.generateText(self.titleText, titleFont , WHITE, 100,
            (int(RESOLUTION[0]/2)), (int(RESOLUTION[1]/8)) )
            self.generateText(self.authors, self.fontName, WHITE, 20,
            (int(RESOLUTION[0]/2)), (int(RESOLUTION[1]/1.2)) )

            if DEBUG_MENU:
                print("Tick")

            self.time.tick(FRAMES)

            # Check boundaries for lights - needs refactoring
            if bl_x > RESOLUTION[0] + 100:
                 bl_x = self.bl_x_y_Spawn[0]
                 bl_y = self.bl_x_y_Spawn[1]
            if bl_y > RESOLUTION[1] + 100 or bl_y < -100:
                 bl_x = self.bl_x_y_Spawn[0]
                 bl_y = self.bl_x_y_Spawn[1]
            if rd_x > RESOLUTION[0] + 100:
                 rd_x = self.rd_x_y_Spawn[0]
                 rd_y = self.rd_x_y_Spawn[1]
            if rd_y > RESOLUTION[1] + 100 or rd_y < -100:
                 rd_x = self.rd_x_y_Spawn[0]
                 rd_y = self.rd_x_y_Spawn[1]
            if gr_x < -30:
                if DEBUG_MENU:
                    print("---------------- GREEN X JUMP!-------------------")
                gr_x = self.gr_x_y_Spawn[0]
                gr_y = self.gr_x_y_Spawn[1]
            if gr_y > RESOLUTION[1] + 100 or gr_y < (-1 * (RESOLUTION[1] + 30)):
                if DEBUG_MENU:
                    print("---------------- GREEN Y JUMP!-------------------")
                gr_x = self.gr_x_y_Spawn[0]
                gr_y = self.gr_x_y_Spawn[1]

            if DEBUG_MENU:
                print(gr_x, gr_y)
            self.screen.blit(self.bl_light, (bl_x,bl_y))
            self.screen.blit(self.rd_light, (rd_x,rd_y))
            self.screen.blit(self.gr_light, (gr_x,rd_y))

            # Generate start button
            start = self.button(LIGHT_GREEN, GRAY, 200, 50, ((int(RESOLUTION[0]/2)) - 100), (int(RESOLUTION[1]/1.8)) )
            self.generateText("Start", self.fontName, BLACK, 30, (int(RESOLUTION[0]/2)), (int(RESOLUTION[1]/1.8))+ 5)

            # Show changes
            pygame.display.flip()
            # Update Light Positions
            bl_x, bl_y = self.updateLightPos("right", x_speed, y_speed, bl_x, bl_y)
            rd_x, rd_y = self.updateLightPos("right", x_speed, y_speed, rd_x, rd_y)
            gr_x, gr_y = self.updateLightPos("left", x_speed, y_speed, gr_x, gr_y)

            # Check for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        openMenu = False
            #Check if start button was pressed
            if start:
                openMenu = False

    def updateLightPos(self, startPath, x_speed, y_speed, x, y):
        if startPath == "right":
            x += x_speed
        if startPath == "left":
            x -= x_speed
        y += rand.randrange(-10, y_speed)
        return (x, y)

    def pauseScreen(self):
        self.screen.fill((0,0,0))
        pygame.draw.rect(self.screen, RED, (350, 250, 100, 50))
        pygame.draw.rect(self.screen, GREEN,(150, 250, 100, 50))
        pygame.display.flip()
        self.runPauseMenu()

    def button(self, active_color, inactive_color, width, height, x_coord, y_coord):
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
            resume = self.button(LIGHT_GREEN, GREEN, btnWidth, btnHeight, resume_btn_x, resume_btn_y)
            self.generateText("Resume", self.fontName, BLACK, 20, resume_btn_x + 50, resume_btn_y + 10)
            if resume:
                openMenu = False
            quit = self.button(LIGHT_RED, RED, btnWidth, btnHeight, quit_btn_x, quit_btn_y)
            self.generateText("Quit", self.fontName, BLACK, 20, quit_btn_x + 50, quit_btn_y + 10)
            if quit:
                pygame.quit()
                sys.exit()        #exit() needed after pygame.quit() fixes video system not initialized issue
            pygame.display.flip()


    def gameoverScreen(self):
        pass

    def generateText(self, text, font, color, textSize, x_coord, y_coord):
        antialias = True
        font = pygame.font.Font(font, textSize)
        textDisplay = font.render(text, antialias, color)
        textRect = textDisplay.get_rect()
        textRect.midtop = (x_coord, y_coord)
        self.screen.blit(textDisplay, textRect)
