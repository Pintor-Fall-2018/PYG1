# settings.py
# settings file

WIDTH = 600
HEIGHT = 400
RESOLUTION = (WIDTH, HEIGHT)  # width x height
FRAMES = 60   # Frames per second
TITLE = "Spectrum v1.0"

#Debug Mode 1 == On 0 == Off
DEBUG = 0
DEBUG_MENU = 0

BLACK = (0, 0, 0)
GRAY = (192,192,192)
LIGHT_GRAY = (210, 210, 210)
WHITE = (255, 255, 255)
RED = (168, 7, 7)
LIGHT_RED = (255, 50, 0)
DARK_RED = (102, 4, 4)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
PASTEL_BLUE = (106, 194, 245)
PASTEL_BLUE_2 = (106, 155, 245)
LIGHT_BLUE = (70, 238, 238)
SKY_BLUE = (224, 248, 254)


GREEN = (0, 150, 0)
LIGHT_GREEN = (0, 255, 0)
DARK_GREEN = (0, 105, 1)

# Map Settings
MAX_RIGHT_WIDTH = 1500 # Maximum distance to the right that the map goes

# Block Lists. These lists will be the platform lists for the entire levels 1-3
# Block __init__(self, x, y, w, h, color):

# Ground Blocks that don't move. This is the base platforms
GROUND_BLOCK_LIST = [(-100, 350, MAX_RIGHT_WIDTH, 200, GREEN)]

# Block list Sky (Level 1)
# This is currently the only level
BLOCK_LIST = [(100, 250, 100, 20, GRAY),
              (200, 125, 100, 20, RED),
              (350, 125, 100, 20, RED),
              (500, 125, 100, 20, RED),
              (650, 125, 100, 20, RED),
              (800, 125, 100, 20, RED),
              (600, 275, 100, 20, BLUE),
              (900, 275, 100, 20, DARK_RED)
              ]

# Block List Forest (Level 2)

# Block List Desert (Level 3)

# Menu Colors
MAINMENU_BG = BLACK
MENU_BG_MUSIC = "sounds/acción.ogg"
MUSIC_VOL = 1.0
