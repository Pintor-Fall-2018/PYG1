# Spectrum.py
import pygame, sys, os
import random
from settings import *
from menu import *

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

    def startup(self):
        #Create Start Up Game timers and counters
        self.block_movement_counter = 0
        self.blockTimer = pygame.time.get_ticks()

        # Create Groups()
        self.sprites = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()         # Moving blocks
        self.ground_blocks = pygame.sprite.Group()  # Ground blocks don't move!

        # Create Game Objects and add to their Groups()
        self.spec = Spec()
        self.sprites.add(self.spec)

        #Initialize blocks by picking from BLOCK_LIST to use from settings and add to Groups
        block_counter = 0
        for block in BLOCK_LIST:
            print ('printing block ', block_counter)
            block_counter += 1
            b = Block(*block) # explode list from block in BLOCK_LIST
            self.sprites.add(b)
            self.blocks.add(b)

        # Initalize ground blocks
        for ground_block in GROUND_BLOCK_LIST:
            gb = Block(*ground_block)
            self.sprites.add(gb)
            self.ground_blocks.add(gb)


        if DEBUG:
            print('Pygame Version: ' + pygame.version.ver)
            print('Platform: ' + sys.platform)

    def shutdown(self):
        pygame.quit()
        sys.exit()

    def drawScreen(self):
        self.screen.fill(BLACK)
        self.sprites.draw(self.screen)
        pygame.display.flip()

    def getCommands(self):
        #Hold Keys for fluid movement
        for event in pygame.event.get(pygame.KEYDOWN):   # gets keydown events and clears queue
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
                    self.spec.jump = True
            if event.key == pygame.K_ESCAPE:
                status = menu.pauseScreen()
                print("Status: ", status)
                if status == "restart":
                    return status


        for event in pygame.event.get(pygame.KEYUP):
            if event.key == pygame.K_RIGHT:  #right arrow
                self.spec.forward = False
                self.spec.slowForward = True
            if event.key == pygame.K_LEFT:   #left arrow
                self.spec.backward = False
                self.spec.slowBackward = True

    def updateSprites(self):
        self.sprites.update()

        collisions = pygame.sprite.spritecollide(self.spec, self.blocks, False)
        ground_collisions = pygame.sprite.spritecollide(self.spec, self.ground_blocks, False)
        if len(collisions) or len(ground_collisions) != 0:
            self.spec.falling = False
            self.spec.fallTimer = 0  # reset falltimer
            if DEBUG:
                print(collisions)
                print(ground_collisions)
        else:
            if self.spec.jump == False:
                self.spec.falling = True


        # Moving the Blocks based on time
        self.timeSinceInit = pygame.time.get_ticks() #get time since overall game ticks
        if self.timeSinceInit - self.blockTimer > 50: # Check if it has been 1000ms
            #print("time should be above 1000 ms: ", self.timeSinceInit - self.blockTimer)
            self.blockTimer = self.timeSinceInit
            self.timeSinceInit = 0
            if self.block_movement_counter < 50:
                self.block_movement_counter += 1
                for block in self.blocks:
                    block.rect.x += 1        # Move blocks right
            elif self.block_movement_counter < 100:
                self.block_movement_counter += 1
                for block in self.blocks:
                    block.rect.x -= 1        # Move blocks left
            else:
                self.block_movement_counter = 0

        # Scrolling happens in the updateSprites part of game
        if (self.spec.rect.x > WIDTH - 150) and self.spec.speed[0] is not 0:
            #self.spec.rect.y -= 100
            self.spec.rect.x -= self.spec.speed[0]
            #self.block.rect.y -=100
            for block in self.blocks:
                block.rect.x -= self.spec.speed[0]

    def checkStatus(self):
        if pygame.event.get(pygame.QUIT): #check if QUIT event. Return status false to terminate game
            self.status = False

class Spec(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #sprite constructor
        #self.image = pygame.Surface((30,30)) #width x height
        #self.image.fill((100,100,0))
        self.step = 0
        self.resting_spec = pygame.image.load('images/spec0.png').convert()
        self.resting_spec.set_colorkey([34,177,76])
        self.animations = []
        self.animations.append(pygame.image.load('images/spec1.png').convert())
        self.animations.append(pygame.image.load('images/spec2.png').convert())
        self.animations.append(pygame.image.load('images/spec3.png').convert())
        self.animations.append(pygame.image.load('images/spec4.png').convert())
        for animation in self.animations:
            animation.set_colorkey([34,177,76])
        self.image = self.resting_spec
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 200
        self.forward = False  #sprite forward movement
        self.backward = False #sprite backward movement
        self.slowForward = False  #slowing forward movement
        self.slowBackward = False  #slowing backward movement
        self.falling = True
        self.jumpTimer = 40
        self.fallTimer = 0
        self.jump = False
        self.speed = [0,0]  #[forward, backward]

    def update(self):
        if self.falling:  #gravity increases velocity
            self.rect.y += self.fallTimer
            self.fallTimer += .5
            if self.fallTimer > 6:
                self.fallTimer = 6
        if self.forward:  #speeds up sprite in right direction
            self.rect.x += self.speed[0]
            self.speedlimiter('forward')
            self.animate()
        elif self.backward: #speeds up sprite in left direction
            self.rect.x -= self.speed[1]
            self.speedlimiter('backward')
            self.animate()
        elif self.slowForward:  #slows down sprite in right direction
            self.speed[0] -= .5
            self.rect.x += self.speed[0]
            if self.speed[0] < 0:
                self.slowForward = False
                self.speed[0] = 0
        elif self.slowBackward:  #slows down sprite in left direction
            self.speed[1] -= .5
            self.rect.x -= self.speed[1]
            if self.speed[1] < 0:
                self.slowBackward = False
                self.speed[1] = 0
        else:  #sprite at rest
            self.resting()
            self.speed = [0,0]

        #Jump mechanics
        if self.jump == True and self.jumpTimer > 20:  #upward arc
            self.rect.y -= self.jumpTimer / 5
            self.jumpTimer -= 1
        elif self.jump == True:  #downward arc
            self.falling = True
            self.jump = False
            self.jumpTimer = 40  # reset timer

    #Sprite acceleration & deceleration
    def speedlimiter(self, direction):
        if direction == 'forward':
            self.speed[0] += .25
            if self.speed[0] > 6:
                self.speed[0] = 6
        if direction == 'backward':
            self.speed[1] += .25
            if self.speed[1] > 6:
                self.speed[1] = 6

    def animate(self):
        self.step += 1
        if self.step > 39:
            self.step = 0
        self.image = self.animations[int(self.step/10)]

    def resting(self):
        self.image = self.resting_spec

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, color):
        pygame.sprite.Sprite.__init__(self) #sprite constructor
        self.image = pygame.Surface([w, h]) #width x height
        self.image.fill(color)
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


menu_imgs = []
menu_imgs.extend((bl_light_img, rd_light_img, gr_light_img, vol_slider, vol_bar, vol_arr_right, vol_arr_left))

# Create menu object
menu = Menu(game.screen, time, menu_imgs)
openGame = True
count = 0
music_vol = 0.5

while(openGame):

    if count == 0:
        menu.startScreen()
        music_vol = menu.mainMenu()
    else:
        pygame.mixer.music.load(MENU_BG_MUSIC)
        pygame.mixer.music.set_volume(music_vol)
        pygame.mixer.music.play(-1) # -1 = loop the song
        music_vol = menu.mainMenu()

    game.startup()

    active = True

    # Main Game Loop
    while(active):
        #increment time
        time.tick(FRAMES)
        #print (time.tick(FRAMES)) prints how many frames of seconds has been passed

        game.checkStatus()
        active = game.status #check if game is still active based on game status
        if not active:
            openGame = False
        #obtain keyboard inputs
        status = game.getCommands()
        if status == "restart":
            print("RESTART!")
            break

        #update sprites
        game.updateSprites()

        #print to screen
        game.drawScreen()

    count += 1


game.shutdown()
