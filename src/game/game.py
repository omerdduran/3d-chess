import pygame
from src.board.board import *
from config.settings import *
from src.utils.logger import logger
from src.pieces.queen import Queen
from src.pieces.rook import Rook
from src.pieces.bishop import Bishop
from src.pieces.knight import Knight
from src.utils.game_saver import GameSaver

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(GAME_NAME)
        
        self.clock = pygame.time.Clock()
        self.board = create_board()
        self.pieces_images = load_pieces()
        
        # Game state
        self.selected_piece = None
        self.selected_square = None
        self.valid_moves = []
        self.current_turn = "white"  # White starts first
        
        # Animation state
        self.animating_piece = None
        self.animation_start = None
        self.animation_end = None
        self.animation_progress = 0
        self.animation_piece_image = None
        self.pending_move = None
        
        # Game tracking
        self.captured_pieces = {"white": [], "black": []}
        self.move_history = []
        self.move_count = 1
        
        # Timer initialization
        self.time_left = {"white": INITIAL_TIME, "black": INITIAL_TIME}
        self.last_tick = pygame.time.get_ticks()
        self.game_over = False
        
        # Initialize fonts
        self.font_large = pygame.font.Font(None, FONT_SIZE_LARGE)
        self.font_medium = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        self.font_small = pygame.font.Font(None, FONT_SIZE_SMALL)
        
        # Load sounds
        self.move_sound = pygame.mixer.Sound('assets/sounds/move.mp3')
        self.capture_sound = pygame.mixer.Sound('assets/sounds/capture.mp3')
        
        # Promotion state
        self.promotion_pending = False
        self.promotion_square = None
        self.promotion_color = None
        self.promotion_pieces = ["queen", "rook", "bishop", "knight"]

        # Initialize game saver
        self.game_saver = GameSaver()
        
        logger.info("New chess game started - White's turn")

    def save_current_game(self):
        """Save the current game state"""
        filename = self.game_saver.save_game(self)
        if filename:
            logger.info(f"Game saved as {filename}")
            return True
        return False

    def load_saved_game(self, filename):
        """Load a saved game state"""
        save_data = self.game_saver.load_game(filename)
        if not save_data:
            return False

        try:
            # Load board state
            self.board = self._deserialize_board(save_data["board_state"])
            self.current_turn = save_data["current_turn"]
            self.time_left = save_data["time_left"]
            self.move_history = save_data["move_history"]
            self.captured_pieces = self._deserialize_captured_pieces(save_data["captured_pieces"])
            self.move_count = save_data["move_count"]
            self.game_over = save_data["game_over"]

            # Reset selection and animation states
            self.selected_piece = None
            self.selected_square = None
            self.valid_moves = []
            self.animating_piece = None
            self.pending_move = None
            self.promotion_pending = False

            logger.info("Game loaded successfully")
            return True

        except Exception as e:
            logger.error(f"Error loading game state: {str(e)}")
            return False

    def _deserialize_board(self, board_state):
        """Convert saved board state back to piece objects"""
        piece_classes = {
            "pawn": Pawn,
            "rook": Rook,
            "knight": Knight,
            "bishop": Bishop,
            "queen": Queen,
            "king": King
        }

        board = [[None for _ in range(8)] for _ in range(8)]
        for row in range(8):
            for col in range(8):
                piece_data = board_state[row][col]
                if piece_data and isinstance(piece_data, dict):  # Check if it's a piece (dictionary)
                    piece_class = piece_classes[piece_data['position']]
                    piece = piece_class(piece_data['color'], piece_data['position'])
                    if 'has_moved' in piece_data:
                        piece.has_moved = piece_data['has_moved']
                    board[row][col] = piece
                else:
                    board[row][col] = None  # Empty square

        return board

    def _deserialize_captured_pieces(self, captured_data):
        """Convert saved captured pieces back to piece objects"""
        piece_classes = {
            "pawn": Pawn,
            "rook": Rook,
            "knight": Knight,
            "bishop": Bishop,
            "queen": Queen,
            "king": King
        }

        captured = {"white": [], "black": []}
        for color in ["white", "black"]:
            for piece_data in captured_data[color]:
                piece_class = piece_classes[piece_data['position']]
                piece = piece_class(piece_data['color'], piece_data['position'])
                captured[color].append(piece)

        return captured

    def get_saved_games(self):
        """Get list of saved games"""
        return self.game_saver.list_saved_games()

    def delete_saved_game(self, filename):
        """Delete a saved game"""
        return self.game_saver.delete_save(filename)

    def get_square_notation(self, row, col):
        """Convert row and column to chess notation (e.g., 'e4')"""
        files = 'abcdefgh'
        ranks = '87654321'
        return f"{files[col]}{ranks[row]}"

    def switch_turn(self):
        """Switch the current turn between white and black"""
        self.current_turn = "black" if self.current_turn == "white" else "white"
        logger.info(f"{self.current_turn.capitalize()}'s turn")
        
        # Reset selection and valid moves
        self.selected_piece = None
        self.selected_square = None
        self.valid_moves = []

    def add_to_move_history(self, piece, source, target, is_capture=False, captured_piece=None):
        """Add a move to the history"""
        move_text = f"{self.move_count}. "
        if piece.color == "white":
            move_text += f"White {piece.position.capitalize()} {source}-{target}"
            if is_capture:
                move_text += f" x{captured_piece.position.capitalize()}"
        else:
            move_text += f"Black {piece.position.capitalize()} {source}-{target}"
            if is_capture:
                move_text += f" x{captured_piece.position.capitalize()}"
            self.move_count += 1
        
        self.move_history.append(move_text)
        if len(self.move_history) > 10:  # Keep only last 10 moves
            self.move_history.pop(0)

    def animate_piece_movement(self, start_pos, end_pos, piece_image):
        """Start piece movement animation"""
        self.animating_piece = True
        self.animation_start = (
            BOARD_OFFSET_X + start_pos[1] * SQUARE_SIZE,
            BOARD_OFFSET_Y + start_pos[0] * SQUARE_SIZE
        )
        self.animation_end = (
            BOARD_OFFSET_X + end_pos[1] * SQUARE_SIZE,
            BOARD_OFFSET_Y + end_pos[0] * SQUARE_SIZE
        )
        self.animation_progress = 0
        self.animation_piece_image = piece_image

    def update_animation(self):
        """Update piece animation progress"""
        if self.animating_piece:
            self.animation_progress += ANIMATION_SPEED / 100
            if self.animation_progress >= 1:
                # Animation is complete, apply the pending move
                if self.pending_move:
                    from_pos = self.pending_move['from']
                    to_pos = self.pending_move['to']
                    is_capture = self.pending_move['is_capture']
                    captured_piece = self.pending_move['captured_piece']
                    source_square = self.pending_move['source_square']
                    target_square = self.pending_move['target_square']
                    
                    # Log the move
                    piece_type = self.board[from_pos[0]][from_pos[1]].position.capitalize()
                    color = self.board[from_pos[0]][from_pos[1]].color.capitalize()
                    
                    if is_capture:
                        # Add captured piece to the list
                        self.captured_pieces[self.current_turn].append(captured_piece)
                        logger.info(
                            f"{color} {piece_type} captures {captured_piece.color.capitalize()} "
                            f"{captured_piece.position.capitalize()} at {target_square} "
                            f"(moved from {source_square})"
                        )
                    else:
                        logger.info(
                            f"{color} {piece_type} moves from {source_square} to {target_square}"
                        )
                    
                    # Add move to history
                    self.add_to_move_history(
                        self.board[from_pos[0]][from_pos[1]],
                        source_square,
                        target_square,
                        is_capture,
                        captured_piece
                    )
                    
                    # Move piece
                    self.board[to_pos[0]][to_pos[1]] = self.board[from_pos[0]][from_pos[1]]
                    self.board[from_pos[0]][from_pos[1]] = None
                    
                    # Update has_moved flag
                    self.board[to_pos[0]][to_pos[1]].has_moved = True
                    
                    # Play appropriate sound
                    if is_capture:
                        self.capture_sound.play()
                    else:
                        self.move_sound.play()
                    
                    # Switch turns after a successful move
                    self.switch_turn()
                    
                    # Check for checkmate
                    self.update_game_state()
                    
                    # Reset animation and move states
                    self.pending_move = None
                    self.selected_piece = None
                    self.selected_square = None
                
                self.animating_piece = None
                self.animation_progress = 0
            return True
        return False

    def draw_animated_piece(self):
        """Draw the piece that is currently being animated"""
        if self.animating_piece and self.animation_piece_image:
            # Calculate current position using smooth easing
            progress = 1 - (1 - self.animation_progress) ** 3  # Cubic easing
            current_x = self.animation_start[0] + (self.animation_end[0] - self.animation_start[0]) * progress
            current_y = self.animation_start[1] + (self.animation_end[1] - self.animation_start[1]) * progress
            
            # Draw the piece at the current position
            x_offset = (SQUARE_SIZE - self.animation_piece_image.get_width()) // 2
            y_offset = (SQUARE_SIZE - self.animation_piece_image.get_height()) // 2
            self.screen.blit(
                self.animation_piece_image,
                (current_x + x_offset, current_y + y_offset)
            )

    def handle_click(self, pos):
        """Handle mouse click events"""
        # Handle promotion selection if pending
        if self.promotion_pending:
            if self.handle_promotion(pos):
                # Promotion was handled, switch turns
                self.switch_turn()
            return
            
        # Don't handle clicks during animation
        if self.animating_piece:
            return
            
        # Convert window coordinates to board coordinates
        board_x = pos[0] - BOARD_OFFSET_X
        board_y = pos[1] - BOARD_OFFSET_Y
        
        # Check if click is outside the board
        if not (0 <= board_x < BOARD_SIZE and 0 <= board_y < BOARD_SIZE):
            return
            
        col = board_x // SQUARE_SIZE
        row = board_y // SQUARE_SIZE
        square = self.get_square_notation(row, col)
        
        # If a piece is already selected
        if self.selected_piece:
            # Try to move the piece
            if (row, col) in self.valid_moves:
                old_row, old_col = self.selected_square
                
                # Check if the move is legal (doesn't put own king in check)
                if not self.simulate_move((old_row, old_col), (row, col)):
                    logger.warning(
                        f"Invalid move attempted to {square} - would put own king in check"
                    )
                    self.selected_piece = None
                    self.selected_square = None
                    self.valid_moves = []
                    return
                
                # Check if this move will result in a pawn promotion
                if self.needs_promotion(self.selected_piece, row):
                    # Store promotion information
                    self.promotion_pending = True
                    self.promotion_square = (row, col)
                    self.promotion_color = self.selected_piece.color
                    
                    # Store move data for after promotion
                    self.pending_move = {
                        'from': (old_row, old_col),
                        'to': (row, col),
                        'is_capture': self.board[row][col] is not None,
                        'captured_piece': self.board[row][col],
                        'source_square': self.get_square_notation(old_row, old_col),
                        'target_square': square
                    }
                    
                    # Move the pawn to the promotion square
                    self.board[row][col] = self.board[old_row][old_col]
                    self.board[old_row][old_col] = None
                    
                    # Clear selection but don't switch turns yet
                    self.selected_piece = None
                    self.selected_square = None
                    self.valid_moves = []
                    return
                
                # Start normal move animation
                piece_key = f"{self.selected_piece.color.lower()}_{self.selected_piece.position}"
                if piece_key in self.pieces_images:
                    self.animate_piece_movement(
                        (old_row, old_col),
                        (row, col),
                        self.pieces_images[piece_key]
                    )
                    
                    # Store move data to be applied after animation
                    self.pending_move = {
                        'from': (old_row, old_col),
                        'to': (row, col),
                        'is_capture': self.board[row][col] is not None,
                        'captured_piece': self.board[row][col],
                        'source_square': self.get_square_notation(old_row, old_col),
                        'target_square': square
                    }
                    
                    # Clear selection but keep the piece info for animation
                    self.valid_moves = []
            else:
                # Log invalid move attempt
                logger.warning(
                    f"Invalid move attempted to {square} "
                    f"for {self.selected_piece.color.capitalize()} "
                    f"{self.selected_piece.position.capitalize()}"
                )
                # Deselect if clicking on invalid square
                self.selected_piece = None
                self.selected_square = None
                self.valid_moves = []
        
        # If no piece is selected, try to select one
        else:
            piece = self.board[row][col]
            if piece and piece.color == self.current_turn:
                self.selected_piece = piece
                self.selected_square = (row, col)
                # Get valid moves for the selected piece
                self.valid_moves = piece.get_valid_moves(self.board, row, col)
                # Filter out moves that would put own king in check
                self.valid_moves = [
                    move for move in self.valid_moves 
                    if self.simulate_move((row, col), move)
                ]
                # Log piece selection and valid moves
                valid_squares = [self.get_square_notation(r, c) for r, c in self.valid_moves]
                logger.info(
                    f"{piece.color.capitalize()} {piece.position.capitalize()} "
                    f"selected at {square}. Valid moves: {', '.join(valid_squares)}"
                )
            elif piece:
                # Log attempt to move piece out of turn
                logger.warning(
                    f"Attempted to select {piece.color.capitalize()} piece at {square} "
                    f"during {self.current_turn.capitalize()}'s turn"
                )

    def draw_side_panel(self, side, x):
        """Draw side panel with captured pieces and information"""
        # Draw panel background with border
        panel_rect = pygame.Rect(x, 0, SIDE_PANEL_WIDTH, WINDOW_HEIGHT)
        pygame.draw.rect(self.screen, PANEL_BG, panel_rect)
        pygame.draw.line(self.screen, PANEL_BORDER, (x, 0), (x, WINDOW_HEIGHT), 2)
        
        # Draw player information with modern style
        color = "White" if side == "white" else "Black"
        is_current = self.current_turn == side
        text_color = ACTIVE_COLOR if is_current else TEXT_COLOR
        
        # Draw player header with background
        header_height = 50
        header_rect = pygame.Rect(x, 20, SIDE_PANEL_WIDTH, header_height)
        if is_current and not self.game_over:
            pygame.draw.rect(self.screen, LIGHT_GRAY, header_rect)
        
        text = self.font_medium.render(color, True, text_color)
        text_rect = text.get_rect(center=(x + SIDE_PANEL_WIDTH//2, 45))
        self.screen.blit(text, text_rect)
        
        # Draw timer
        self.draw_timer(side, x)
        
        # Draw captured pieces with labels
        y = 130  # Moved down to make room for timer
        piece_values = {"pawn": 1, "knight": 3, "bishop": 3, "rook": 5, "queen": 9, "king": 0}
        total_value = 0
        
        for piece in self.captured_pieces[side]:
            piece_key = f"{piece.color}_{piece.position}"
            if piece_key in self.pieces_images:
                # Calculate piece value
                total_value += piece_values.get(piece.position, 0)
                
                # Draw piece
                piece_img = pygame.transform.smoothscale(
                    self.pieces_images[piece_key],
                    (CAPTURED_PIECE_SIZE, CAPTURED_PIECE_SIZE)
                )
                self.screen.blit(piece_img, (x + 15, y))
                y += CAPTURED_PIECE_SIZE + 10
        
        # Draw material advantage
        if total_value > 0:
            advantage_text = f"+{total_value}"
            text = self.font_medium.render(advantage_text, True, TEXT_COLOR)
            self.screen.blit(text, (x + SIDE_PANEL_WIDTH - 50, 45))

    def draw_move_history(self):
        """Draw move history panel at the bottom"""
        y = WINDOW_HEIGHT - HISTORY_PANEL_HEIGHT
        
        # Draw panel background with border
        history_rect = pygame.Rect(0, y, WINDOW_WIDTH, HISTORY_PANEL_HEIGHT)
        pygame.draw.rect(self.screen, PANEL_BG, history_rect)
        pygame.draw.line(self.screen, PANEL_BORDER, (0, y), (WINDOW_WIDTH, y), 2)
        
        # Draw "Move History" title with modern style
        title_bg = pygame.Rect(0, y, WINDOW_WIDTH, 40)
        pygame.draw.rect(self.screen, LIGHT_GRAY, title_bg)
        
        text = self.font_medium.render("Move History", True, TEXT_COLOR)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, y + 20))
        self.screen.blit(text, text_rect)
        
        # Draw moves in three columns with alternating backgrounds
        x_start = BOARD_OFFSET_X - 150
        y_start = y + 50
        moves_per_column = 5
        column_width = 350
        
        for i, move in enumerate(self.move_history[-15:]):
            column = i // moves_per_column
            row = i % moves_per_column
            
            x = x_start + (column * column_width)
            y = y_start + (row * 24)
            
            # Draw alternating row backgrounds
            if row % 2 == 0:
                row_rect = pygame.Rect(x - 5, y - 2, column_width - 10, 24)
                pygame.draw.rect(self.screen, LIGHT_GRAY, row_rect)
            
            # Highlight the last move
            if i == len(self.move_history[-15:]) - 1:
                last_move_rect = pygame.Rect(x - 5, y - 2, column_width - 10, 24)
                pygame.draw.rect(self.screen, PRIMARY, last_move_rect)
                text = self.font_small.render(move, True, WHITE)
            else:
                text = self.font_small.render(move, True, TEXT_COLOR)
            
            self.screen.blit(text, (x, y))

    def format_time(self, seconds):
        """Convert seconds to MM:SS format"""
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

    def update_timer(self):
        """Update the timer for the current player"""
        if not self.game_over:
            current_tick = pygame.time.get_ticks()
            delta = (current_tick - self.last_tick) / 1000  # Convert to seconds
            self.time_left[self.current_turn] -= delta
            self.last_tick = current_tick

            # Check for time out
            if self.time_left[self.current_turn] <= 0:
                self.time_left[self.current_turn] = 0
                self.game_over = True
                winner = "Black" if self.current_turn == "white" else "White"
                logger.info(f"Game Over - {winner} wins by timeout")

    def draw_timer(self, side, x):
        """Draw timer for a player"""
        time_left = int(self.time_left[side])
        time_str = self.format_time(time_left)
        
        # Choose color based on remaining time
        if time_left <= TIME_CRITICAL:
            color = DANGER
        elif time_left <= TIME_WARNING:
            color = WARNING
        else:
            color = TEXT_COLOR
        
        # Draw time with background
        timer_y = 70
        timer_height = 40
        timer_rect = pygame.Rect(x + 10, timer_y, SIDE_PANEL_WIDTH - 20, timer_height)
        
        if self.current_turn == side:
            pygame.draw.rect(self.screen, LIGHT_GRAY, timer_rect)
        
        text = self.font_medium.render(time_str, True, color)
        text_rect = text.get_rect(center=(x + SIDE_PANEL_WIDTH//2, timer_y + timer_height//2))
        self.screen.blit(text, text_rect)

    def get_threatened_pieces(self, attacking_color):
        """Get all pieces that are under threat from the attacking color"""
        threatened_pieces = []
        defending_color = "black" if attacking_color == "white" else "white"
        
        # For each attacking piece
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == attacking_color:
                    # Get all possible moves for this piece
                    moves = piece.get_valid_moves(self.board, row, col)
                    
                    # Check if any of these moves can capture an opponent's piece
                    for move_row, move_col in moves:
                        target_piece = self.board[move_row][move_col]
                        if target_piece and target_piece.color == defending_color:
                            # Simulate the move to check if it's legal (doesn't put own king in check)
                            # Save current board state
                            temp_piece = self.board[move_row][move_col]
                            self.board[move_row][move_col] = self.board[row][col]
                            self.board[row][col] = None
                            
                            # Check if the move is legal (doesn't put own king in check)
                            if not self.is_king_in_check(attacking_color):
                                threatened_pieces.append((move_row, move_col))
                            
                            # Restore board state
                            self.board[row][col] = self.board[move_row][move_col]
                            self.board[move_row][move_col] = temp_piece
        
        return threatened_pieces

    def is_king_in_check(self, color):
        """Check if the king of the given color is in check"""
        # Find king position
        king_pos = None
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.position == "king" and piece.color == color:
                    king_pos = (row, col)
                    break
            if king_pos:
                break
        
        if not king_pos:
            return False
        
        # Check if any opponent piece can attack the king
        opponent_color = "black" if color == "white" else "white"
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == opponent_color:
                    moves = piece.get_valid_moves(self.board, row, col)
                    if king_pos in moves:
                        return True
        return False

    def simulate_move(self, from_pos, to_pos):
        """Simulate a move and return if it's legal"""
        # Save current board state
        temp_piece = self.board[to_pos[0]][to_pos[1]]
        # Make move
        self.board[to_pos[0]][to_pos[1]] = self.board[from_pos[0]][from_pos[1]]
        self.board[from_pos[0]][from_pos[1]] = None
        
        # Check if king is in check after move
        color = self.board[to_pos[0]][to_pos[1]].color
        is_legal = not self.is_king_in_check(color)
        
        # Restore board state
        self.board[from_pos[0]][from_pos[1]] = self.board[to_pos[0]][to_pos[1]]
        self.board[to_pos[0]][to_pos[1]] = temp_piece
        
        return is_legal

    def is_checkmate(self, color):
        """Check if the given color is in checkmate"""
        # If king is not in check, it's not checkmate
        if not self.is_king_in_check(color):
            return False
        
        # Try all possible moves for all pieces
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == color:
                    # Get all possible moves for this piece
                    moves = piece.get_valid_moves(self.board, row, col)
                    
                    # Try each move
                    for move_row, move_col in moves:
                        # If any move gets out of check, it's not checkmate
                        if self.simulate_move((row, col), (move_row, move_col)):
                            return False
        
        # If no legal moves found, it's checkmate
        return True

    def update_game_state(self):
        """Update game state including check and checkmate conditions"""
        if self.is_king_in_check(self.current_turn):
            logger.info(f"{self.current_turn.capitalize()} is in check!")
            
            if self.is_checkmate(self.current_turn):
                self.game_over = True
                winner = "Black" if self.current_turn == "white" else "White"
                logger.info(f"Checkmate! {winner} wins!")
                return True
        return False

    def draw_game_over_screen(self):
        """Draw game over screen with statistics"""
        if not self.game_over:
            return
            
        # Create semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Semi-transparent black
        self.screen.blit(overlay, (0, 0))
        
        # Create game over panel
        panel_width = 600
        panel_height = 400
        panel_x = (WINDOW_WIDTH - panel_width) // 2
        panel_y = (WINDOW_HEIGHT - panel_height) // 2
        
        # Draw panel background
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        pygame.draw.rect(self.screen, PANEL_BG, panel_rect)
        pygame.draw.rect(self.screen, PANEL_BORDER, panel_rect, 2)
        
        # Determine winner and reason
        if self.time_left["white"] <= 0:
            winner = "Black"
            reason = "by timeout"
        elif self.time_left["black"] <= 0:
            winner = "White"
            reason = "by timeout"
        elif self.is_checkmate(self.current_turn):
            winner = "Black" if self.current_turn == "white" else "White"
            reason = "by checkmate"
        else:
            winner = "Unknown"
            reason = ""
        
        # Draw game over text
        game_over_text = self.font_large.render("Game Over", True, TEXT_COLOR)
        text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, panel_y + 50))
        self.screen.blit(game_over_text, text_rect)
        
        # Draw winner text with reason
        winner_text = self.font_large.render(f"{winner} Wins {reason}!", True, WINNER_COLOR)
        text_rect = winner_text.get_rect(center=(WINDOW_WIDTH // 2, panel_y + 120))
        self.screen.blit(winner_text, text_rect)
        
        # Draw statistics
        y = panel_y + 180
        spacing = 40
        
        # Time statistics
        for color in ["White", "Black"]:
            time_str = self.format_time(int(self.time_left[color.lower()]))
            text = self.font_medium.render(f"{color}'s Time Left: {time_str}", True, TEXT_COLOR)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, y))
            self.screen.blit(text, text_rect)
            y += spacing
        
        # Captured pieces statistics
        for color in ["White", "Black"]:
            captured = len(self.captured_pieces[color.lower()])
            text = self.font_medium.render(f"{color}'s Captured Pieces: {captured}", True, TEXT_COLOR)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, y))
            self.screen.blit(text, text_rect)
            y += spacing
        
        # Total moves
        total_moves = len(self.move_history)
        text = self.font_medium.render(f"Total Moves: {total_moves}", True, TEXT_COLOR)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, y))
        self.screen.blit(text, text_rect)
        
        # Draw "Press any key to exit" text
        text = self.font_small.render("Press any key to exit", True, SECONDARY)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, panel_y + panel_height - 40))
        self.screen.blit(text, text_rect)

    def draw(self):
        """Draw the game state"""
        self.screen.fill(WHITE)
        
        # Draw side panels
        self.draw_side_panel("black", 0)
        self.draw_side_panel("white", WINDOW_WIDTH - SIDE_PANEL_WIDTH)
        
        # Draw board with shadow effect
        board_rect = pygame.Rect(
            BOARD_OFFSET_X - 2,
            BOARD_OFFSET_Y - 2,
            BOARD_SIZE + 4,
            BOARD_SIZE + 4
        )
        pygame.draw.rect(self.screen, PANEL_BORDER, board_rect)
        
        # Draw squares
        for row in range(8):
            for col in range(8):
                color = LIGHT_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE
                pygame.draw.rect(
                    self.screen,
                    color,
                    (BOARD_OFFSET_X + col * SQUARE_SIZE,
                     BOARD_OFFSET_Y + row * SQUARE_SIZE,
                     SQUARE_SIZE, SQUARE_SIZE)
                )
        
        # Draw board coordinates
        files = 'abcdefgh'
        ranks = '87654321'
        
        # Draw file labels (a-h)
        for i in range(8):
            # Bottom labels
            text = self.font_small.render(files[i], True, SECONDARY)
            text_rect = text.get_rect(center=(
                BOARD_OFFSET_X + i * SQUARE_SIZE + SQUARE_SIZE//2,
                BOARD_OFFSET_Y + BOARD_SIZE + 25
            ))
            self.screen.blit(text, text_rect)
            
            # Top labels
            text = self.font_small.render(files[i], True, SECONDARY)
            text_rect = text.get_rect(center=(
                BOARD_OFFSET_X + i * SQUARE_SIZE + SQUARE_SIZE//2,
                BOARD_OFFSET_Y - 25
            ))
            self.screen.blit(text, text_rect)
        
        # Draw rank labels (1-8)
        for i in range(8):
            # Left side labels
            text = self.font_small.render(ranks[i], True, SECONDARY)
            text_rect = text.get_rect(center=(
                BOARD_OFFSET_X - 25,
                BOARD_OFFSET_Y + i * SQUARE_SIZE + SQUARE_SIZE//2
            ))
            self.screen.blit(text, text_rect)
            
            # Right side labels
            text = self.font_small.render(ranks[i], True, SECONDARY)
            text_rect = text.get_rect(center=(
                BOARD_OFFSET_X + BOARD_SIZE + 25,
                BOARD_OFFSET_Y + i * SQUARE_SIZE + SQUARE_SIZE//2
            ))
            self.screen.blit(text, text_rect)
        
        # Draw threatened pieces
        opponent_color = "black" if self.current_turn == "white" else "white"
        threatened_pieces = self.get_threatened_pieces(opponent_color)
        
        for row, col in threatened_pieces:
            s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            pygame.draw.rect(s, THREATENED_SQUARE, s.get_rect())
            self.screen.blit(s, (
                BOARD_OFFSET_X + col * SQUARE_SIZE,
                BOARD_OFFSET_Y + row * SQUARE_SIZE
            ))
        
        # Highlight king in check
        if self.is_king_in_check(self.current_turn):
            # Find king position
            for row in range(8):
                for col in range(8):
                    piece = self.board[row][col]
                    if piece and piece.position == "king" and piece.color == self.current_turn:
                        s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                        pygame.draw.rect(s, KING_DANGER, s.get_rect())
                        self.screen.blit(s, (
                            BOARD_OFFSET_X + col * SQUARE_SIZE,
                            BOARD_OFFSET_Y + row * SQUARE_SIZE
                        ))
        
        # Highlight selected square with semi-transparent overlay
        if self.selected_square:
            row, col = self.selected_square
            s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            pygame.draw.rect(s, (*HIGHLIGHT, 180), s.get_rect())  # Semi-transparent
            self.screen.blit(s, (
                BOARD_OFFSET_X + col * SQUARE_SIZE,
                BOARD_OFFSET_Y + row * SQUARE_SIZE
            ))
        
        # Highlight valid moves with semi-transparent circles
        for row, col in self.valid_moves:
            center = (
                BOARD_OFFSET_X + col * SQUARE_SIZE + SQUARE_SIZE//2,
                BOARD_OFFSET_Y + row * SQUARE_SIZE + SQUARE_SIZE//2
            )
            # Draw outer circle with solid color
            pygame.draw.circle(self.screen, POSSIBLE_MOVE, center, 18)
            
            # Draw inner circle with semi-transparent surface
            s = pygame.Surface((36, 36), pygame.SRCALPHA)
            pygame.draw.circle(s, POSSIBLE_MOVE_ALPHA, (18, 18), 12)
            self.screen.blit(s, (center[0] - 18, center[1] - 18))
        
        # Draw pieces with shadows
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece:
                    piece_key = f"{piece.color.lower()}_{piece.position}"
                    if piece_key in self.pieces_images:
                        # Skip drawing if this piece is being animated
                        if self.animating_piece and (row, col) == self.selected_square:
                            continue
                        
                        piece_image = self.pieces_images[piece_key]
                        x_offset = (SQUARE_SIZE - piece_image.get_width()) // 2
                        y_offset = (SQUARE_SIZE - piece_image.get_height()) // 2
                        self.screen.blit(
                            piece_image,
                            (BOARD_OFFSET_X + col * SQUARE_SIZE + x_offset,
                             BOARD_OFFSET_Y + row * SQUARE_SIZE + y_offset)
                        )
        
        # Draw the animated piece on top
        self.draw_animated_piece()
        
        # Draw turn indicator with modern style
        turn_text = f"{self.current_turn.capitalize()}'s Turn"
        text_surface = self.font_large.render(turn_text, True, ACTIVE_COLOR)
        text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, 30))
        self.screen.blit(text_surface, text_rect)
        
        # Draw move history
        self.draw_move_history()
        
        # Draw game over screen if game is over
        if self.game_over:
            self.draw_game_over_screen()
        
        # Draw promotion panel on top if needed
        if self.promotion_pending:
            self.draw_promotion_panel()
        
        # Draw temporary message if exists
        if hasattr(self, 'message') and hasattr(self, 'message_start_time'):
            current_time = pygame.time.get_ticks()
            if current_time - self.message_start_time < self.message_duration:
                text = self.font_large.render(self.message, True, PRIMARY)
                text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 80))
                self.screen.blit(text, text_rect)
            else:
                delattr(self, 'message')
                delattr(self, 'message_start_time')

        pygame.display.flip()

    def run(self):
        """Main game loop"""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    logger.info("Game ended")
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # Return to menu when ESC is pressed
                        logger.info("Returning to main menu")
                        return "menu"
                    elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        # Ctrl+S to save game
                        if self.save_current_game():
                            self._show_message("Game saved successfully!", 2)
                        else:
                            self._show_message("Failed to save game!", 2)
                    elif event.key == pygame.K_l and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        # Ctrl+L to load game
                        saved_games = self.get_saved_games()
                        if saved_games:
                            # Load the most recent save
                            if self.load_saved_game(saved_games[0]['filename']):
                                self._show_message("Game loaded successfully!", 2)
                            else:
                                self._show_message("Failed to load game!", 2)
                        else:
                            self._show_message("No saved games found!", 2)
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                    if event.button == 1:  # Left click
                        self.handle_click(event.pos)
            
            # Update animation
            if self.update_animation():
                # Only update timer and game state when not animating
                pass
            else:
                # Update timer
                self.update_timer()
            
            # Draw game state
            self.draw()
            self.clock.tick(ANIMATION_FPS)
        
        pygame.quit()
        return "quit"

    def needs_promotion(self, piece, row):
        """Check if a pawn needs promotion"""
        return (piece.position == "pawn" and 
                ((piece.color == "white" and row == 0) or 
                 (piece.color == "black" and row == 7)))

    def handle_promotion(self, pos):
        """Handle click events during pawn promotion"""
        if not self.promotion_pending:
            return False
            
        # Calculate promotion panel position
        panel_x = (WINDOW_WIDTH - PROMOTION_PANEL_WIDTH) // 2
        panel_y = (WINDOW_HEIGHT - PROMOTION_PANEL_HEIGHT) // 2
        
        # Check if click is within panel
        if not (panel_x <= pos[0] <= panel_x + PROMOTION_PANEL_WIDTH and
                panel_y <= pos[1] <= panel_y + PROMOTION_PANEL_HEIGHT):
            return False
            
        # Calculate which piece was clicked
        piece_width = PROMOTION_PANEL_WIDTH // len(self.promotion_pieces)
        piece_index = (pos[0] - panel_x) // piece_width
        
        if 0 <= piece_index < len(self.promotion_pieces):
            # Get the chosen piece type
            chosen_piece = self.promotion_pieces[piece_index]
            row, col = self.promotion_square
            
            # Create the new piece
            piece_classes = {
                "queen": Queen,
                "rook": Rook,
                "bishop": Bishop,
                "knight": Knight
            }
            
            # Replace the pawn with the chosen piece
            self.board[row][col] = piece_classes[chosen_piece](self.promotion_color, chosen_piece)
            
            # Log the promotion
            logger.info(
                f"Pawn promoted to {chosen_piece.capitalize()} at "
                f"{self.get_square_notation(row, col)}"
            )
            
            # Clear promotion state
            self.promotion_pending = False
            self.promotion_square = None
            self.promotion_color = None
            
            return True
        
        return False

    def draw_promotion_panel(self):
        """Draw the pawn promotion selection panel"""
        if not self.promotion_pending:
            return
            
        # Create semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))
        
        # Draw promotion panel
        panel_x = (WINDOW_WIDTH - PROMOTION_PANEL_WIDTH) // 2
        panel_y = (WINDOW_HEIGHT - PROMOTION_PANEL_HEIGHT) // 2
        panel_rect = pygame.Rect(panel_x, panel_y, PROMOTION_PANEL_WIDTH, PROMOTION_PANEL_HEIGHT)
        
        # Draw panel background
        pygame.draw.rect(self.screen, PROMOTION_BG, panel_rect)
        pygame.draw.rect(self.screen, PROMOTION_BORDER, panel_rect, 2)
        
        # Draw promotion pieces
        piece_width = PROMOTION_PANEL_WIDTH // len(self.promotion_pieces)
        
        # Get mouse position for hover effect
        mouse_pos = pygame.mouse.get_pos()
        
        for i, piece_type in enumerate(self.promotion_pieces):
            piece_x = panel_x + (i * piece_width)
            piece_rect = pygame.Rect(piece_x, panel_y, piece_width, PROMOTION_PANEL_HEIGHT)
            
            # Draw hover effect
            if piece_rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, PROMOTION_HOVER, piece_rect)
            
            # Draw piece
            piece_key = f"{self.promotion_color}_{piece_type}"
            if piece_key in self.pieces_images:
                piece_image = pygame.transform.smoothscale(
                    self.pieces_images[piece_key],
                    (PROMOTION_PIECE_SIZE, PROMOTION_PIECE_SIZE)
                )
                
                # Center the piece in its section
                image_x = piece_x + (piece_width - PROMOTION_PIECE_SIZE) // 2
                image_y = panel_y + (PROMOTION_PANEL_HEIGHT - PROMOTION_PIECE_SIZE) // 2
                
                self.screen.blit(piece_image, (image_x, image_y))
                
                # Draw piece name
                text = self.font_small.render(piece_type.capitalize(), True, TEXT_COLOR)
                text_rect = text.get_rect(center=(piece_x + piece_width//2, panel_y + PROMOTION_PANEL_HEIGHT - 20))
                self.screen.blit(text, text_rect)

    def _show_message(self, message, duration):
        """Show a temporary message on screen"""
        self.message = message
        self.message_start_time = pygame.time.get_ticks()
        self.message_duration = duration * 1000  # Convert to milliseconds
