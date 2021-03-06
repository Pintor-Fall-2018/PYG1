'''
 Name: Spectrum.py  (PGY1)
 Team Name: Pictor
 Team Members: Jarret Edelen, Shane Klumpp, Tiffany Warner
 Course: CS 467 - Fall 2018 - Capstone Project
 Description: Spectrum is a platformer game built in pygame. The user
        plays as a character called Spec who's goal is to play through
        3 levels(Sky, Forest, and Desert) and acquire the
        lights(Blue, Green, and Red) at the end of each. Spec has
        to navigate around obstacles and avoid mobs to reach the light
        objects at the end. Spec starts with 7 lives. If all lives
        are lost, the game resets. Upon acquiring all 3 lights, the
        game is won. Safe Mode can be entered by hitting "s" which
        allows Spec to navigate each level while being invincible against
        mobs.

'''
import pygame, sys, os
import random
from settings import *
from menu import *
from spec import *
from mob import *
from light import *
from powerup import *
from map_Blue import *
from map_Green import *
from map_Red import *
from tile import *
from block import *


# Note: Initialize sound before game to prevent sound lag
#       Especially import for sound effects
# 44100 Hz = Frequency,    -16 = size
# 1 = channels, 2048 = buffersize -- this is what prevents sound lag
pygame.mixer.pre_init(44100, -16, 2, 4096)


pygame.init()   #initialize imported pygame modules
pygame.display.set_caption(TITLE)
pygame.mouse.set_visible(1)   # Mouse visible == 1
time = pygame.time.Clock()

#Font for handling safe/invincible mode
pygame.font.init() #initialize font module
system_font = pygame.font.SysFont(pygame.font.get_default_font(), 28, False, False)
safe_mode = system_font.render('Safety Mode Active', False, (50,120,75))

class Game:
    '''
    Name: Game Class
    Description: Main handler for gameplay. Handles movement
                 mechanics, game flow, and all main game features.
    Functions:
        __init__(self, mob_sounds)- Constructor
        resetGame(self) - resets game variables
        startup(self, levelSelect) - sets game variables, sprites, levels
        playBlue(self) - Handler for blue/sky level
        playGreen(self) - Handler for green/forest level
        playRed(self) - Handler for red/desert level
        blackHoleGravity(self) - Implements black hole gravity effects on Spec
        displayLifeBars(self) - Handler for the 7 life hearts for Spec
        shutdown(self) - exits the game
        resetScreenSize(self, size) - Fullscreen or windowed mode
        loseAnimation(self) - Animation when Spec loses one life
        endAnimation(self) - Animation when Spec obtains all 3 lights and wins game
        drawScreen(self) - Handler for drawing changes to the screen
        getCommands(self) - Handler for getting user actions
        updateSprites(self) - Handler for updating all sprites-movements/actions
        tileCollisions(self) - Handler for Spec's interactions with environment
        loseLife(self) - Handler for showing screens when Spec loses 1 life or all lives
        platformMotion(self) - Handler for moving Spec with moving platforms
        checkStatus(self) - Checks for pygame's quit event to quit the game
        setLightAcquired(self, light) - Sets light variables when Spec has obtained a light
        checkLightAcquired(self, light) - Checks light variables to see which lights have been acquired
    '''
    def __init__(self, mob_sounds):
        '''
        __init__ - Constructor function - intializes game variables
        '''
        self.status = True
        #sets up screen resolution
        self.screen = pygame.display.set_mode(RESOLUTION, pygame.RESIZABLE)   #display settings
        self.blue_light_acquired = 0
        self.red_light_acquired = 0
        self.green_light_acquired = 0
        self.endCurrentLevel = 0
        self.levelStatus = ""
        self.lives = 7
        self.gameLost = False
        self.randomPowerUpLevel = random.randint(1, 3)
        self.bluePowerUp = 0
        self.greenPowerUp = 0
        self.redPowerUp = 0
        self.powerUpOnMap = False
        self.powerUpTimer = 0
        self.red = False
        self.mob_sounds = mob_sounds
        self.block_timer = 0
        self.safe_mode = False

        self.lights_collected = pygame.mixer.Sound('sounds/lights_collected.wav')
        self.lights_collected.set_volume(0.15)

        #https://opengameart.org/content/fast-fight-battle-music-looped
        #Author: XCVG
        self.powerup_music = pygame.mixer.Sound('sounds/fight_looped.wav')
        self.powerup_music.set_volume(0.05)

    def resetGame(self):
        '''
        resetGame(self) - resets all game status variables to initial conditions
        '''
        # resets game attributes
        self.blue_light_acquired = 0
        self.red_light_acquired = 0
        self.green_light_acquired = 0
        self.endCurrentLevel = 0
        self.levelStatus = ""
        self.lives = 7
        self.gameLost = False
        self.randomPowerUpLevel = random.randint(1, 3)
        self.powerUpActive = False
        self.bluePowerUp = 0
        self.greenPowerUp = 0
        self.redPowerUp = 0
        self.powerUpOnMap = False
        self.powerUpTimer = 0
        self.red = False

    # Startup function. Responsible for creating the map and all objects
    def startup(self, levelSelect):
        '''
        startup(self, levelSelect) -  Responsible for creating the map
                    and all game objects. Also sets up level selection
                    and an invisible wall to prevent Spec from running
                    off-screen on the left.
        '''
        #Create Start Up Game timers, counters and variables
        self.background_x = 0  # rate of background scrolling (calculated at runtime)
        self.block_movement_counter = 0
        self.whichLevelToPlay = levelSelect # assign map to play based on levelSelect String
        self.powerUpActive = False
        self.powerUpOnMap = False

        #assign power up level based on randomPowerUpLevel. 1 = spawn power up on that map
        if self.randomPowerUpLevel == 1:
            self.bluePowerUp = 1
        elif self.randomPowerUpLevel == 2:
            self.greenPowerUp = 1
        elif self.randomPowerUpLevel == 3:
            self.redPowerUp = 1
        else:
            print("game.startUp: ERROR setting level power up")

        # Create Groups()
        self.sprites = pygame.sprite.Group()
        self.sky_blocks = pygame.sprite.Group()             # Moving blocks
        self.ground_blocks = pygame.sprite.Group()          # Ground blocks don't move!
        self.invisible_wall_block = pygame.sprite.Group()   # Invisible wall block (left screen limiter)
        self.bg_blocks = pygame.sprite.Group()              # Background blocks (no collisions)
        self.all_blocks = pygame.sprite.Group()
        self.lights = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.uv_mobs = pygame.sprite.Group()
        self.bh_mobs = pygame.sprite.Group()
        self.powerUpGroup = pygame.sprite.Group()           # Power Up Group

        # Life bar images
        self.lives_imgs = []
        self.lives_imgs.append(pygame.image.load('images/life_heart.png').convert())
        self.lives_imgs.append(pygame.image.load('images/life_heart_gone.png').convert())

        # Create Game Objects and add to their Groups()
        self.spec = Spec()
        self.sprites.add(self.spec)

        # Create Level based on user selection from menu.MainMenu()
        # Levels create level specific map, mobs, EOG light object
        if self.whichLevelToPlay == "BLUE":
            #print("game.startUp: starting game.playBlue")
            game.playBlue()
        elif self.whichLevelToPlay == "GREEN":
            #print("game.startUp: starting game.playGreen")
            game.playGreen()
        elif self.whichLevelToPlay == "RED":
            #print("game.startUp: starting game.playRed")
            game.playRed()
        else:
            print("You shouldn't ever see this. Level selection ERROR")
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
        '''
        playBlue(self) -  Responsible for handling the map and all sprites
                    within the Sky/blue level
        '''
        self.red = False
        #print ("game.playBlue: Creating the Sky level")
        self.background = pygame.image.load('images/blue_background.png').convert() #load background image
        # Create Blue Level from tile map
        for row in range(len(bluebox)):
            for column in range(len(bluebox[0])):
                if bluebox[row][column] is not tiles_blue['sky']:
                    if bluebox[row][column] == tiles_blue['earth']:
                        tile = Tile(20 * column, 20 * row, 'images/earth.png')
                        self.sprites.add(tile)
                        self.all_blocks.add(tile)
                        self.ground_blocks.add(tile)
                    elif bluebox[row][column] == tiles_blue['cloud']:
                        tile = Tile(20 * column, 20 * row, 'images/cloud.png')
                        self.sprites.add(tile)
                        self.all_blocks.add(tile)
                        self.ground_blocks.add(tile)
                    elif bluebox[row][column] == tiles_blue['platform']:
                        tile = Tile(20 * column, 20 * row, 'images/platform.png')
                        self.sprites.add(tile)
                        self.all_blocks.add(tile)
                        self.sky_blocks.add(tile)
                    elif bluebox[row][column] == tiles_blue['platform1']:
                        tile = Tile(20 * column, 20 * row, 'images/blue_platform1.png')
                        self.sprites.add(tile)
                        self.all_blocks.add(tile)
                        self.ground_blocks.add(tile)

        # Create Blue Light Object that wins the blue level and adds it to its Groups()
        self.light = Light(bl_light_endGame_imgs)
        self.sprites.add(self.light)
        self.lights.add(self.light)

        # Set DEBUG_MOBS_NO_SPAWN to 1 to not spawn mobs
        if DEBUG_MOBS_NO_SPAWN:
            print("Playing without mobs")
        else:
            # Create Mobs and add to its Groups()
            for ultraviolet in ULTRAVIOLET_SKY_LIST:
                uv = Ultraviolet(*ultraviolet, self.mob_sounds)
                self.sprites.add(uv)
                self.mobs.add(uv)
                self.uv_mobs.add(uv)

            for gammaRay in GAMMA_SKY_LIST:
                gr = Gamma(*gammaRay, self.mob_sounds)
                self.sprites.add(gr)
                self.mobs.add(gr)

            for infrared in INFRARED_SKY_LIST:
                ir = Infrared(*infrared, self.mob_sounds)
                self.sprites.add(ir)
                self.mobs.add(ir)

            for blackhole in BLACK_HOLE_SKY_LIST:
                bh = BlackHole(*blackhole, self.mob_sounds)
                self.sprites.add(bh)
                self.mobs.add(bh)

        # Create Powerup if active on blue level
        if self.bluePowerUp == 1:
            self.powerUp = PowerUp(1120, 260, powerUp_image)
            self.sprites.add(self.powerUp)
            self.powerUpGroup.add(self.powerUp)
            self.powerUpOnMap = True

    def playGreen(self):
        '''
        playGreen(self): -  Responsible for handling the map and all sprites
                    within the Forest/green level
        '''
        self.red = False
        #print ("game.playGreen: Creating the Forest level")
        self.background = pygame.image.load('images/green_background.png').convert() #load background image
        # Create Green Level from tile map
        for row in range(len(greenbox)):
            for column in range(len(greenbox[0])):
                if greenbox[row][column] is not tiles_green['sky']:
                    if greenbox[row][column] == tiles_green['earth']:
                        tile = Tile(20 * column, 20 * row, 'images/green_earth.png')
                        self.sprites.add(tile)
                        self.all_blocks.add(tile)
                        self.ground_blocks.add(tile)
                    elif greenbox[row][column] == tiles_green['grass']:
                        tile = Tile(20 * column, 20 * row, 'images/green_grass.png')
                        self.sprites.add(tile)
                        self.all_blocks.add(tile)
                        self.ground_blocks.add(tile)
                    elif greenbox[row][column] == tiles_green['platform']:
                        tile = Tile(20 * column, 20 * row, 'images/green_platform.png')
                        self.sprites.add(tile)
                        self.all_blocks.add(tile)
                        self.ground_blocks.add(tile)
                        #self.sky_blocks.add(tile)
                    elif greenbox[row][column] == tiles_green['earth1']:
                        tile = Tile(20 * column, 20 * row, 'images/green_earth01.png')
                        self.sprites.add(tile)
                        self.all_blocks.add(tile)
                        self.ground_blocks.add(tile)
                    elif greenbox[row][column] == tiles_green['earth2']:
                        tile = Tile(20 * column, 20 * row, 'images/green_earth02.png')
                        self.sprites.add(tile)
                        self.all_blocks.add(tile)
                        self.ground_blocks.add(tile)
                    elif greenbox[row][column] == tiles_green['water_surface']:
                        tile = Tile(20 * column, 20 * row, 'images/green_water.png')
                        self.sprites.add(tile)
                        self.ground_blocks.add(tile)
                    elif greenbox[row][column] == tiles_green['water']:
                        tile = Tile(20 * column, 20 * row, 'images/green_water1.png')
                        self.sprites.add(tile)
                        self.ground_blocks.add(tile)
                    elif greenbox[row][column] == tiles_green['grass_edge_right']:
                        tile = Tile(20 * column, 20 * row, 'images/green_grass01.png')
                        self.sprites.add(tile)
                        self.all_blocks.add(tile)
                        self.ground_blocks.add(tile)
                    elif greenbox[row][column] == tiles_green['grass_edge_left']:
                        tile = Tile(20 * column, 20 * row, 'images/green_grass02.png')
                        self.sprites.add(tile)
                        self.all_blocks.add(tile)
                        self.ground_blocks.add(tile)
                    elif greenbox[row][column] == tiles_green['grass_edge_overlap_right']:
                        tile = Tile(20 * column, 20 * row, 'images/green_grass03.png')
                        self.sprites.add(tile)
                        self.all_blocks.add(tile)
                        self.ground_blocks.add(tile)
                    elif greenbox[row][column] == tiles_green['platform2']:
                        tile = Tile(20 * column, 20 * row, 'images/green_platform02.png')
                        self.bg_blocks.add(tile)


        # Create Green Light Object that wins the green level and adds it to its Groups()
        self.light = Light(green_light_endGame_imgs)
        self.sprites.add(self.light)
        self.lights.add(self.light)

        # Set DEBUG_MOBS_NO_SPAWN to 1 to not spawn mobs
        if DEBUG_MOBS_NO_SPAWN:
            print("Playing without mobs")
        else:
            # Create Mobs and add to its Groups()
            for mob in ULTRAVIOLET_FOREST_LIST:
                m = Ultraviolet(*mob, self.mob_sounds)
                self.sprites.add(m)
                self.mobs.add(m)
                self.uv_mobs.add(m)
            for mob in GAMMA_FOREST_LIST:
                g = Gamma(*mob, self.mob_sounds)
                self.sprites.add(g)
                self.mobs.add(g)
            for mob in INFRARED_FOREST_LIST:
                i = Infrared(*mob, self.mob_sounds)
                self.sprites.add(i)
                self.mobs.add(i)

        # Create Powerup if active on green level
        if self.greenPowerUp == 1:
            self.powerUp = PowerUp(980, 300, powerUp_image)
            self.sprites.add(self.powerUp)
            self.powerUpGroup.add(self.powerUp)
            self.powerUpOnMap = True

    def playRed(self):
        '''
        playRed(self): -  Responsible for handling the map and all sprites
                    within the Desert/red level
        '''
        self.red = True
        #print ("game.playRed: Creating the Desert level")
        self.background = pygame.image.load('images/red_background.png').convert() #load background image
        # Create Green Level from tile map
        for row in range(len(redbox)):
            for column in range(len(redbox[0])):
                if redbox[row][column] is not tiles_red['sky']:
                    if redbox[row][column] == tiles_red['sand_center']:
                        tile = Tile(20 * column, 20 * row, 'images/sand_center.png')
                        self.sprites.add(tile)
                        self.all_blocks.add(tile)
                        self.ground_blocks.add(tile)
                    elif redbox[row][column] == tiles_red['sand_top']:
                        tile = Tile(20 * column, 20 * row, 'images/sand_top.png')
                        self.sprites.add(tile)
                        self.all_blocks.add(tile)
                        self.ground_blocks.add(tile)
                    elif redbox[row][column] == tiles_red['platform']:
                        tile = Tile(20 * column, 20 * row, 'images/red_platform.png')
                        self.sprites.add(tile)
                        self.all_blocks.add(tile)
                        self.sky_blocks.add(tile)
                    elif redbox[row][column] == tiles_red['red_metal']:
                        tile = Tile(20 * column, 20 * row, 'images/red_platform2.png')
                        self.sprites.add(tile)
                        self.all_blocks.add(tile)
                        self.ground_blocks.add(tile)
                    elif redbox[row][column] == tiles_red['red_metal_move']:
                        tile = Tile(20 * column, 20 * row, 'images/red_platform2.png')
                        self.sprites.add(tile)
                        self.all_blocks.add(tile)
                        self.sky_blocks.add(tile)


        # Create Red Light Object that wins the red level and adds it to its Groups()
        self.light = Light(red_light_endGame_imgs)
        self.sprites.add(self.light)
        self.lights.add(self.light)

        #Set DEBUG_MOBS_NO_SPAWN to 1 to not spawn mobs
        if DEBUG_MOBS_NO_SPAWN:
            print("Playing without mobs")
        else:
            # Create Mobs and add to its Groups()
            for mob in ULTRAVIOLET_DESERT_LIST:
                m = Ultraviolet(*mob, self.mob_sounds)
                self.sprites.add(m)
                self.mobs.add(m)
                self.uv_mobs.add(m)
            for mob in GAMMA_DESERT_LIST:
                g = Gamma(*mob, self.mob_sounds)
                self.sprites.add(g)
                self.mobs.add(g)
            for mob in BLACK_HOLE_DESERT_LIST:
                bh = BlackHole(*mob, self.mob_sounds)
                self.sprites.add(bh)
                self.mobs.add(bh)
                self.bh_mobs.add(bh)

        # Create Powerup if active on red level
        if self.redPowerUp == 1:
            self.powerUp = PowerUp(440, 300, powerUp_image)
            self.sprites.add(self.powerUp)
            self.powerUpGroup.add(self.powerUp)
            self.powerUpOnMap = True

    def blackHoleGravity(self):
        BLACKHOLE_RANGE = 80
        if self.red:
            for mob in self.bh_mobs:
                #Distance to the left of the black hole
                if self.spec.rect.x - mob.rect.x <= -10 and self.spec.rect.x - mob.rect.x > - BLACKHOLE_RANGE \
                and mob.rect.y - self.spec.rect.y < 30:
                    self.spec.rect.x = self.spec.rect.x + 1
                #Distance to the right of the black hole.
                elif self.spec.rect.x - mob.rect.x >= -10 and self.spec.rect.x - mob.rect.x < BLACKHOLE_RANGE \
                and mob.rect.y - self.spec.rect.y < 30:
                    self.spec.rect.x = self.spec.rect.x - 1

    def displayLifeBars(self):
        '''
        displayLifeBars(self) - Displays appropriate number of red and black
                life hearts at the top of the game screen depending on
                how many lives Spec has.
        '''
        self.lives_imgs[0].set_colorkey(BLACK)
        self.lives_imgs[1].set_colorkey(BLACK)
        coords = [-10, -10, 20, -10, 50, -10, 80, -10, 110, -10, 140, -10, 170, -10]
        img = 0
        if self.lives > 6:
            for i in range(0,14,2):
                self.screen.blit(self.lives_imgs[img], (coords[i], coords[i+1]))
        elif self.lives > 5:
            for i in range(0,14,2):
                if(i == 12):
                    img = 1
                self.screen.blit(self.lives_imgs[img], (coords[i], coords[i+1]))
        elif self.lives > 4:
            for i in range(0,14,2):
                if(i == 10 or i == 12):
                    img = 1
                self.screen.blit(self.lives_imgs[img], (coords[i], coords[i+1]))
        elif self.lives > 3:
            for i in range(0,14,2):
                if(i == 8 or i == 10 or i == 12):
                    img = 1
                self.screen.blit(self.lives_imgs[img], (coords[i], coords[i+1]))
        elif self.lives > 2:
            for i in range(0,14,2):
                if(i == 6 or i == 8 or i == 10 or i == 12):
                    img = 1
                self.screen.blit(self.lives_imgs[img], (coords[i], coords[i+1]))
        elif self.lives > 1:
            for i in range(0,14,2):
                if(i == 4 or i == 6 or i == 8 or i == 10 or i == 12):
                    img = 1
                self.screen.blit(self.lives_imgs[img], (coords[i], coords[i+1]))
        elif self.lives > 0:
            for i in range(0,14,2):
                if(i == 0):
                    img = 0
                else:
                    img = 1
                self.screen.blit(self.lives_imgs[img], (coords[i], coords[i+1]))
        else:
            img = 1
            for i in range(0,14,2):
                self.screen.blit(self.lives_imgs[img], (coords[i], coords[i+1]))
        img = 0

    def shutdown(self):
        '''
        shutdown(self) - Quits and exits the game
        '''
        pygame.quit()
        sys.exit()

    def resetScreenSize(self, size):
        '''
        resetScreenSize(self, size) - resets screen to full screen or windowed
                mode depending on what user has selected.
        '''
        if size == 1:
            self.screen = pygame.display.set_mode(RESOLUTION, pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(RESOLUTION, pygame.RESIZABLE)

    def loseAnimation(self):
        '''
        loseAnimation(self) - Animation occurs when Spec collides with
                mob and loses a life
        '''
        #Spec has lost all 7 of his lives
        if self.lives <= 1:
            death_yell_alternate.play()
        else:
            death_yell.play()
        self.spec.kill()
        self.drawScreen()
        frozen_screen = self.screen.copy()
        collision_image = pygame.image.load('images/spec_collision.png').convert()
        collision_image.set_colorkey([34,177,76])
        self.spec.image = collision_image
        self.screen.blit(self.spec.image, (self.spec.rect.x, self.spec.rect.y))
        pygame.display.flip()
        pygame.time.wait(500)
        for i in range(100):
            if i < 20:
                self.spec.rect.y -= self.spec.vertical[i] / 1.5
            elif i < 40:
                self.spec.rect.y += self.spec.vertical[19-i] / 1.5
            else:
                self.spec.rect.y += self.spec.vertical[0] / 1.5
            self.screen.blit(frozen_screen, (0,0))
            self.screen.blit(self.spec.image, (self.spec.rect.x, self.spec.rect.y))
            pygame.display.flip()
            pygame.time.wait(10)

    def endAnimation(self):
        '''
        endAnimation(self) - Game winning animation.
                Light object radiates color and screen fades to white
        '''
        self.lights_collected.play()
        fade_out = pygame.Surface((600,400))
        fade_out.fill(WHITE)
        fade_out.set_alpha(20)
        for i in range(300):
            if i < 100:
                pygame.draw.line(self.screen, (randint(0,255),randint(0,255),randint(0,255)), (self.light.rect.centerx, self.light.rect.centery), (randint(400,600),randint(0,400)), 1)
                self.screen.blit(self.light.image, (self.light.rect.x, self.light.rect.y))
                self.screen.blit(fade_out, (0,0))
                pygame.display.flip()
                pygame.time.wait(2)
            elif i < 200:
                pygame.draw.line(self.screen, (randint(0,255),randint(0,255),randint(0,255)), (self.light.rect.centerx, self.light.rect.centery), (randint(300,600),randint(0,400)),2)
                self.screen.blit(self.light.image, (self.light.rect.x, self.light.rect.y))
                self.screen.blit(fade_out, (0,0))
                pygame.display.flip()
                pygame.time.wait(2)
            else:
                pygame.draw.line(self.screen, (randint(0,255),randint(0,255),randint(0,255)), (self.light.rect.centerx, self.light.rect.centery), (randint(0,600),randint(0,400)), 3)
                self.screen.blit(self.light.image, (self.light.rect.x, self.light.rect.y))
                self.screen.blit(fade_out, (0,0))
                pygame.display.flip()
                pygame.time.wait(2)

    def drawScreen(self):
        '''
        drawScreen(self) - Draws updated positions of objects and images
                to screen.
        '''
        self.screen.blit(self.background, (self.background_x,0))
        self.bg_blocks.draw(self.screen)
        self.sprites.draw(self.screen)
        self.displayLifeBars()
        if self.safe_mode:
            self.screen.blit(safe_mode, (405, 0))
        pygame.display.flip()

    def getCommands(self):
        '''
        getCommands(self) - Tracks all user actions/events (clicks and keypresses)
                in the game.
        '''
        #Hold Keys for fluid movement
        pygame.event.clear(pygame.MOUSEBUTTONUP)
        pygame.event.clear(pygame.MOUSEBUTTONDOWN)
        pygame.event.clear(pygame.MOUSEMOTION)


        for event in pygame.event.get(pygame.KEYDOWN):   # gets keydown events and clears queue
            if event.key == pygame.K_RIGHT:  #right arrow
                self.spec.forward = True
            if event.key == pygame.K_LEFT:   #left arrow
                self.spec.backward = True
            if event.key == pygame.K_UP:
                if self.spec.falling is False:
                    jump_sound.play()
                    self.spec.jumpTimeElapsed = pygame.time.get_ticks() #initial store of milliseconds to evaluate length of keypress
                    self.spec.jump = True
            if event.key == pygame.K_ESCAPE:
                self.powerup_music.stop()
                self.levelStatus = menu.pauseScreen()
            if event.key == pygame.K_s:
                self.safe_mode = not self.safe_mode     #deactive or activate safe mode
                if self.safe_mode:
                    print ("Safemode activated")
                else:
                    print ("Safemode not active")

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
        '''
        updateSprites(self) - Updates all sprites positions and events that occur,
                including: sound events, powerups, mob collisions, map interactions,
                light object interactions, block interactions, scrolling effects
                on mob persistence, and boundary wall.
        '''
        self.sprites.update(self.powerUpActive, self.sprites, self.mobs, self.spec.rect.x)

        if self.powerUpActive == True:
            self.powerup_music.play(1)
            self.powerUpTimer -= 1      #reduce timer
            if self.powerUpTimer <= 0:
                #Rest Power Up timer
                self.powerUpActive = False
                self.powerUpTimer = 0
        else:
            self.powerup_music.stop()

        # Test Spec for collisions with a mob
        collision_mob = pygame.sprite.spritecollide(self.spec, self.mobs, False)
        if len(collision_mob) != 0 and not self.safe_mode and not self.powerUpActive:
            self.loseLife()
            return

        # Test Spec for death below the map
        if self.spec.rect.top >= HEIGHT:
            self.loseLife()
            return

        # Test Spec for collisions with tiles in environment
        self.tileCollisions()

        # Check if there is a collision with spec and the light object
        collide_light = pygame.sprite.spritecollide(self.spec, self.lights, False)
        if len(collide_light) != 0:
            self.powerup_music.stop()
            if self.whichLevelToPlay == "BLUE":
                self.setLightAcquired("blue")
            elif self.whichLevelToPlay == "GREEN":
                self.setLightAcquired("green")
            elif self.whichLevelToPlay == "RED":
                self.setLightAcquired("red")
            else:
                print("game.updateSprites: ERROR IN SETTING LIGHT ACQUIRED")
            self.endCurrentLevel = 1

        # Check if collision between Spec and powerup
        collide_powerUp = pygame.sprite.spritecollide(self.spec, self.powerUpGroup, True)
        if len(collide_powerUp) != 0:
            self.powerUpActive = True
            self.powerUpOnMap = False
            self.powerUpTimer = 600

        # Trying to detect collisions for ultraviolet mobs and walls
        for mob in pygame.sprite.groupcollide(self.uv_mobs, self.all_blocks, False, False):
            # moving rect.x by 3 is done because 1 or 2 would leave mobs stuck in walls sometimes
            if mob.left == True:
                mob.rect.x += 3         # Move mob right slightly
                mob.left = False        # Change moving direction to right
            else:
                mob.rect.x -=3          # Move mob left slightly
                mob.left = True         # Change moving direction to left
            mob.step = 0                # Reset stepcount

        # Check for a collision between the invisible wall block and the sky blocks kill sky block
        for block in self.sky_blocks:
            # If midpoint of skyblock touches invisible wall center delete skyblock
            if block.rect.midright <= self.invisible_block.rect.center:
                #print("Block should be deleted at this point")
                block.kill()    #Remove block from its groups (Don't draw object anymore)

        for mob in self.mobs:
            # if mob touches invisible wall center delete mob
            if mob.rect.midright <= self.invisible_block.rect.center:
                #print ("Killing mob!")
                mob.kill()

        # Check for a collision between the invisible_wall_block and spec
        collide_invisible_wall = pygame.sprite.spritecollide(self.spec, self.invisible_wall_block, False)
        if len(collide_invisible_wall) != 0:
            self.spec.rect.x += 1       # Move Spec forward slightly so he is off the invisible_wall_block
            self.spec.speed[1] = 0      # Set backward speed to 0 so Spec can't move backwards

        # Moving the Blocks based on time
        if len(self.sky_blocks) > 0:
            self.block_timer += 1
            if self.block_timer == 3:
                if self.block_movement_counter < 50:
                    self.block_movement_counter += 1
                    for block in self.sky_blocks:
                        block.rect.x += 1        # Move blocks right
                        block.moving_left = False
                        block.moving_right = True
                elif self.block_movement_counter < 100:
                    self.block_movement_counter += 1
                    for block in self.sky_blocks:
                        block.rect.x -= 1        # Move blocks left
                        block.moving_left = True
                        block.moving_right = False
                else:
                    self.block_movement_counter = 0
                    block.moving_left = False
                    block.moving_right = False
                self.block_timer = 0
                self.platformMotion()  #Move spec if collision with sky_blocks occurs

        # Scrolling happens last in updateSprites. Scroll if the following are true:
        # Spec is within WIDTH-300 of the screen, Spec is not at rest, The light object is above WIDTH-40
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
            # Move Power up if it exists
            if self.powerUpOnMap == True and self.powerUpActive == False:
                self.powerUp.rect.x -= self.spec.speed[0]
            # Move Background Blocks
            for bg_block in self.bg_blocks:
                bg_block.rect.x -= self.spec.speed[0]
            # Scroll Background image based on which level we're playing
            if self.whichLevelToPlay == "BLUE":
                self.background_x -= (len(bluebox[0]) * 20 / self.background.get_width()) * .60  # map pixels / background image pixels
            elif self.whichLevelToPlay == "GREEN":
                self.background_x -= (len(greenbox[0]) * 20 / self.background.get_width()) * .60  # map pixels / background image pixels
            elif self.whichLevelToPlay == "RED":
                self.background_x -= (len(redbox[0]) * 20 / self.background.get_width()) * .60  # map pixels / background image pixels

        self.blackHoleGravity()

    def tileCollisions(self):
        '''
        tileCollisions(self) - Detects all collisions between spec and tiles
                in environment and adjusts player movement and location accordingly
        '''
        top_collision = False
        collisions = pygame.sprite.spritecollide(self.spec, self.all_blocks, False)
        if len(collisions) != 0:
            rightmost = leftmost = highest = lowest = collisions[0]
            #determine relative positioning of objects
            for collision in collisions:
                if collision.rect.left < leftmost.rect.left:
                    leftmost = collision
                if collision.rect.right > rightmost.rect.right:
                    rightmost = collision
                if collision.rect.bottom > lowest.rect.bottom:
                    lowest = collision
                if collision.rect.top < highest.rect.top:
                    highest = collision
            #prohibits assignment of rightmost/leftmost blocks to bottom collision logic
            if self.spec.speed[0] > 0 and (self.spec.jump or self.spec.falling) and rightmost.rect.bottom <= self.spec.rect.bottom:
                lowest = None
            if self.spec.speed[1] > 0 and (self.spec.jump or self.spec.falling) and leftmost.rect.bottom <= self.spec.rect.bottom:
                lowest = None
            #prohibits "sticking" to the wall
            if (self.spec.forward or self.spec.backward) and self.spec.jump is False:
                highest = None
            if lowest is not None:
                grounded = False #indicates whether sprite is grounded
                if self.spec.falling and self.spec.rect.center[1] - self.spec.shadow['center'][1] >= 3:
                    if self.spec.rect.bottom <= lowest.rect.bottom: #prohibits falling through floor while falling at higher rates of speed
                        grounded = True
                elif self.spec.jump:
                    if self.spec.rect.bottom <= lowest.rect.top + 1: #least forgiving threshold for jumping
                        grounded = True
                elif self.spec.rect.bottom <= lowest.rect.centery: #medium-level threshold while walking
                    grounded = True
                if grounded:
                    self.spec.rect.bottom = lowest.rect.top + 1 #reposition spec slightly below top of object
                    self.spec.falling = False
                    self.spec.fallTimer = 0  # reset falltimer
            if highest is not None:
                if self.spec.rect.top - highest.rect.bottom <= 0 and self.spec.rect.top - highest.rect.bottom >= -10:  #top collision
                    if self.spec.forward and highest.rect.centerx - self.spec.rect.centerx > 18.5: #permits spec to jump smoothly against walls
                        pass
                    elif self.spec.backward and self.spec.rect.centerx - highest.rect.centerx > 18.5: #permits spec to jump smoothly against walls
                        pass
                    else:
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

    def loseLife(self):
        '''
        loseLife(self) - Generates appropriate screen when Spec loses life
                or all lives and map restarts or game ends
        '''
        self.powerup_music.stop()
        self.loseAnimation()
        self.spec.kill()
        self.levelStatus = "restart"    #go back to main menu for now

        #Spec has lost all 7 of his lives
        if self.lives <= 1:
            self.lives -= 1
            menu.finalGameOverScreen()  #no more lives show finalGameOverScreen
            self.gameLost = True

        elif self.lives > 1:
            self.lives -= 1
            menu.gameOverScreen()            #leave game.updateSprites

    def platformMotion(self):
        '''
        platformMotion(self) - Detect whether spec is on a moving platform and
                adjust x coordinate accordingly
        '''
        top_collision = False
        collisions = pygame.sprite.spritecollide(self.spec, self.sky_blocks, False)
        if len(collisions) != 0:
            rightmost = leftmost = highest = lowest = collisions[0]
            #determine relative positioning of objects
            for collision in collisions:
                if collision.rect.left < leftmost.rect.left:
                    leftmost = collision
                if collision.rect.right > rightmost.rect.right:
                    rightmost = collision
                if collision.rect.bottom > lowest.rect.bottom:
                    lowest = collision
                if collision.rect.top < highest.rect.top:
                    highest = collision
            #prohibits assignment of rightmost/leftmost blocks to bottom collision logic
            if self.spec.forward and (self.spec.jump or self.spec.falling) and rightmost.rect.bottom <= self.spec.rect.bottom:
                lowest = None
            if self.spec.backward and (self.spec.jump or self.spec.falling) and leftmost.rect.bottom <= self.spec.rect.bottom:
                lowest = None
            #prohibits "sticking" to the wall
            if (self.spec.forward or self.spec.backward) and self.spec.jump is False:
                highest = None
            if lowest is not None:
                grounded = False #indicates whether sprite is grounded
                if self.spec.falling and self.spec.rect.bottom <= lowest.rect.bottom: #prohibits falling through floor while falling
                    grounded = True
                elif self.spec.rect.bottom <= lowest.rect.centery: #less forgiving threshold while walking
                    grounded = True
                if grounded:
                    if lowest.moving_left:
                        self.spec.rect.x -= 1
                        return
                    else:
                        self.spec.rect.x += 1
                        return


    def checkStatus(self):
        '''
        checkStatus(self) - Checks for the quit event.
        '''
        if pygame.event.get(pygame.QUIT): #check if QUIT event. Return status false to terminate game
            self.status = False

    def setLightAcquired(self, light):
        '''
        setLightAcquired(self, light) - Sets appropriate light variable when Spec acquires
                a light at the end of a level.
        '''
        # Set light acquired game variable. 1 is acquired, 0 is not acquired (default)
        if light == "blue":
            self.blue_light_acquired = 1
        elif light == "red":
            self.red_light_acquired = 1
        elif light == "green":
            self.green_light_acquired = 1
        else:
            print("game.setLightAcquired: ERROR IN SETTING LIGHT ACQUIRED")

    def checkLightAcquired(self, light):
        '''
        checkLightAcquired(self, light) - accepts a light parameter and checks
                if that light has been acquired or not
        Returns - Appropriate light acquired variable which is set to 1 or 0
                depending on whether it's been acquired or not.
        '''
        # Check if a light has been acquired. Return its boolean value
        if light == "blue":
            return self.blue_light_acquired
        elif light == "red":
            return self.red_light_acquired
        elif light == "green":
            return self.green_light_acquired
        else:
            print("game.checkLightAcquired: Unknown light passed to function")

# -----Load Game sounds------
mob_sounds = [] #Initialize mob sounds list
mob_ray = pygame.mixer.Sound('sounds/mob_ray.wav')  #Mob Ray Sound for Gamma Mobs
mob_ray.set_volume(0.05)
mob_sounds.append(mob_ray)
mob_jump = pygame.mixer.Sound('sounds/mob_jump.wav')#Mob Jump Sound for Infrared Mobs
mob_jump.set_volume(0.15)
mob_sounds.append(mob_jump)

# -----Spec Sound Effects------
jump_sound = pygame.mixer.Sound('sounds/jump_01.ogg')  #Platformer Jumping Sounds CC-BY 3.0 by dklon (https://opengameart.org/content/platformer-jumping-sounds)
jump_sound.set_volume(0.5)
death_yell = pygame.mixer.Sound('sounds/spec_die.wav')
death_yell.set_volume(.3)
death_yell_alternate = pygame.mixer.Sound('sounds/Wilhelm_Scream.wav')
death_yell_alternate.set_volume(0.5)


game = Game(mob_sounds) #Initialize game object

# -----Load Menu sounds------
click = pygame.mixer.Sound('sounds/click.ogg')
click.set_volume(0.5)
lose_music = pygame.mixer.Sound('sounds/lose_music.ogg')
win_music = pygame.mixer.Sound('sounds/win_music.ogg')
# Music by Otto Halmén - https://opengameart.org/content/death-is-just-another-path
final_death = pygame.mixer.Sound('sounds/Death Is Just Another Path.ogg')

# -----Load Menu sounds into a list------
menu_sounds = [click, lose_music, win_music, final_death]

# -----Load Menu images------
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
forestlevel_inactive = pygame.image.load('images/forestlevel_inactive.png').convert()
forestlevel_active = pygame.image.load('images/forestlevel_active.png').convert()
desertlevel_inactive = pygame.image.load('images/desertlevel_inactive.png').convert()
desertlevel_active = pygame.image.load('images/desertlevel_active.png').convert()
dead_spec = pygame.image.load('images/spec_died.png').convert()
frame_img = pygame.image.load('images/frame.png').convert()
powerUp_image = pygame.image.load('images/power_up_img.png').convert()

# -----Create Menu Images List and Add all Images------
menu_imgs = []
menu_imgs.extend((bl_light_img, rd_light_img, gr_light_img, vol_slider, \
 vol_bar, vol_arr_right, vol_arr_left, play_btn_inactive, play_btn_active, \
 fullscreen_inactive, fullscreen_active, skylevel_inactive, skylevel_active, \
 forestlevel_inactive, forestlevel_active, desertlevel_inactive, desertlevel_active, \
 dead_spec, frame_img))

# -----Load Light Images------
bl_light_1 = pygame.image.load('images/bl_light_endGame1.png').convert()
bl_light_2 = pygame.image.load('images/bl_light_endGame2.png').convert()
green_light_1 = pygame.image.load('images/green_light_endGame1.png').convert()
green_light_2 = pygame.image.load('images/green_light_endGame2.png').convert()
red_light_1 = pygame.image.load('images/red_light_endGame1.png').convert()
red_light_2 = pygame.image.load('images/red_light_endGame2.png').convert()

# -----Add Light Images to Appropriate Lists------
bl_light_endGame_imgs = []
bl_light_endGame_imgs.extend((bl_light_1, bl_light_2))
green_light_endGame_imgs = []
green_light_endGame_imgs.extend((green_light_1, green_light_2))
red_light_endGame_imgs = []
red_light_endGame_imgs.extend((red_light_1, red_light_2))

 # Initialize Menu Object
menu = Menu(game.screen, time, menu_imgs, menu_sounds)
openMenu = True # Flag variable to track whether in a menu screen or not
first_playthrough = True # Tracks if first playthrough to display start screen or not.
music_vol = 0.5

# Open the Menu
while(openMenu):
    #If first playthrough, open start screen and then the main Menu
    if first_playthrough == True:
        menu.startScreen()
        music_vol, fullScreen, levelSelect = menu.mainMenu(game)
    else:
        #Otherwise, skip start screen and only open the main Menu
        pygame.mixer.music.load(MENU_BG_MUSIC)
        pygame.mixer.music.set_volume(music_vol)
        pygame.mixer.music.play(-1) # -1 = loop the song
        music_vol, fullScreen, levelSelect = menu.mainMenu(game)

    game.resetScreenSize(fullScreen) #Checks if user selected or de-selected fullscreen
    game.startup(levelSelect) #Starts game

    active = True
    game.status = True

    # Main Game Loop
    while(active):
        # Check is Spec Lost all his lives
        if game.gameLost == True:
            game.resetGame()

        # Check if all lights have been acquired ; End game if true
        if game.checkLightAcquired("blue") \
        and game.checkLightAcquired("red") \
        and game.checkLightAcquired("green"):
            game.endAnimation()
            menu.gameCompletedScreen()
            game.resetGame()
            break
         #Check for end level status
        if game.endCurrentLevel == 1:
            menu.completeLevel()
            game.endCurrentLevel = 0
            break

        #Increment time
        time.tick(FRAMES)

        game.checkStatus()
        active = game.status #check if game is still active based on game status
        if not active:
            openGame = False

        # Obtain keyboard inputs
        game.getCommands()

        #Check level status to see if level is exited from Pause Menu
        status = game.levelStatus

        #If level exited, reset level status
        if status == "restart":
            game.levelStatus = ""
            game.powerup_music.stop()
            break

        # Update sprites and background
        game.updateSprites()

        # Check status and don't drawScreen if death on that frame
        status = game.levelStatus
        if status == "restart" and game.gameLost != True:
            game.levelStatus = ""
            break

        # Check is Spec Lost all his lives
        if game.gameLost == True:
            game.resetGame()
            break

        # Print to screen
        game.drawScreen()

    first_playthrough = False;

game.shutdown()
