import pygame
from src.game.game import Game
from src.menu.menu import Menu
from config.settings import *
from src.utils.logger import logger

def main():
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(GAME_NAME)
    
    # Create menu and game instances
    menu = Menu(screen)
    game = None
    current_screen = "menu"
    
    # Main game loop
    running = True
    while running:
        if current_screen == "menu":
            # Handle menu events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    action = menu.handle_event(event)
                    if action == "new_game":
                        game = Game()
                        current_screen = "game"
                        logger.info("Starting new game")
                    elif action == "save_game":
                        if game:
                            if game.save_current_game():
                                logger.info("Game saved successfully")
                            else:
                                logger.error("Failed to save game")
                        else:
                            logger.warning("No active game to save")
                    elif action == "load_game":
                        saved_games = None
                        if game:
                            saved_games = game.get_saved_games()
                        else:
                            game = Game()
                            saved_games = game.get_saved_games()
                        
                        if saved_games:
                            if game.load_saved_game(saved_games[0]['filename']):
                                current_screen = "game"
                                logger.info("Game loaded successfully")
                            else:
                                logger.error("Failed to load game")
                        else:
                            logger.warning("No saved games found")
                    elif action == "quit":
                        running = False
            
            # Draw menu
            menu.draw()
            
        elif current_screen == "game":
            # Run game and handle return value
            result = game.run()
            if result == "menu":
                current_screen = "menu"
                logger.info("Returned to main menu")
            elif result == "quit":
                running = False
    
    pygame.quit()

if __name__ == "__main__":
    main()