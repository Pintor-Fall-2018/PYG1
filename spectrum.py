# Spectrum.py
import pygame, sys, os
import random
from settings import *
from menu import *
from spec import *
from mob import *
from light import *
from map_Blue import *
from map_Green import *
from map_Red import *

# Note: Initialize sound before game to prevent sound lag
#       Especially import for sound effects
# 44100 Hz = Frequency,    -16 = size
# 1 = channels, 2048 = buffersize -- this is what prevents sound lag
pygame.mixer.pre_init(44100, -16, 1, 2048)


pygame.init()   #initialize imported pygame modules
pygame.display.set_caption(TITLE)
pygame.mouse.set_visible(1)   # Mouse visible == 1
time = pygame.time.Clock()


class Game:
    def __init__(self):
        #sets up screen resolution
        self.status = True
        self.screen = pygame.display.set_mode(RESOLUTION, pygame.RESIZABLE)   #display settings
        self.blue_light_acquired = 0
        self.red_light_acquired = 0
        self.green_light_acquired = 0
        self.endCurrentLevel = 0
        self.levelStatus = ""

    def resetGame(self):
        # resets game attributes
        self.blue_light_acquired = 0
        self.red_light_acquired = 0
        self.green_light_acquired = 0
        self.endCurrentLevel = 0
        self.levelStatus = ""

    # Startup function. Responsible for creating the map and all objects
    def startup(self, levelSelect):
        #Create Start Up Game timers and counters
        self.background_x = 0  # rate of background scrolling (calculated at runtime)
        self.block_movement_counter = 0
        self.blockTimer = pygame.time.get_ticks()
        self.whichLevelToPlay = levelSelect # assign map to play based on levelSelect String

        #Background image
        self.background = pygame.image.load('images/background.png').convert()

        # Create Groups()
        self.sprites = pygame.sprite.Group()
        self.sky_blocks = pygame.sprite.Group()             # Moving blocks
        self.ground_blocks = pygame.sprite.Group()          # Ground blocks don't move!
        self.invisible_wall_block = pygame.sprite.Group()   # Invisible wall block (left screen limiter)
        self.all_blocks = pygame.sprite.Group()
        self.lights = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()

        # Create Game Objects and add to their Groups()
        self.spec = Spec()
        self.sprites.add(self.spec)

        # Create Level based on user selection from menu.MainMenu()
        # Levels create level specific map, mobs, EOG light object
        if self.whichLevelToPlay == "BLUE":
            print("game.startUp: starting game.playBlue")
            game.playBlue()
        elif self.whichLevelToPlay == "GREEN":
            print("game.startUp: starting game.playGreen")
            game.playGreen()
        elif self.whichLevelToPlay == "RED":
            print("game.startUp: starting game.playRed")
            game.playRed()
        else:
            print("You shouldn't ever seen this. Level selection ERROR")
            #exit safely
            pygame.quit()
            sys.exit()

        # Initalize left "Invisible" Wall Block
        self.invisible_block = Block(-50, 0, 50, 600, WHITE)
        self.sprites.add(self.invisible_block)
        self.invisible_wall_block.add(self.invisible_block)

        if DEBUG:
            print('Pygame Version: ' + pygame.version.ver)
            print('Platform: ' + sys.platform)

    def playBlue(self):
        print ("game.playBlue: Creating the Sky level")
        # Create Blue Level from tile map
        for row in range(len(bluebox)):
            for column in range(len(bluebox[0])):
                if bluebox[row][column] is not tiles['sky']:
                    if bluebox[row][column] == tiles['earth']:
                        tile = Tile(20 * column, 20 * row, 'images/earth.png')
                        self.sprites.add(tile)
                        self.all_blocks.add(tile)
                        self.ground_blocks.add(tile)
                    elif bluebox[row][column] == tiles['grass']:
                        tile = Tile(20 * column, 20 * row, 'images/grass.png')
                        self.sprites.add(tile)
                        self.all_blocks.add(tile)
                        self.ground_blocks.add(tile)
                    elif bluebox[row][column] == tiles['platform']:
                        tile = Tile(20 * column, 20 * row, 'images/platform.png')
                        self.sprites.add(tile)
                        self.all_blocks.add(tile)
                        self.sky_blocks.add(tile)

        # Create Blue Light Object that wins the blue level and adds it to its Groups()
        self.light = Light(bl_light_endGame_imgs)
        self.sprites.add(self.light)
        self.lights.add(self.light)

        # Set DEBUG_MOBS_NO_SPAWN to 1 to not spawn mobs
        if DEBUG_MOBS_NO_SPAWN:
            print("Playing without mobs")
        else:
            # Create Mobs and add to its Groups()
            for mob in MOBS_SKY_LIST:
                m = Mob(*mob)
                self.sprites.add(m)
                self.mobs.add(m)

    def playGreen(self):
        print ("game.playGreen: Creating the Forest level")
        # Create Green Level from tile map
        for row in range(len(greenbox)):
            for column in range(len(greenbox[0])):
                if greenbox[row][column] is not tiles['sky']:
                    if greenbox[row][column] == tiles['earth']:
                        tile = Tile(20 * column, 20 * row, 'images/earth.png')
                        self.sprites.add(tile)
                        self.all_blocks.add(tile)
                        self.ground_blocks.add(tile)
                    elif greenbox[row][column] == tiles['grass']:
                        tile = Tile(20 * column, 20 * row, 'images/grass.png')
                        self.sprites.add(tile)
                        self.all_blocks.add(tile)
                        self.ground_blocks.add(tile)
                    elif greenbox[row][column] == tiles['platform']:
                        tile = Tile(20 * column, 20 * row, 'images/platform.png')
                        self.sprites.add(tile)
                        self.all_blocks.add(tile)
                        self.sky_blocks.add(tile)

        # Create Green Light Object that wins the green level and adds it to its Groups()
        self.light = Light(green_light_endGame_imgs)
        self.sprites.add(self.light)
        self.lights.add(self.light)

        # Set DEBUG_MOBS_NO_SPAWN to 1 to not spawn mobs
        if DEBUG_MOBS_NO_SPAWN:
            print("Playing without mobs")
        else:
            # Create Mobs and add to its Groups()
            for mob in MOBS_SKY_LIST:
                m = Mob(*mob)
                self.sprites.add(m)
                self.mobs.add(m)

    def playRed(self):
        print ("game.playRed: Creating the Desert level")
        # Create Green Level from tile map
        for row in range(len(redbox)):
            for column in range(len(redbox[0])):
                if redbox[row][column] is not tiles['sky']:
                    if redbox[row][column] == tiles['earth']:
                        tile = Tile(20 * column, 20 * row, 'images/earth.png')
                        self.sprites.add(tile)
                        self.all_blocks.add(tile)
                        self.ground_blocks.add(tile)
                    elif redbox[row][column] == tiles['grass']:
                        tile = Tile(20 * column, 20 * row, 'images/grass.png')
                        self.sprites.add(tile)
                        self.all_blocks.add(tile)
                        self.ground_blocks.add(tile)
                    elif redbox[row][column] == tiles['platform']:
                        tile = Tile(20 * column, 20 * row, 'images/platform.png')
                        self.sprites.add(tile)
                        self.all_blocks.add(tile)
                        self.sky_blocks.add(tile)

        # Create Red Light Object that wins the red level and adds it to its Groups()
        self.light = Light(red_light_endGame_imgs)
        self.sprites.add(self.light)
        self.lights.add(self.light)

        # Set DEBUG_MOBS_NO_SPAWN to 1 to not spawn mobs
        if DEBUG_MOBS_NO_SPAWN:
            print("Playing without mobs")
        else:
            # Create Mobs and add to its Groups()
            for mob in MOBS_SKY_LIST:
                m = Mob(*mob)
                self.sprites.add(m)
                self.mobs.add(m)

    def shutdown(self):
        pygame.quit()
        sys.exit()

    def resetScreenSize(self, size):
        if size == 1:
            self.screen = pygame.display.set_mode(RESOLUTION, pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(RESOLUTION, pygame.RESIZEABLE)

    def drawScreen(self):
        self.screen.fill(SKY_BLUE)
        self.screen.blit(self.background, (self.background_x,0))
        self.sprites.draw(self.screen)
        pygame.display.flip()

    def getCommands(self):
        #Hold Keys for fluid movement
        #print("I'm in getCommands")

        pygame.event.clear(pygame.MOUSEBUTTONUP)
        pygame.event.clear(pygame.MOUSEBUTTONDOWN)
        pygame.event.clear(pygame.MOUSEMOTION)


        for event in pygame.event.get(pygame.KEYDOWN):   # gets keydown events and clears queue
            #print("Detected KEYDOWN")
            if event.key == pygame.K_RIGHT:  #right arrow
                self.spec.forward = True
            if event.key == pygame.K_LEFT:   #left arrow
                self.spec.backward = True
            if event.key == pygame.K_UP:
                if self.spec.falling is False:
                    self.spec.jumpTimeElapsed = pygame.time.get_ticks() #initial store of milliseconds to evaluate length of keypress
                    self.spec.jump = True
            if event.key == pygame.K_ESCAPE:
                self.levelStatus = menu.pauseScreen()

        for event in pygame.event.get(pygame.KEYUP):
            #print("Detected KEYUP")
            if event.key == pygame.K_RIGHT:  #right arrow
                self.spec.forward = False
            if event.key == pygame.K_LEFT:   #left arrow
                self.spec.backward = False
            if event.key == pygame.K_UP: #up arrow
                if self.spec.falling is not True:
                    if pygame.time.get_ticks() - self.spec.jumpTimeElapsed < 200: #if up key was tapped
                        self.spec.jumpThreshold = 5 #raise threshold for smaller jump

    def updateSprites(self):
        self.sprites.update()

        # Test Spec for death below the map or collisions with a mob
        collision_mob = pygame.sprite.spritecollide(self.spec, self.mobs, False)
        if self.spec.rect.top >= HEIGHT or len(collision_mob) != 0:
            print("I should be dying now")
            self.levelStatus = "restart"    #go back to main menu for now
            menu.gameOverScreen()            #leave game.updateSprites

        # Test Spec for collisions with environment
        top_collision = False
        collisions = pygame.sprite.spritecollide(self.spec, self.all_blocks, False)
        if len(collisions) != 0:
            rightmost = leftmost = highest = lowest = collisions[0]
            for collision in collisions:
                if collision.rect.left < leftmost.rect.left:
                    leftmost = collision
                if collision.rect.right > rightmost.rect.right:
                    rightmost = collision
                if lowest is not None and collision.rect.bottom > lowest.rect.bottom:
                    lowest = collision
                if collision.rect.top < highest.rect.top:
                    highest = collision
            #prohibits assignment of rightmost/leftmost blocks to bottom collision logic
            if self.spec.forward and (self.spec.jump or self.spec.falling) and rightmost.rect.bottom <= self.spec.rect.bottom:
                lowest = None
            if self.spec.backward and (self.spec.jump or self.spec.falling) and leftmost.rect.bottom <= self.spec.rect.bottom:
                lowest = None
            if (self.spec.forward or self.spec.backward) and self.spec.jump is False:
                highest = None
            if lowest is not None:
                if self.spec.rect.bottom <= lowest.rect.bottom and self.spec.rect.bottom > lowest.rect.top: #bottom collision
                    self.spec.rect.bottom = lowest.rect.top + 1 #reposition spec slightly below top of object
                    self.spec.falling = False
                    self.spec.fallTimer = 0  # reset falltimer
            if highest is not None:
                if self.spec.rect.top - highest.rect.bottom <= 0 and self.spec.rect.top - highest.rect.bottom >= -10:  #top collision
                    self.spec.rect.top = highest.rect.bottom  #reposition spec to bottom of object
                    self.spec.jump = False
                    self.spec.jumpTimer = 0
                    self.spec.falling = True
                    top_collision = True
            if rightmost is not None:
                if not top_collision and self.spec.rect.right - rightmost.rect.left <= 10 and self.spec.rect.right - rightmost.rect.left >= 0 and rightmost.rect.top < self.spec.rect.bottom - 1: #right collision
                    self.spec.rect.right = rightmost.rect.left #reposition spec to left side of object
                    self.spec.speed[0] = 0 #stop all forward movement
            if leftmost is not None:
                if not top_collision and self.spec.rect.left - leftmost.rect.right <= 0 and self.spec.rect.left - leftmost.rect.right >= -10 and leftmost.rect.top < self.spec.rect.bottom - 1:  #left collision
                    self.spec.rect.left = leftmost.rect.right #reposition spec to right side of object
                    self.spec.speed[1] = 0 #stop all backward movement
        elif len(collisions) == 0:
            if self.spec.jump == False:
                self.spec.falling = True

        # Check if there is a collision with spec and the light object
        collide_light = pygame.sprite.spritecollide(self.spec, self.lights, False)
        if len(collide_light) != 0:
            #print('I am colliding with the light object now')
            if self.whichLevelToPlay == "BLUE":
                self.setLightAcquired("blue")
            elif self.whichLevelToPlay == "GREEN":
                self.setLightAcquired("green")
            elif self.whichLevelToPlay == "RED":
                self.setLightAcquired("red")
            else:
                print("game.updateSprites: ERROR IN SETTING LIGHT ACQUIRED")
            self.endCurrentLevel = 1

        # Check if there is a collision with spec and the mob object
        collide_mob = pygame.sprite.spritecollide(self.spec, self.mobs, False)
        if len(collide_mob) != 0:
            print("I should be dying by hitting a mob")
            self.levelStatus = "restart"    #go back to main menu for now
            menu.gameOverScreen()

        # Check for a collision between the invisible wall block and the sky blocks
        for block in self.sky_blocks:
            # If midpoint of skyblock touches invisible wall center delete skyblock
            if block.rect.midright <= self.invisible_block.rect.center:
                #print("Block should be deleted at this point")
                block.kill()    #Remove block from its groups (Don't draw object anymore)

        # Check for a collision between the invisible_wall_block and spec
        collide_invisible_wall = pygame.sprite.spritecollide(self.spec, self.invisible_wall_block, False)
        if len(collide_invisible_wall) != 0:
            #print("spec is colliding with the invisible_wall_block")
            self.spec.rect.x += 1       # Move Spec forward slightly so he is off the invisible_wall_block
            self.spec.speed[1] = 0      # Set backward speed to 0 so Spec can't move backwards

        # Moving the Blocks based on time
        self.timeSinceInit = pygame.time.get_ticks() #get time since overall game ticks
        if self.timeSinceInit - self.blockTimer > 50: # Check if it has been 1000ms
            # print("time should be above 1000 ms: ", self.timeSinceInit - self.blockTimer)
            # print("self.timeSinceInit: ", self.timeSinceInit)
            # print("self.blockTimer: ", self.blockTimer)
            self.blockTimer = self.timeSinceInit
            self.timeSinceInit = 0
            if self.block_movement_counter < 50:
                self.block_movement_counter += 1
                for block in self.sky_blocks:
                    block.rect.x += 1        # Move blocks right
            elif self.block_movement_counter < 100:
                self.block_movement_counter += 1
                for block in self.sky_blocks:
                    block.rect.x -= 1        # Move blocks left
            else:
                self.block_movement_counter = 0

        # Scrolling happens in the updateSprites part of game
        if (self.spec.rect.x > WIDTH - 300) \
            and self.spec.speed[0] is not 0 \
            and self.light.rect.x > WIDTH-40:
            #Move Everthing based on speed of Spec
            self.spec.rect.x -= self.spec.speed[0]
            # Move Sky Blocks
            for block in self.sky_blocks:
                block.rect.x -= self.spec.speed[0]
            # Move Ground blocks now
            for gb in self.ground_blocks:
                gb.rect.x -= self.spec.speed[0]
            # Scroll Mobs
            for m in self.mobs:
                m.rect.x -= self.spec.speed[0]
            # Move Game ending light Object
            self.light.rect.x -= self.spec.speed[0]
            # Scroll Background image based on which level we're playing
            if self.whichLevelToPlay == "BLUE":
                self.background_x -= (len(bluebox[0]) * 20 / self.background.get_width()) * .60  # map pixels / background image pixels
            elif self.whichLevelToPlay == "GREEN":
                self.background_x -= (len(greenbox[0]) * 20 / self.background.get_width()) * .60  # map pixels / background image pixels
            elif self.whichLevelToPlay == "RED":
                self.background_x -= (len(redbox[0]) * 20 / self.background.get_width()) * .60  # map pixels / background image pixels

    def checkStatus(self):
        if pygame.event.get(pygame.QUIT): #check if QUIT event. Return status false to terminate game
            self.status = False

    def setLightAcquired(self, light):
        print("setLightAcquired: Trying to set acquired light: ", light)
        if light == "blue":
            self.blue_light_acquired = 1
        elif light == "red":
            self.red_light_acquired = 1
        elif light == "green":
            self.green_light_acquired = 1
        else:
            print("game.setLightAcquired: ERROR IN SETTING LIGHT ACQUIRED")

    def checkLightAcquired(self, light):
        if light == "blue":
            return self.blue_light_acquired
        elif light == "red":
            return self.red_light_acquired
        else:
            return self.green_light_acquired

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, color):
        pygame.sprite.Sprite.__init__(self) #sprite constructor
        self.image = pygame.Surface([w, h]) #width x height
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

#Tiled blocks build environment
class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_path).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

game = Game()

#Load menu sounds
click = pygame.mixer.Sound('sounds/click.ogg')
click.set_volume(0.5)
lose_music = pygame.mixer.Sound('sounds/lose_music.ogg')
win_music = pygame.mixer.Sound('sounds/win_music.ogg')

# Load Menu images
bl_light_img = pygame.image.load('images/blueLight.png').convert()
rd_light_img = pygame.image.load('images/redLight.png').convert()
gr_light_img = pygame.image.load('images/greenLight.png').convert()
vol_slider = pygame.image.load('images/vol_slider.png').convert()
vol_bar = pygame.image.load('images/vol_bar.png').convert()
vol_arr_right = pygame.image.load('images/vol_arrowRight.png').convert()
vol_arr_left = pygame.image.load('images/vol_arrowLeft.png').convert()
play_btn_inactive = pygame.image.load('images/pl_btn_inactive.png').convert()
play_btn_active = pygame.image.load('images/pl_btn_active.png').convert()
fullscreen_inactive = pygame.image.load('images/fullscreen_inactive.png').convert()
fullscreen_active = pygame.image.load('images/fullscreen_active.png').convert()
skylevel_inactive = pygame.image.load('images/skylevel_inactive.png').convert()
skylevel_active = pygame.image.load('images/skylevel_active.png').convert()
frame_img = pygame.image.load('images/frame.png').convert()


menu_imgs = []
menu_imgs.extend((bl_light_img, rd_light_img, gr_light_img, vol_slider, vol_bar, vol_arr_right, vol_arr_left, play_btn_inactive, play_btn_active, fullscreen_inactive, fullscreen_active, skylevel_inactive, skylevel_active, frame_img))

menu_sounds = [click, lose_music, win_music]

bl_light_1 = pygame.image.load('images/bl_light_endGame1.png').convert()
bl_light_2 = pygame.image.load('images/bl_light_endGame2.png').convert()
green_light_1 = pygame.image.load('images/green_light_endGame1.png').convert()
green_light_2 = pygame.image.load('images/green_light_endGame2.png').convert()
red_light_1 = pygame.image.load('images/red_light_endGame1.png').convert()
red_light_2 = pygame.image.load('images/red_light_endGame2.png').convert()

bl_light_endGame_imgs = []
bl_light_endGame_imgs.extend((bl_light_1, bl_light_2))
green_light_endGame_imgs = []
green_light_endGame_imgs.extend((green_light_1, green_light_2))
red_light_endGame_imgs = []
red_light_endGame_imgs.extend((red_light_1, red_light_2))
# Create menu object
menu = Menu(game.screen, time, menu_imgs, menu_sounds)
openMenu = True
count = 0
music_vol = 0.5

while(openMenu):
    # print("Starting outer loop...")
    if count == 0:
        menu.startScreen()
        music_vol, fullScreen, levelSelect = menu.mainMenu(game)
    else:
        pygame.mixer.music.load(MENU_BG_MUSIC)
        pygame.mixer.music.set_volume(music_vol)
        pygame.mixer.music.play(-1) # -1 = loop the song
        music_vol, fullScreen, levelSelect = menu.mainMenu(game)

    if fullScreen:
        game.screen = pygame.display.set_mode(RESOLUTION, pygame.FULLSCREEN)
    else:
        game.screen = pygame.display.set_mode(RESOLUTION, pygame.RESIZABLE)

    game.startup(levelSelect)

    active = True
    game.status = True
    # Main Game Loop
    while(active):
        # print("Starting inner loop")
        # Check if all lights have been acquired ; End game if true
        if game.checkLightAcquired("blue") \
        and game.checkLightAcquired("red") \
        and game.checkLightAcquired("green"):
            menu.gameCompletedScreen()
            game.resetGame()
            break
         #Check for end level status
        if game.endCurrentLevel == 1:
            menu.completeLevel()
            game.endCurrentLevel = 0
            break

        #print("Active: ", active)
        #print("openGame: ", openGame)
        #increment time
        time.tick(FRAMES)
        #print ("Frames: ", time.tick(FRAMES)) #prints how many frames of seconds has been passed

        game.checkStatus()
        active = game.status #check if game is still active based on game status
        if not active:
            openGame = False

        # Obtain keyboard inputs
        #print("About to call getCommands")
        game.getCommands()

        #print("Finished calling getCommands")
        status = game.levelStatus
        #print(status)
        if status == "restart":
            game.levelStatus = ""
            break

        # Update sprites and background
        game.updateSprites()


        # Print to screen
        game.drawScreen()

    count += 1
    #print("openGame", openGame)


game.shutdown()
