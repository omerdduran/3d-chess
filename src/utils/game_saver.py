import json
import os
from datetime import datetime
from src.utils.logger import logger

class GameSaver:
    def __init__(self, save_dir="saved_games"):
        """Initialize the GameSaver with a directory for saved games"""
        self.save_dir = save_dir
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

    def save_game(self, game_state):
        """Save the current game state to a JSON file"""
        try:
            # Create a timestamp for the filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"chess_game_{timestamp}.json"
            filepath = os.path.join(self.save_dir, filename)

            # Convert game state to serializable format
            save_data = {
                "board_state": self._serialize_board(game_state.board),
                "current_turn": game_state.current_turn,
                "time_left": game_state.time_left,
                "move_history": game_state.move_history,
                "captured_pieces": self._serialize_captured_pieces(game_state.captured_pieces),
                "move_count": game_state.move_count,
                "game_over": game_state.game_over
            }

            # Save to file
            with open(filepath, 'w') as f:
                json.dump(save_data, f, indent=4)

            logger.info(f"Game saved successfully to {filename}")
            return filename

        except Exception as e:
            logger.error(f"Error saving game: {str(e)}")
            return None

    def load_game(self, filename):
        """Load a game state from a JSON file"""
        try:
            filepath = os.path.join(self.save_dir, filename)
            with open(filepath, 'r') as f:
                save_data = json.load(f)

            logger.info(f"Game loaded successfully from {filename}")
            return save_data

        except Exception as e:
            logger.error(f"Error loading game: {str(e)}")
            return None

    def list_saved_games(self):
        """List all saved game files"""
        try:
            saved_games = []
            for filename in os.listdir(self.save_dir):
                if filename.endswith('.json'):
                    filepath = os.path.join(self.save_dir, filename)
                    timestamp = os.path.getmtime(filepath)
                    date = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
                    saved_games.append({
                        'filename': filename,
                        'date': date
                    })
            return sorted(saved_games, key=lambda x: x['date'], reverse=True)
        except Exception as e:
            logger.error(f"Error listing saved games: {str(e)}")
            return []

    def delete_save(self, filename):
        """Delete a saved game file"""
        try:
            filepath = os.path.join(self.save_dir, filename)
            if os.path.exists(filepath):
                os.remove(filepath)
                logger.info(f"Deleted save file: {filename}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting save file: {str(e)}")
            return False

    def _serialize_board(self, board):
        """Convert the board state to a serializable format"""
        board_state = []
        for row in range(8):
            board_row = []
            for col in range(8):
                piece = board[row][col]
                if piece:
                    board_row.append({
                        'position': piece.position,
                        'color': piece.color,
                        'has_moved': getattr(piece, 'has_moved', False)
                    })
                else:
                    board_row.append("")
            board_state.append(board_row)
        return board_state

    def _serialize_captured_pieces(self, captured_pieces):
        """Convert captured pieces to a serializable format"""
        serialized = {"white": [], "black": []}
        for color in ["white", "black"]:
            for piece in captured_pieces[color]:
                serialized[color].append({
                    'position': piece.position,
                    'color': piece.color
                })
        return serialized 