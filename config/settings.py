GAME_NAME = '3D Chess Game'

# Window dimensions
WINDOW_WIDTH = 1200  # Increased width for more space
WINDOW_HEIGHT = 1000
BOARD_SIZE = 680    # Slightly larger board
SQUARE_SIZE = BOARD_SIZE // 8

# Board position
BOARD_OFFSET_X = (WINDOW_WIDTH - BOARD_SIZE) // 2
BOARD_OFFSET_Y = 80  # Moved up slightly

# Game settings
FPS_LIMIT = 60
INITIAL_TIME = 1 * 60    # 1 minute in seconds for each player
TIME_WARNING = 50       # Warning when 60 seconds left
TIME_CRITICAL = 30      # Critical time warning when 30 seconds left

# Modern Color Scheme
WHITE = (248, 249, 250)      # Off-white background
BLACK = (33, 37, 41)         # Dark gray, almost black
GRAY = (173, 181, 189)       # Medium gray
LIGHT_GRAY = (233, 236, 239) # Light gray for panels
PRIMARY = (64, 169, 255)     # Bright blue for highlights
SECONDARY = (108, 117, 125)  # Dark gray for text
WARNING = (255, 193, 7)      # Warning color (yellow)
DANGER = (220, 53, 69)       # Danger color (red)

# Board Colors
LIGHT_SQUARE = (237, 238, 240)  # Very light gray
DARK_SQUARE = (125, 135, 150)   # Medium blue-gray
HIGHLIGHT = (87, 204, 153)      # Soft green
POSSIBLE_MOVE = (108, 117, 125)  # Base color for move indicators
POSSIBLE_MOVE_ALPHA = (108, 117, 125, 100)  # Semi-transparent version for overlays

# UI Colors
TEXT_COLOR = (33, 37, 41)     # Dark gray for text
PANEL_BG = (248, 249, 250)    # Light background for panels
PANEL_BORDER = (222, 226, 230) # Light gray for borders
ACTIVE_COLOR = (64, 169, 255)  # Bright blue for active elements

# UI Settings
SIDE_PANEL_WIDTH = 220        # Wider panels
CAPTURED_PIECE_SIZE = 45      # Slightly larger captured pieces
FONT_SIZE_LARGE = 40
FONT_SIZE_MEDIUM = 28
FONT_SIZE_SMALL = 20

# Move History Panel Settings
HISTORY_PANEL_HEIGHT = 180    # Taller history panel

# Piece Settings
PIECE_SCALE = 0.90           # Scale pieces to 90% of square size