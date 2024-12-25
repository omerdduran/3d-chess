GAME_NAME = 'Chess Game'

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
THREATENED_SQUARE = (231, 76, 60, 80)  # Semi-transparent red for threatened squares
KING_DANGER = (192, 57, 43, 120)  # Darker red for king in check

# Game Over Colors
WINNER_COLOR = (46, 204, 113)  # Green for winner
LOSER_COLOR = (231, 76, 60)    # Red for loser
DRAW_COLOR = (52, 152, 219)    # Blue for draw

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

# Animation Settings
ANIMATION_SPEED = 8  # Pixels per frame
ANIMATION_FPS = 60   # Animation frame rate
MIN_ANIMATION_SPEED = 2  # Minimum speed at the end of animation
ANIMATION_SMOOTHING = 0.85  # Smoothing factor for animation (0-1)

# Promotion Settings
PROMOTION_PANEL_WIDTH = 400
PROMOTION_PANEL_HEIGHT = 120
PROMOTION_PIECE_SIZE = 80
PROMOTION_BG = (248, 249, 250)  # Light background
PROMOTION_BORDER = (222, 226, 230)  # Border color
PROMOTION_HOVER = (233, 236, 239)  # Hover color

# Menu Settings
MENU_BG = (248, 249, 250)  # Light background
MENU_BUTTON_BG = (255, 255, 255, 230)  # Semi-transparent white
MENU_BUTTON_HOVER = (255, 255, 255, 255)  # Full white on hover
MENU_BUTTON_ACTIVE = (64, 169, 255)  # Active button color
MENU_BUTTON_WIDTH = 300
MENU_BUTTON_HEIGHT = 60
MENU_BUTTON_SPACING = 20  # Space between buttons
MENU_TITLE_SIZE = 82  # Slightly larger title
MENU_BUTTON_TEXT_SIZE = 36
MENU_PANEL_ALPHA = 180  # Transparency for menu panel
MENU_TITLE_COLOR = (33, 37, 41)  # Dark text for title
MENU_SUBTITLE_SIZE = 28  # Size for subtitle text
MENU_BUTTON_SHADOW = (0, 0, 0, 30)  # Soft shadow for buttons
MENU_BUTTON_BORDER_RADIUS = 10  # Rounded corners for buttons

# Menu button texts
MENU_BUTTON_NEW_GAME = "New Game"
MENU_BUTTON_SAVE_GAME = "Save Game"
MENU_BUTTON_LOAD_GAME = "Load Game"
MENU_BUTTON_QUIT = "Quit"

# Menu button colors
MENU_BUTTON_SAVE = (46, 204, 113)  # Green for save
MENU_BUTTON_LOAD = (52, 152, 219)  # Blue for load

# Game saving/loading settings
SAVE_DIR = "saved_games"
SAVE_MESSAGE_DURATION = 2  # seconds
LOAD_MESSAGE_DURATION = 2  # seconds