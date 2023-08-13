TILE_SIZE = 40
FPS = 60

BUTTON_TEXT_COLOR = "#FCD029"

DIFFICULTY = "EASY"

EASY_DIFFICULTY_TIME = 0.5
MIDDLE_DIFFICULTY_TIME = 0.25
HARD_DIFFICULTY_TIME = 0.10

BOARD_WIDTH = 10
BOARD_HEIGHT = 20

MOVE_TIME = 0.4  # seconds
SCORE_NUMBER = 500

GRID_THICK = 1
CELL_ANGLE = 4

# code positions were reversed, so lower cells go further ahead
TETRO_CODES = [[[0, 0], [1, 0], [-1, -1], [-1, 0]],
                   [[0, 0], [1, 0], [-1, 0], [0, -1]],
                   [[0, 0], [1, 0], [-2, 0], [-1, 0]],
                   [[0, 0], [0, -1], [-1, -1], [-1, 0]],
                   [[0, 0], [1, 0], [-1, -1], [0, -1]],
                   [[0, 0], [0, -1], [1, -1], [-1, 0]],
                   [[0, 0], [0, -1], [-2, 0], [-1, 0]]]
TETRO_COLORS = ["#0A6EBD", "#8062D6", "#97FEED", "#F1C93B", "#F31559", "#F31559", "#E57C23"]
