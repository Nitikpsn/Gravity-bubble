WIDTH = 600
HEIGHT = 500
FPS = 60

GRAVITY = 0.09
WALL_BOUNCE = 0.85
COLLISION_BOUNCE = 0.9

SPAWN_FRAMES = 30

MIN_RADIUS = 20
MAX_RADIUS = 45
MIN_SPEED = 0.5
MAX_SPEED = 2.5
MAX_DRIFT = 1.5

# Plain black theme: black background, monochrome bubbles, white text.
BACKGROUND = (0, 0, 0)
TEXT_COLOR = (255, 255, 255)
OUTLINE_COLOR = (255, 255, 255)
OUTLINE_WIDTH = 2

MIN_COLOR = 60
MAX_COLOR = 255

# Physics runs in "frames" (1.0 = a 60 FPS frame).
# Cap the frame step so a slow frame can never launch a bubble across the screen.
MAX_FRAME_STEP = 3.0
SCORE_POS = (20, 20)
FONT_PATH = "GrapeSquishy.woff"
FONT_SIZE = 40
