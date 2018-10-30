# Spectrum.py
import pygame, sys, os
import random
from settings import *
from menu import *
from spec import *
from mob import *
from light import *
from map_sandbox import *

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
    def startup(self):
        #Create Start Up Game timers and counters
        self.background_x = 0  # rate of background scrolling (calculated at runtime)
        self.block_movement_counter = 0
        self.blockTimer = pygame.time.get_ticks()

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

        # Create Mobs and add to its Groups()
        for mob in MOBS_SKY_LIST:
            m = Mob(*mob)
            self.sprites.add(m)
            self.mobs.add(m)

        #Initialize blocks from map and add to sprite groups
        for row in range(len(sandbox)):
            for column in range(len(sandbox[0])):
                if sandbox[row][column] is not tiles['sky']:
                    if sandbox[row][column] == tiles['earth']:
                        tile = Tile(20 * column, 20 * row, 'images/earth.png')
                        self.sprites.add(tile)
                        self.all_blocks.add(tile)
                        self.ground_blocks.add(tile)
                    elif sandbox[row][column] == tiles['grass']:
                        tile = Tile(20 * column, 20 * row, 'images/grass.png')
                        self.sprites.add(tile)
                        self.all_blocks.add(tile)
                        self.ground_blocks.add(tile)
                    elif sandbox[row][column] == tiles['platform']:
                        tile = Tile(20 * column, 20 * row, 'images/platform.png')
                        self.sprites.add(tile)
                        self.all_blocks.add(tile)
                        self.sky_blocks.add(tile)

        # Initalize left "Invisible" Wall Block
        self.invisible_block = Block(-50, 0, 50, 600, WHITE)
        self.sprites.add(self.invisible_block)
        self.invisible_wall_block.add(self.invisible_block)

        # Create Light Object that wins the game and adds it to its Groups()
        self.light = Light(bl_light_endGame_imgs)
        self.sprites.add(self.light)
        self.lights.add(self.light)

        if DEBUG:
            print('Pygame Version: ' + pygame.version.ver)
            print('Platform: ' + sys.platform)

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
                if self.spec.speed[1] == 0:  #disallows immediately reversing direction
                    self.spec.forward = True
                else:  #permits player to hold down opposite direction key
                    pygame.event.post(event) #places keydown event back to queue
            if event.key == pygame.K_LEFT:   #left arrow
                if self.spec.speed[0] == 0: #disallows immediately reversing direction
                    self.spec.backward = True
                else: #permits player to hold down opposite direction key
                    pygame.event.post(event) #places keydown event back into queue
            if event.key == pygame.K_UP:
                if self.spec.falling is not True:
                    self.spec.jumpTimeElapsed = pygame.time.get_ticks() #initial store of milliseconds to evaluate length of keypress
                    self.spec.jump = True
            if event.key == pygame.K_ESCAPE:
                self.levelStatus = menu.pauseScreen()

        for event in pygame.event.get(pygame.KEYUP):
            #print("Detected KEYUP")
            if event.key == pygame.K_RIGHT:  #right arrow
                self.spec.forward = False
                self.spec.slowForward = True
            if event.key == pygame.K_LEFT:   #left arrow
                self.spec.backward = False
                self.spec.slowBackward = True
            if event.key == pygame.K_UP: #up arrow
                if self.spec.falling is not True:
                    if pygame.time.get_ticks() - self.spec.jumpTimeElapsed < 200: #if up key was tapped
                        self.spec.jumpThreshold = 30 #raise threshold for smaller jump

    def updateSprites(self):
        self.sprites.update()

        # Test Spec for death below the map or collisions with a mob
        collision_mob = pygame.sprite.spritecollide(self.spec, self.mobs, False)
        if self.spec.rect.top >= HEIGHT or len(collision_mob) != 0:
            print("I should be dying now")
            self.levelStatus = "restart"    #go back to main menu for now
            menu.gameOverScreen()            #leave game.updateSprites

        # Test Spec for collisions with environment
        # collisions = pygame.sprite.spritecollide(self.spec, self.blocks, False)
        collisions = pygame.sprite.spritecollide(self.spec, self.all_blocks, False)
        if len(collisions) != 0:
            if self.spec.rect.bottom <= collisions[0].rect.centery:
                self.spec.rect.bottom = collisions[0].rect.top + 1 #reposition spec to above object
                self.spec.falling = False
                self.spec.fallTimer = 0  # reset falltimer
            elif self.spec.rect.top - collisions[0].rect.bottom <= 0 and self.spec.rect.top - collisions[0].rect.bottom >= -10:  #top collision
                self.spec.rect.top = collisions[0].rect.bottom  #reposition spec to bottom of object
                self.spec.jump = False
                self.spec.jumpTimer = 40
                self.spec.falling = True
            elif self.spec.rect.right - collisions[0].rect.left <= 10 and self.spec.rect.right - collisions[0].rect.left >= -0: #right collision
                self.spec.rect.right = collisions[0].rect.left #reposition spec to left side of object
                self.spec.speed[0] = 0 #stop all forward movement
            elif self.spec.rect.left - collisions[0].rect.right <= 0 and self.spec.rect.left - collisions[0].rect.right >= -10: #left collision
                self.spec.rect.left = collisions[0].rect.right #reposition spec to right side of object
                self.spec.speed[1] = 0 #stop all backward movement
            if DEBUG:
                print(collisions)

        # Check if there is a collision with spec and the light object
        collide_light = pygame.sprite.spritecollide(self.spec, self.lights, False)
        if len(collide_light) != 0:
            #print('I am colliding with the light object now')
            self.setLightAcquired("blue")
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
            # Scroll Background image
            self.background_x -= (len(sandbox[0]) * 20 / self.background.get_width()) * .90  # map pixels / background image pixels

    def checkStatus(self):
        if pygame.event.get(pygame.QUIT): #check if QUIT event. Return status false to terminate game
            self.status = False

    def setLightAcquired(self, light):
        if light == "blue":
            self.blue_light_acquired = 1
        elif light == "red":
            self.red_light_acquired = 1
        else:
            self.green_light_acquired = 1

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
frame_img = pygame.image.load('images/frame.png').convert()

menu_imgs = []
menu_imgs.extend((bl_light_img, rd_light_img, gr_light_img, vol_slider, vol_bar, vol_arr_right, vol_arr_left, play_btn_inactive, play_btn_active, frame_img))


bl_light_1 = pygame.image.load('images/bl_light_endGame1.png').convert()
bl_light_2 = pygame.image.load('images/bl_light_endGame2.png').convert()

bl_light_endGame_imgs = []
bl_light_endGame_imgs.extend((bl_light_1, bl_light_2))
# Create menu object
menu = Menu(game.screen, time, menu_imgs)
openMenu = True
count = 0
music_vol = 0.5

while(openMenu):
    # print("Starting outer loop...")
    if count == 0:
        menu.startScreen()
        music_vol, fullScreen = menu.mainMenu()
    else:
        pygame.mixer.music.load(MENU_BG_MUSIC)
        pygame.mixer.music.set_volume(music_vol)
        pygame.mixer.music.play(-1) # -1 = loop the song
        music_vol, fullScreen  = menu.mainMenu()
        # if fullScreen:
        #     game.screen = pygame.display.set_mode(RESOLUTION, pygame.FULLSCREEN)
        # else:
        #     game.screen = pygame.display.set_mode(RESOLUTION, pygame.RESIZABLE)

    game.startup()

    active = True
    game.status = True
    # Main Game Loop
    while(active):
        # print("Starting inner loop")
        #Check for acquired lights
        blue_light = game.checkLightAcquired("blue")
        red_light = game.checkLightAcquired("red")
        green_light = game.checkLightAcquired("green")
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
