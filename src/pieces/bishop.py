from src.pieces.piece import Piece

class Bishop(Piece):
    def get_valid_moves(self, board, current_row, current_col):
        """Get all valid moves for the bishop"""
        return self.get_diagonal_moves(board, current_row, current_col)
