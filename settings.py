# settings.py
# settings file

WIDTH = 600
HEIGHT = 400
RESOLUTION = (600, HEIGHT)  # width x height
FRAMES = 60   # Frames per second
TITLE = "Spectrum v1.0"

#Debug Mode 1 == On 0 == Off
DEBUG = 0
DEBUG_MENU = 0

BLACK = (0, 0, 0)
GRAY = (192,192,192)
WHITE = (255, 255, 255)
RED = (168, 7, 7)
GREEN = (0, 150, 0)
BLUE = (0, 0, 255)

LIGHT_RED = (255, 50, 0)
LIGHT_GREEN = (0, 255, 0)

# Map Settings
MAX_RIGHT_WIDTH = 1500 # Maximum distance to the right that the map goes

# Block Lists. These lists will be the platform lists for the entire levels 1-3
# Block __init__(self, x, y, w, h, color):

# Block list Sky (Level 1)
# This is currently the only level
BLOCK_LIST = [(-100, 350, MAX_RIGHT_WIDTH, 200, GREEN),
              (100, 275, 100, 20, GRAY),
              (600, 275, 100, 20, BLUE)]

# Block List Forest (Level 2)

# Block List Desert (Level 3)
