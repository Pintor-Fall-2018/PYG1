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

BLUE = (0, 0, 255)
PASTEL_BLUE = (106, 194, 245)
PASTEL_BLUE_2 = (106, 155, 245)
LIGHT_BLUE = (70, 238, 238)


GREEN = (0, 150, 0)
LIGHT_GREEN = (0, 255, 0)
DARK_GREEN = (0, 105, 1)

# Map Settings
MAX_RIGHT_WIDTH = 1500 # Maximum distance to the right that the map goes

# Block Lists. These lists will be the platform lists for the entire levels 1-3
# Block __init__(self, x, y, w, h, color):

# Block list Sky (Level 1)
# This is currently the only level
BLOCK_LIST = [(0, 350, MAX_RIGHT_WIDTH, 200, GREEN),
              (100, 275, 100, 20, GRAY),
              (600, 275, 100, 20, BLUE)]

# Menu Colors
MAINMENU_BG = BLACK
MENU_BG_MUSIC = "sounds/Convert.ogg"
