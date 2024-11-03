import pygame
import logging
from config.settings import *

logging.basicConfig(
    filename='chess.log',  # Logların kaydedileceği dosya adı
    level=logging.DEBUG,       # Log seviyesini DEBUG olarak ayarlıyoruz
    format='%(asctime)s - %(levelname)s - %(message)s'  # Log formatı
)
logging.info('Game Script Started')

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(GAME_NAME)

programIcon = pygame.image.load('assets/images/icon.webp')
pygame.display.set_icon(programIcon)

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    clock.tick(FPS_LIMIT)  

pygame.quit()