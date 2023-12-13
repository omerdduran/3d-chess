import os
from config.settings import *
import pygame
from src.pieces.piece import Piece
from src.pieces.rook import Rook
from src.pieces.knight import Knight
from src.pieces.bishop import Bishop
from src.pieces.queen import Queen
from src.pieces.king import King
from src.pieces.pawn import Pawn


def load_pieces():
    """Loads piece images with high quality"""
    pieces = {}
    piece_types = ["bishop", "king", "knight", "pawn", "queen", "rook"]
    colors = ["BLACK", "WHITE"]
    
    # Calculate piece size based on square size and scale factor
    piece_size = int(SQUARE_SIZE * PIECE_SCALE)

    for color in colors:
        for piece_type in piece_types:
            filename = f"{color}-{piece_type}.svg"
            path = os.path.join("assets", "images", "pieces", filename)

            try:
                # Load SVG at a larger size first for better quality
                temp_size = piece_size * 2  # Load at 2x size initially
                image = pygame.image.load(path)
                image = pygame.transform.smoothscale(image, (temp_size, temp_size))
                # Then scale down to desired size for better anti-aliasing
                image = pygame.transform.smoothscale(image, (piece_size, piece_size))
                pieces[f"{color.lower()}_{piece_type}"] = image
            except pygame.error as e:
                print(f"Error: Could not load {filename} - {e}")

    return pieces


def create_board():
    """Creates a chess board in starting position"""
    board = [[None for _ in range(8)] for _ in range(8)]
    
    # Map piece names to their classes
    piece_classes = {
        "rook": Rook,
        "knight": Knight,
        "bishop": Bishop,
        "queen": Queen,
        "king": King,
        "pawn": Pawn
    }

    # Initial piece arrangement
    piece_order = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"]

    # Place black pieces
    for col in range(8):
        # Create the specific piece type for back rank
        piece_class = piece_classes[piece_order[col]]
        board[0][col] = piece_class("black", piece_order[col])
        # Create pawns
        board[1][col] = Pawn("black", "pawn")

    # Place white pieces
    for col in range(8):
        # Create the specific piece type for back rank
        piece_class = piece_classes[piece_order[col]]
        board[7][col] = piece_class("white", piece_order[col])
        # Create pawns
        board[6][col] = Pawn("white", "pawn")

    return board


def draw_board(screen):
    """Satranç tahtasını çizer"""
    for row in range(8):
        for col in range(8):
            color = LIGHT_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE
            pygame.draw.rect(
                screen,
                color,
                (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
            )


def draw_pieces(screen, board, pieces_images):
    """Draws the pieces centered in their squares"""
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece:
                piece_key = f"{piece.color.lower()}_{piece.position}"
                if piece_key in pieces_images:
                    piece_image = pieces_images[piece_key]
                    # Calculate centering offsets
                    x_offset = (SQUARE_SIZE - piece_image.get_width()) // 2
                    y_offset = (SQUARE_SIZE - piece_image.get_height()) // 2
                    # Draw piece centered in square
                    screen.blit(
                        piece_image,
                        (col * SQUARE_SIZE + x_offset, row * SQUARE_SIZE + y_offset)
                    )

