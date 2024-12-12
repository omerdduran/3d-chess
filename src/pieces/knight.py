from src.pieces.piece import Piece

class Knight(Piece):
    def get_valid_moves(self, board, current_row, current_col):
        """Get all valid moves for the knight"""
        moves = []
        # All possible L-shaped moves
        directions = [
            (-2, -1), (-2, 1),  # Up 2, left/right 1
            (2, -1), (2, 1),    # Down 2, left/right 1
            (-1, -2), (1, -2),  # Left 2, up/down 1
            (-1, 2), (1, 2)     # Right 2, up/down 1
        ]
        
        for dir_row, dir_col in directions:
            new_row = current_row + dir_row
            new_col = current_col + dir_col
            
            if self.is_valid_position(new_row, new_col) and self.is_empty_or_enemy(board, new_row, new_col):
                moves.append((new_row, new_col))
                
        return moves