from src.pieces.piece import Piece

class Rook(Piece):
    def get_valid_moves(self, board, current_row, current_col):
        """Get all valid moves for the rook"""
        return self.get_straight_moves(board, current_row, current_col)
