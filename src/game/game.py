import pygame
from src.board.board import *
from config.settings import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(GAME_NAME)
        
        self.clock = pygame.time.Clock()
        self.board = create_board()
        self.pieces_images = load_pieces()
        
        self.selected_piece = None
        self.selected_square = None
        self.valid_moves = []
        
        # Load sounds
        self.move_sound = pygame.mixer.Sound('assets/sounds/move.mp3')
        self.capture_sound = pygame.mixer.Sound('assets/sounds/capture.mp3')

    def handle_click(self, pos):
        """Handle mouse click events"""
        col = pos[0] // SQUARE_SIZE
        row = pos[1] // SQUARE_SIZE
        
        # If a piece is already selected
        if self.selected_piece:
            # Try to move the piece
            if (row, col) in self.valid_moves:
                # Check if target square has a piece (capture)
                is_capture = self.board[row][col] is not None
                
                # Move piece
                old_row, old_col = self.selected_square
                self.board[row][col] = self.board[old_row][old_col]
                self.board[old_row][old_col] = None
                
                # Update has_moved flag
                self.board[row][col].has_moved = True
                
                # Play appropriate sound
                if is_capture:
                    self.capture_sound.play()
                else:
                    self.move_sound.play()
                
                # Reset selection
                self.selected_piece = None
                self.selected_square = None
                self.valid_moves = []
            else:
                # Deselect if clicking on invalid square
                self.selected_piece = None
                self.selected_square = None
                self.valid_moves = []
        
        # If no piece is selected, try to select one
        else:
            piece = self.board[row][col]
            if piece:
                self.selected_piece = piece
                self.selected_square = (row, col)
                # Get valid moves for the selected piece
                self.valid_moves = piece.get_valid_moves(self.board, row, col)

    def draw(self):
        """Draw the game state"""
        # Draw board
        draw_board(self.screen)
        
        # Highlight selected square
        if self.selected_square:
            row, col = self.selected_square
            pygame.draw.rect(
                self.screen,
                HIGHLIGHT,
                (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            )
        
        # Highlight valid moves
        for row, col in self.valid_moves:
            pygame.draw.circle(
                self.screen,
                POSSIBLE_MOVE,
                (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2),
                15
            )
        
        # Draw pieces
        draw_pieces(self.screen, self.board, self.pieces_images)
        
        pygame.display.flip()

    def run(self):
        """Main game loop"""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        self.handle_click(event.pos)
            
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()
