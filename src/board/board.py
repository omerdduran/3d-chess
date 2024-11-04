import os
from config.settings import *
import pygame


def load_pieces():
    """Taş görsellerini yükler"""
    pieces = {}
    piece_types = ['bishop', 'king', 'knight', 'pawn', 'queen', 'rook']
    colors = ['BLACK', 'WHITE']

    for color in colors:
        for piece_type in piece_types:
            # Dosya adını oluştur (örn: "BLACK-bishop.svg")
            filename = f"{color}-{piece_type}.svg"
            path = os.path.join('assets', 'images', 'pieces', filename)

            try:
                # SVG dosyasını yükle ve boyutlandır
                image = pygame.image.load(path)
                image = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))
                # Sözlükte sakla (örn: pieces['black_bishop'])
                pieces[f"{color.lower()}_{piece_type}"] = image
            except pygame.error as e:
                print(f"Hata: {filename} yüklenemedi - {e}")

    return pieces


def create_board():
    """Başlangıç pozisyonunda bir satranç tahtası oluşturur"""
    board = [[None for _ in range(8)] for _ in range(8)]

    # Taşların başlangıç dizilimi
    piece_order = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']

    # Siyah taşları yerleştir
    for col in range(8):
        board[0][col] = ('black', piece_order[col])
        board[1][col] = ('black', 'pawn')

    # Beyaz taşları yerleştir
    for col in range(8):
        board[7][col] = ('white', piece_order[col])
        board[6][col] = ('white', 'pawn')

    return board


def draw_board(screen):
    """Satranç tahtasını çizer"""
    for row in range(8):
        for col in range(8):
            color = LIGHT_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE
            pygame.draw.rect(
                screen,
                color,
                (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            )


def draw_pieces(screen, board, pieces_images):
    """Taşları çizer"""
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece:
                color, piece_type = piece
                # Görsel anahtarını oluştur (örn: "black_bishop")
                piece_key = f"{color}_{piece_type}"
                if piece_key in pieces_images:
                    screen.blit(
                        pieces_images[piece_key],
                        (col * SQUARE_SIZE, row * SQUARE_SIZE)
                    )