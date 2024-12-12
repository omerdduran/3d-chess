from src.pieces.piece import Piece

class King(Piece):
    def get_valid_moves(self, board, current_row, current_col):
        """Get all valid moves for the king"""
        moves = []
        # All possible directions (horizontal, vertical, and diagonal)
        directions = [
            (-1, -1), (-1, 0), (-1, 1),  # Top-left, top, top-right
            (0, -1),           (0, 1),    # Left, right
            (1, -1),  (1, 0),  (1, 1)     # Bottom-left, bottom, bottom-right
        ]
        
        for dir_row, dir_col in directions:
            new_row = current_row + dir_row
            new_col = current_col + dir_col
            
            if self.is_valid_position(new_row, new_col) and self.is_empty_or_enemy(board, new_row, new_col):
                moves.append((new_row, new_col))
                
        return moves
