from src.pieces.piece import Piece

class Queen(Piece):
    def get_valid_moves(self, board, current_row, current_col):
        """Get all valid moves for the queen"""
        straight_moves = self.get_straight_moves(board, current_row, current_col)
        diagonal_moves = self.get_diagonal_moves(board, current_row, current_col)
        return straight_moves + diagonal_moves
