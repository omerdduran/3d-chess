from src.pieces.piece import Piece

class Pawn(Piece):
    def get_valid_moves(self, board, current_row, current_col):
        """Get all valid moves for the pawn"""
        moves = []
        direction = -1 if self.color == "white" else 1  # White moves up (-1), Black moves down (1)
        
        # Forward move
        new_row = current_row + direction
        if self.is_valid_position(new_row, current_col) and board[new_row][current_col] is None:
            moves.append((new_row, current_col))
            
            # First move - can move two squares
            if not self.has_moved:
                new_row = current_row + (direction * 2)
                if self.is_valid_position(new_row, current_col) and board[new_row][current_col] is None:
                    moves.append((new_row, current_col))
        
        # Capture moves (diagonal)
        for col_offset in [-1, 1]:
            new_row = current_row + direction
            new_col = current_col + col_offset
            
            if self.is_valid_position(new_row, new_col):
                target_square = board[new_row][new_col]
                if target_square is not None and target_square.color != self.color:
                    moves.append((new_row, new_col))
        
        return moves
