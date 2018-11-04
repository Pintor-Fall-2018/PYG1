import pygame, sys, os
from settings import *
import random as rand
import time
class Menu:
    def __init__(self, screen, time, images):
        """
        Description: Initiates Menu Class Instance... to be continued
        """
        self.screen = screen
        self.time = time
        self.fps = FRAMES
        self.images = images
        self.volume = MUSIC_VOL
        self.fontName = pygame.font.match_font('arial')
        self.titleFont = os.path.join("fonts", "VT323-Regular.ttf")
        self.fontPM = os.path.join("fonts", "PermanentMarker-Regular.ttf")
        self.titleText = "Spectrum"
        self.authors = "(c) 2018 Jarret Edelen, Shane Klumpp, and Tiffany Warner"
        self.quitText = "Press Escape to quit"
        self.helpText = "Press H to access help tutorial"
        self.volumeBarImgs = images[3:7]
        self.bl_light = images[0]
        self.bl_light.set_colorkey(BLACK)
        self.rd_light = images[1]
        self.rd_light.set_colorkey(BLACK)
        self.gr_light = images[2]
        self.gr_light.set_colorkey(BLACK)
        self.bl_x_y_Spawn = (-30, 100)
        self.rd_x_y_Spawn = (-30, 250)
        self.gr_x_y_Spawn = (WIDTH + 30, 50)
        self.fullScreen = False

    def startScreen(self):
        """
        Description: Generates the start screen and loops
                     until user clicks start or closes the window
        Returns: x and y coordinates of the light
        """
        openMenu = True

        frame_img = self.images[-1]
        frame_img.set_colorkey(BLACK)

        play_btn_inactive = self.images[7]
        play_btn_inactive.set_colorkey(BLACK)

        play_btn_active = self.images[8]
        play_btn_active.set_colorkey(BLACK)

        # Faster y-speed gives lights "bouncy" effect
        x_speed, y_speed = (3, 8)

        # Get Spawn Points for each light
        bl_x, bl_y = self.bl_x_y_Spawn
        rd_x, rd_y = self.rd_x_y_Spawn
        gr_x, gr_y = self.gr_x_y_Spawn
        pygame.mixer.music.load(MENU_BG_MUSIC)
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play(-1) # -1 = loop the song

        # Begin loop for animations
        while openMenu:
            # Cover old screen
            self.screen.fill(BLACK)

            # Generate text
            self.generateText(self.titleText, self.titleFont , WHITE, 100,
            (int(WIDTH/2)), (int(HEIGHT/4)) )
            self.generateText(self.authors, self.fontName, WHITE, 16,
            (int(WIDTH/2.1)), (int(HEIGHT/1.2)) )

            # Generate start button
            start_x = (int(WIDTH/2))
            start_y = (int(HEIGHT/1.8))
            start = self.button(LIGHT_GREEN, GRAY, 200, 50, (start_x, start_y) )
            self.generateText("Start", self.fontName, BLACK, 30, start_x, start_y)

            if DEBUG_MENU:
                print("Tick")

            self.time.tick(FRAMES)

            # Check boundaries for lights
            bl_x, bl_y = self.checkBoundaries("blue", (bl_x, bl_y), self.bl_x_y_Spawn)
            rd_x, rd_y = self.checkBoundaries("red", (rd_x, rd_y), self.rd_x_y_Spawn)
            gr_x,gr_y = self.checkBoundaries("green", (gr_x, gr_y), self.gr_x_y_Spawn)

            # Green light is still jumping in the middle of the screen at times.
            # Debug later
            if DEBUG_MENU:
                print(gr_x, gr_y)

            # play_active = self.checkMousePos((WIDTH/2 - 125, start_y - 20), 250, 51)
            # play = self.checkMouseClicks((WIDTH/2 - 125, start_y - 20), 250, 51)
            # if play or play_active:
            #     self.screen.blit(play_btn_active, (WIDTH/2 -125, start_y - 20))
            # else:
            #     self.screen.blit(play_btn_inactive, (WIDTH/2 -125, start_y - 20))
            # self.generateText("PLAY", self.fontName, WHITE, 20, WIDTH/2, start_y)
            # Display the light changes
            self.screen.blit(self.bl_light, (bl_x, bl_y))
            self.screen.blit(self.rd_light, (rd_x, rd_y))
            self.screen.blit(self.gr_light, (gr_x, rd_y))
            self.screen.blit(self.images[-1], (0, 0))


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
        time.sleep(0.1)



    def mainMenu(self, game):
        lvl_btn_w = 160
        lvl_btn_h = 120
        btn_w = 220
        btn_h = 60
        bl_lvl_coords = (int(WIDTH/6), int(HEIGHT/5))
        gr_lvl_coords = (int(WIDTH/2), int(HEIGHT/5))
        rd_lvl_coords = (int(WIDTH/1.2), int(HEIGHT/5))

        # Variable that holds which level has been selected. Set by button select
        self.levelSelectButton = ""

        # Get volume images
        vol_slider = self.volumeBarImgs[0]
        vol_bar = self.volumeBarImgs[1]
        vol_arr_right = self.volumeBarImgs[2]
        vol_arr_left = self.volumeBarImgs[3]

        #Full screen button images
        fs_btn_inactive = self.images[9]
        fs_btn_inactive.set_colorkey(BLACK)

        fs_btn_active = self.images[10]
        fs_btn_active.set_colorkey(BLACK)

        #Bar is 200 pixels wide
        vol_bar_coords = (int(WIDTH/10), int(HEIGHT/1.6))

        #Slider 15 x 40
        vol_slider_coords = [vol_bar_coords[0] + 90, vol_bar_coords[1] - 7]
        vol_arr_right_coords = (vol_bar_coords[0] + 190, vol_bar_coords[1] - 5)
        vol_arr_left_coords = (vol_bar_coords[0] - 20, vol_bar_coords[1]- 3)

        fs_coords = [int(WIDTH/2.5), int(HEIGHT/1.23)]
        fs_img_size = (25, 26)

        skylevel_inactive = self.images[11]
        skylevel_active = self.images[12]

        openMenu = True

        while openMenu:
            self.time.tick(FRAMES)
            # Cover old screen
            self.screen.fill(MAINMENU_BG)
            # Check for events to see if user closed window
            for event in pygame.event.get(pygame.QUIT):
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Colored level panels for main menu
            # Generate text over button based on level completion checkStatus
            #---Blue----
            blue = self.button(LIGHT_BLUE, PASTEL_BLUE, lvl_btn_w, lvl_btn_h, bl_lvl_coords, True, PASTEL_BLUE_2)
            sky_rect = skylevel_inactive.get_rect()
            sky_rect.center = bl_lvl_coords
            bl_lvl_active = self.checkMousePos((int(bl_lvl_coords[0]/4),int(bl_lvl_coords[1]/4)) , lvl_btn_w, lvl_btn_h)
            if bl_lvl_active:
                self.screen.blit(skylevel_active, sky_rect)
            else:
                self.screen.blit(skylevel_inactive, sky_rect)
            self.btnOutline(sky_rect, WHITE, 5)

            if game.checkLightAcquired("blue"):
                self.generateText("COMPLETED", self.fontPM, BLACK, 30, (int(WIDTH/6)), (int(HEIGHT/5)))
            else:
                self.generateText("PLAY", self.fontPM, BLACK, 30, (int(WIDTH/6)), (int(HEIGHT/5)))

            #---Green----
            green = self.button(LIGHT_GREEN, GREEN, lvl_btn_w, lvl_btn_h, gr_lvl_coords, True, DARK_GREEN)
            if game.checkLightAcquired("green"):
                self.generateText("COMPLETED", self.fontPM, BLACK, 30, (int(WIDTH/2)), (int(HEIGHT/5)))
            else:
                self.generateText("PLAY", self.fontPM, BLACK, 30, (int(WIDTH/2)), (int(HEIGHT/5)))
            #---Red----
            red = self.button(LIGHT_RED, RED, lvl_btn_w, lvl_btn_h, rd_lvl_coords, True, DARK_RED)
            if game.checkLightAcquired("red"):
                self.generateText("COMPLETED", self.fontPM, BLACK, 30, (int(WIDTH/1.2)), (int(HEIGHT/5)))
            else:
                self.generateText("PLAY", self.fontPM, BLACK, 30, (int(WIDTH/1.2)), (int(HEIGHT/5)))

            tutorial = self.button(WHITE, GRAY, btn_w, btn_h, (int(WIDTH/1.3), HEIGHT/1.6) )
            self.generateText("Tutorial", self.fontPM, BLACK, 30, (int(WIDTH/1.3)), int(HEIGHT/1.6))

            quit = self.button(WHITE, GRAY, btn_w, btn_h, (int(WIDTH/1.3), HEIGHT/1.2) )
            self.generateText("Quit", self.fontPM, BLACK, 30, (int(WIDTH/1.3)), int(HEIGHT/1.2))

            #Set up full-screen button
            # fullScreen_active = self.checkMousePos((fs_coords[0], fs_coords[1]), fs_img_size[0], fs_img_size[1])
            fullScreen_clicked = self.checkMouseClicks((fs_coords[0], fs_coords[1]), fs_img_size[0], fs_img_size[1])
            time.sleep(0.1)
            if fullScreen_clicked and self.fullScreen is False:
                self.fullScreen = True
            elif fullScreen_clicked and self.fullScreen is True:
                self.fullScreen = False

            if self.fullScreen is False:
                self.screen.blit(fs_btn_inactive, (fs_coords[0], fs_coords[1]))
            else:
                self.screen.blit(fs_btn_active, (fs_coords[0], fs_coords[1]))

            self.generateText("FullScreen:", self.fontPM, WHITE, 30, (int(WIDTH/5)), int(HEIGHT/1.2))
            coords = (int(WIDTH/4), int(HEIGHT/1.2))
            fullS_btn = self.checkMouseClicks(coords, btn_w, btn_h)

            #Load Volume bar
            self.generateText("Volume:", self.fontPM, WHITE, 30, vol_bar_coords[0] + 30, vol_bar_coords[1] - 30)
            self.screen.blit(vol_bar, vol_bar_coords)
            self.screen.blit(vol_slider, vol_slider_coords)
            self.screen.blit(vol_arr_right, vol_arr_right_coords)
            self.screen.blit(vol_arr_left, vol_arr_left_coords)

            vol_inc = self.checkMouseClicks(vol_arr_right_coords, 40, 41)
            vol_dec = self.checkMouseClicks(vol_arr_left_coords, 40, 41)

            # Volume starts at 0.5 - can click 4 times to the right
            #If user increases volume
            if vol_inc:
                vol_slider_coords[0] += 5
                self.volume = self.volume + 0.1
                if vol_slider_coords[0] > vol_bar_coords[0] + 160:
                    vol_slider_coords[0] = vol_bar_coords[0] + 160
                    self.volume = 2.0
                if self.volume > 2.0:
                    self.volume = 2.0
                pygame.mixer.music.set_volume(self.volume)
                vol_inc = False

            #If user decreases volume
            if vol_dec:
                vol_slider_coords[0] -= 5
                self.volume = self.volume - 0.1
                #print("Slider x:", vol_slider_coords[0])
                #print("Bar x:", vol_bar_coords[0])
                if vol_slider_coords[0] < vol_bar_coords[0] + 20:
                    vol_slider_coords[0] = vol_bar_coords[0] + 20
                    self.volume = 0
                if self.volume < 0:
                    self.volume = 0
                #print("Volume:", self.volume)
                pygame.mixer.music.set_volume(self.volume)
                vol_dec = False

            pygame.display.flip()

            if quit:
                pygame.quit()
                sys.exit()

            if tutorial:
                self.tutorialScreen()
                #print ("Back in main menu loop from tutorial")
                tutorial = False

            if blue:
                self.levelSelectButton = "BLUE"
                openMenu = False
            if green:
                self.levelSelectButton = "GREEN"
                openMenu = False
            if red:
                self.levelSelectButton = "RED"
                openMenu = False

        pygame.mixer.music.stop() #Stop menu music
        time.sleep(0.1)
        return self.volume, self.fullScreen, self.levelSelectButton


    def tutorialScreen(self):
        btn_w = 180
        btn_h = 40
        openMenu = True
        quit = False
        title_coords = (int(WIDTH/2), int(HEIGHT/6))
        main_menu_coords = ((int(WIDTH/1.3), int(HEIGHT/3)))
        quit_coords = ((int(WIDTH/1.3), int(HEIGHT/2)))
        obj_title_coords = ((int(WIDTH/5.5), int(HEIGHT/4)))
        obj1_coords = ((int(WIDTH/4), int(HEIGHT/3)))
        obj2_coords = ((int(WIDTH/3.5), int(HEIGHT/2.6)))
        obj3_coords = ((int(WIDTH/4), int(HEIGHT/2.3)))
        obj4_coords = ((int(WIDTH/4), int(HEIGHT/2.1)))
        control_title_coords = ((int(WIDTH/6), int(HEIGHT/1.7)))
        ctrl1_coords = ((int(WIDTH/5.5), int(HEIGHT/1.5)))
        ctrl2_coords = ((int(WIDTH/5.5), int(HEIGHT/1.4)))
        ctrl3_coords = ((int(WIDTH/5.5), int(HEIGHT/1.3)))
        obj1 = "Spec travels the world in search of light!"
        obj2 = "Help Spec navigate through this perilous world"
        obj3 = "and acquire the blue, red, and green light"
        obj4 =" to save... the light of the world"
        control1 ="Left Arrow = Move Left"
        control2 ="Right Arrow = Move Right"
        control3 ="Up Arrow = Jump"
        textList = ["Tutorial", "Main Menu", "Quit", "Objectives:", "Controls:", obj1, obj2, obj3, obj4, control1, control2, control3]
        textCoords = [title_coords, main_menu_coords, quit_coords, obj_title_coords, control_title_coords, obj1_coords, obj2_coords, obj3_coords, obj4_coords, ctrl1_coords, ctrl2_coords, ctrl3_coords]
        instr_attr = (WHITE, 16, self.fontName)
        textAttr = [(WHITE, 40, self.titleFont), (BLACK, 20, self.fontName), (BLACK, 20, self.fontName), (WHITE, 20, self.fontName), (WHITE, 20, self.fontName), instr_attr, instr_attr, instr_attr, instr_attr, instr_attr, instr_attr, instr_attr]
        btnList = [(btn_w, btn_h), (btn_w, btn_h)]
        btnCoords = [main_menu_coords, quit_coords]
        btnColor = [(WHITE, GRAY), (WHITE, GRAY)]
        btnActions = ["menu", "quit"]

        self.runMenuLoop(20, textList, textCoords, textAttr, btnList, btnCoords, btnColor, btnActions)
        time.sleep(0.1)

    def completeLevel(self):
        start_time = time.time()
        openMenu = True

        while openMenu:
            end_time = time.time()
            self.time.tick(FRAMES)
            # Cover old screen
            self.screen.fill(MAINMENU_BG)
            # Check for events to see if user closed window
            for event in pygame.event.get(pygame.QUIT):
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.generateText("Level Completed!", self.fontName, WHITE, 30, (int(WIDTH/2)), int(HEIGHT/3))

            self.generateText("Good job!", self.fontName, WHITE, 30, (int(WIDTH/2)), int(HEIGHT/2.2))

            pygame.display.flip()

            if (end_time - start_time) > 3:
                openMenu = False

    def gameOverScreen(self):
        start_time = time.time()
        openMenu = True

        while openMenu:
            end_time = time.time()
            self.time.tick(FRAMES)
            # Cover old screen
            self.screen.fill(MAINMENU_BG)
            # Check for events to see if user closed window
            for event in pygame.event.get(pygame.QUIT):
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.generateText("Oh no! Spec died...", self.fontName, WHITE, 30, (int(WIDTH/2)), int(HEIGHT/3))

            self.generateText("Game Over", self.fontName, WHITE, 30, (int(WIDTH/2)), int(HEIGHT/2.2))

            pygame.display.flip()

            if (end_time - start_time) > 3:
                openMenu = False

    def gameCompletedScreen(self):

        text1 = "YOU WON OMG"
        text2 = "PLAY ME AGAIN? I BET YOU WON'T"
        menuFPS = 20
        btn_w = 220
        btn_h = 60
        replay_coords = (int(WIDTH/2)), int(HEIGHT/1.8)
        quit_coords = (int(WIDTH/2)), int(HEIGHT/1.2)

        textList = [text1, text2, "Replay Game", "Quit"]
        textCoords = [((int(WIDTH/2)), int(HEIGHT/5)), \
                      ((int(WIDTH/2)), int(HEIGHT/3)), \
                      ((int(WIDTH/2)), int(HEIGHT/1.8)), \
                      ((int(WIDTH/2)), int(HEIGHT/1.2))]
        textAttr = [(WHITE, 30, self.fontName), \
                    (WHITE, 30, self.fontName), \
                    (BLACK, 30, self.fontName), \
                    (BLACK, 30, self.fontName)]
        btnList = [(btn_w, btn_h), (btn_w, btn_h)]
        btnCoords = [replay_coords, quit_coords]
        btnColors = [(LIGHT_GREEN, GRAY), (LIGHT_RED, GRAY)]
        btnActions = ["replay", "quit"]

        status = self.runMenuLoop(menuFPS, textList, textCoords, textAttr, btnList, btnCoords, btnColors, btnActions)
        time.sleep(0.1)
        return status



    def checkMouseClicks(self, start_coords, width, height):
        """
        #Check for mouse clicks within defined area.
        #Set a start x, y, ar right top corner of area.
        # Will check boundaries for width, height.
        """
        x, y = start_coords
        mouse_pos = pygame.mouse.get_pos()
        btn_click = pygame.mouse.get_pressed()

        if( x < mouse_pos[0] < x + width and
            y < mouse_pos[1] < y + height
            ):
            if btn_click[0] == 1:
                return True
        return False

    def checkMousePos(self, start_coords, width, height):
        x, y = start_coords
        mouse_pos = pygame.mouse.get_pos()

        if( x < mouse_pos[0] < x + width and
            y < mouse_pos[1] < y + height
            ):
            return True
        return False

    def checkBoundaries(self, lightColor, curCoords, spawnCoords):
        """
        Description: Checks if lights have surpassed screen boundaries and
                     resets the x and y coordinates of the lights to the
                     spawn point as needed.
        Returns: x and y coordinates of the light
        """
        x, y = curCoords
        if lightColor == "red" or lightColor == "blue":
            if x > RESOLUTION[0] + 100:
                 x = spawnCoords[0]
                 y = spawnCoords[1]
            if y > RESOLUTION[1] + 100 or y < -100:
                 x = spawnCoords[0]
                 y = spawnCoords[1]
        else:
            if x < -30:
                x = spawnCoords[0]
                y = spawnCoords[1]
            if y > RESOLUTION[1] + 100 or y < (-1 * (RESOLUTION[1] + 30)):
                x = spawnCoords[0]
                y = spawnCoords[1]
        return (x, y)

    def updateLightPos(self, startPath, x_speed, y_speed, x, y):
        """
        Description: Updates animated light position on start screen
        Returns: Updated x and y coordinates
        """
        if startPath == "right":
            x += x_speed
        if startPath == "left":
            x -= x_speed
        y += rand.randrange(-10, y_speed)
        return (x, y)

    def pauseScreen(self):
        """
        Description: Generates the pause screen
        """
        paused_coords = (int(WIDTH/2), int(HEIGHT/4))
        openMenu = True
        menuFPS = 20
        btn_w = 220
        btn_h = 60
        resume_coords = (int(WIDTH/2)), int(HEIGHT/1.8)
        quit_coords = (int(WIDTH/2)), int(HEIGHT/1.2)
        textList = ["Paused", "Resume", "Main Menu"]
        textCoords = [paused_coords, resume_coords, quit_coords]
        textAttr = [(WHITE, 100, self.titleFont), (BLACK, 30, self.fontPM), (BLACK, 30, self.fontPM)]
        btnList = [(btn_w, btn_h), (btn_w, btn_h)]
        btnCoords = [resume_coords, quit_coords]
        btnColors = [(LIGHT_GREEN, GRAY), (LIGHT_RED, GRAY)]
        btnActions = ["resume", "pause_return"]
        status = self.runMenuLoop(menuFPS, textList, textCoords, textAttr, btnList, btnCoords, btnColors, btnActions)
        time.sleep(0.1)
        return status

# fps = integer
# textList = strings to be generated
# textCoords = [(x,y)]
# textAttr = [(color, fontsize, fontName)]
# buttonList = [(width, height)]
# buttonCoords = [(x, y)]
# btnColor = Color
# btnActions = list of strings naming the actions
    def runMenuLoop(self, fps, textList, textCoords, textAttr, buttonList, buttonCoords, btnColors, btnActions):
        openMenu = True
        self.screen.fill(BLACK)
        while openMenu:
            self.time.tick(fps)
            buttons = []
            text = []
            for event in pygame.event.get(pygame.QUIT):
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if len(buttonList) is not 0:
                #print("ButtonList ", buttonList)
                k = 0
                for button in buttonList:
                    buttonName = self.button(btnColors[k][0], btnColors[k][1], buttonList[k][0], buttonList[k][1], buttonCoords[k])
                    buttons.append(buttonName)
                    k += 1

            if len(textList) is not 0:
                k = 0
                for textString in textList:
                    #print("K", k)
                    stringName = self.generateText(textList[k], textAttr[k][2], textAttr[k][0], textAttr[k][1], textCoords[k][0], textCoords[k][1])
                    text.append(stringName)
                    k += 1

            if len(btnActions) is not 0:
                #Check status of quit button
                k = 0
                for btn in btnActions:
                    #print("Button", btn)
                    if btn == "resume":
                        if buttons[k] == True:
                            openMenu = False
                    if btn == "quit":
                        if buttons[k] == True:
                            openMenu = False
                            pygame.quit()
                            sys.exit()
                    if btn == "menu":
                        if buttons[k] == True:
                            openMenu = False
                    if btn == "pause_return":
                        if buttons[k] == True:
                            return "restart"
                    if btn == "replay":
                        if buttons[k] == True:
                            return "replay"
                    k += 1
            pygame.display.flip()
            text = []
            buttons = []
            pygame.event.clear

    # ---------------------------------------------------------------
    # The following code to create a button was made based on this
    # reference: https://pythonprogramming.net/pygame-button-function/
    #----------------------------------------------------------------
    def button(self, active_color, inactive_color, width, height, coords, outline=False, outline_color=BLACK):
        """
        Description: Creates a button on the screen that reacts to mouse position
        Parameters: active color = int tuple - Color while mouse is hovering
                    inactive_color = int tuple - Color while mouse is not hovering
                    width = int - button width in pixels
                    height = int - button height in pixels
                    x_coord = int - x position of button on screen
                    y_coord = int - y position of button on screen
        """
        x, y = coords
        mouse_pos = pygame.mouse.get_pos()
        btn_click = pygame.mouse.get_pressed()

        btn = pygame.Surface((width, height))
        btn_rect = btn.get_rect()
        btn_rect.center = (x, y)
        if outline:
            self.btnOutline(btn_rect, outline_color, 5)

        if(
            x - width/2 < mouse_pos[0] < (x + width/2) and
            y - height/2 < mouse_pos[1] < (y + height/2)
         ):
            #draw.rect(x, y, width, height)
            btn.fill(active_color)
            self.screen.blit(btn, btn_rect)
            if btn_click[0] == 1:
                return True
        else:
            btn.fill(inactive_color)
            self.screen.blit(btn, btn_rect)

    def btnOutline(self, btnRect, color, size):
        pygame.draw.rect(self.screen, color, btnRect, size)

    def generateText(self, text, font, color, textSize, x_coord, y_coord):
        """
        Description: Generates text on the screen
        Parameters: text = string - to be generated
                    font = string - font name
                    color = int tuple - indicating rgb color
                    textSize = int - pixel size of text
                    x_coord = int - x position of text on screen
                    y_coord = int - y position of text on screen
        """
        antialias = True
        font = pygame.font.Font(font, textSize)
        textDisplay = font.render(text, antialias, color)
        textRect = textDisplay.get_rect()
        textRect.center = (x_coord, y_coord)
        self.screen.blit(textDisplay, textRect)
