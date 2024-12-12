class Piece:
    def __init__(self, color, piece_type):
        self.color = color  # 'white' or 'black'
        self.position = piece_type  # The type of piece (e.g., "rook", "pawn")
        self.has_moved = False

    def is_valid_position(self, row, col):
        """Check if the position is within the board boundaries"""
        return 0 <= row < 8 and 0 <= col < 8

    def is_empty_or_enemy(self, board, row, col):
        """Check if the target square is empty or contains an enemy piece"""
        if not self.is_valid_position(row, col):
            return False
        if board[row][col] is None:
            return True
        return board[row][col].color != self.color

    def get_straight_moves(self, board, current_row, current_col):
        """Get all possible straight moves (horizontal and vertical)"""
        moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # right, left, down, up
        
        for dir_row, dir_col in directions:
            row, col = current_row + dir_row, current_col + dir_col
            while self.is_valid_position(row, col):
                if board[row][col] is None:
                    moves.append((row, col))
                elif board[row][col].color != self.color:
                    moves.append((row, col))
                    break
                else:
                    break
                row += dir_row
                col += dir_col
        return moves

    def get_diagonal_moves(self, board, current_row, current_col):
        """Get all possible diagonal moves"""
        moves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for dir_row, dir_col in directions:
            row, col = current_row + dir_row, current_col + dir_col
            while self.is_valid_position(row, col):
                if board[row][col] is None:
                    moves.append((row, col))
                elif board[row][col].color != self.color:
                    moves.append((row, col))
                    break
                else:
                    break
                row += dir_row
                col += dir_col
        return moves

    def get_valid_moves(self, board, current_row, current_col):
        """Returns list of valid moves for the piece - to be implemented by subclasses"""
        raise NotImplementedError
