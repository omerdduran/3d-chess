import pygame
import logging
from config.settings import *
from src.board.board import draw_board, draw_pieces, create_board, load_pieces

logging.basicConfig(
    filename='chess.log',  
    level=logging.DEBUG,    
    format='%(asctime)s - %(levelname)s - %(message)s' 
)
logging.info('Game Script Started')

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(GAME_NAME)

programIcon = pygame.image.load('assets/images/icon.webp')
pygame.display.set_icon(programIcon)

clock = pygame.time.Clock()
running = True

pieces_images = load_pieces()
board = create_board()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    clock.tick(FPS_LIMIT)
    draw_board(screen)
    draw_pieces(screen, board, pieces_images)
    pygame.display.flip()
    

pygame.quit()