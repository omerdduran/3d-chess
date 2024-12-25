import pygame
from config.settings import *
from src.utils.logger import logger

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.buttons = []
        self.selected_button = None
        self.font_title = pygame.font.Font(None, MENU_TITLE_SIZE)
        self.font_button = pygame.font.Font(None, MENU_BUTTON_TEXT_SIZE)
        self.font_subtitle = pygame.font.Font(None, MENU_SUBTITLE_SIZE)
        
        # Load background image
        try:
            self.bg_image = pygame.image.load('assets/images/menu_bg.jpg')
            self.bg_image = pygame.transform.scale(self.bg_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
        except:
            self.bg_image = None
            logger.warning("Menu background image not found")
        
        # Create buttons
        button_y = WINDOW_HEIGHT // 2
        self.buttons = [
            {
                'text': MENU_BUTTON_NEW_GAME,
                'rect': pygame.Rect(
                    (WINDOW_WIDTH - MENU_BUTTON_WIDTH) // 2,
                    button_y,
                    MENU_BUTTON_WIDTH,
                    MENU_BUTTON_HEIGHT
                ),
                'color': MENU_BUTTON_BG,
                'action': 'new_game'
            },
            {
                'text': MENU_BUTTON_SAVE_GAME,
                'rect': pygame.Rect(
                    (WINDOW_WIDTH - MENU_BUTTON_WIDTH) // 2,
                    button_y + MENU_BUTTON_HEIGHT + MENU_BUTTON_SPACING,
                    MENU_BUTTON_WIDTH,
                    MENU_BUTTON_HEIGHT
                ),
                'color': MENU_BUTTON_SAVE,
                'action': 'save_game'
            },
            {
                'text': MENU_BUTTON_LOAD_GAME,
                'rect': pygame.Rect(
                    (WINDOW_WIDTH - MENU_BUTTON_WIDTH) // 2,
                    button_y + (MENU_BUTTON_HEIGHT + MENU_BUTTON_SPACING) * 2,
                    MENU_BUTTON_WIDTH,
                    MENU_BUTTON_HEIGHT
                ),
                'color': MENU_BUTTON_LOAD,
                'action': 'load_game'
            },
            {
                'text': MENU_BUTTON_QUIT,
                'rect': pygame.Rect(
                    (WINDOW_WIDTH - MENU_BUTTON_WIDTH) // 2,
                    button_y + (MENU_BUTTON_HEIGHT + MENU_BUTTON_SPACING) * 3,
                    MENU_BUTTON_WIDTH,
                    MENU_BUTTON_HEIGHT
                ),
                'color': MENU_BUTTON_BG,
                'action': 'quit'
            }
        ]

    def handle_event(self, event):
        """Handle menu events"""
        if event.type == pygame.MOUSEMOTION:
            # Check for button hover
            self.selected_button = None
            for button in self.buttons:
                if button['rect'].collidepoint(event.pos):
                    self.selected_button = button
                    break
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                for button in self.buttons:
                    if button['rect'].collidepoint(event.pos):
                        logger.info(f"Menu button clicked: {button['text']}")
                        return button['action']
        
        return None

    def draw(self):
        """Draw the menu"""
        # Draw background
        if self.bg_image:
            self.screen.blit(self.bg_image, (0, 0))
        else:
            self.screen.fill(MENU_BG)
        
        # Draw semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.fill(MENU_BG)
        overlay.set_alpha(MENU_PANEL_ALPHA)
        self.screen.blit(overlay, (0, 0))
        
        # Draw title
        title_text = self.font_title.render("Chess Game", True, MENU_TITLE_COLOR)
        title_rect = title_text.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3)
        )
        self.screen.blit(title_text, title_rect)
        
        # Draw subtitle
        subtitle_text = self.font_subtitle.render(
            "A Modern Chess Implementation",
            True,
            SECONDARY
        )
        subtitle_rect = subtitle_text.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3 + 60)
        )
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Draw buttons with shadow and hover effect
        for button in self.buttons:
            # Draw button shadow
            shadow_rect = button['rect'].copy()
            shadow_rect.y += 4
            pygame.draw.rect(
                self.screen,
                MENU_BUTTON_SHADOW,
                shadow_rect,
                border_radius=MENU_BUTTON_BORDER_RADIUS
            )
            
            # Draw button background
            color = button['color']
            if button == self.selected_button:
                # Make color more opaque on hover
                if isinstance(color, tuple) and len(color) == 4:
                    color = (*color[:3], 255)
                else:
                    color = MENU_BUTTON_HOVER
            
            pygame.draw.rect(
                self.screen,
                color,
                button['rect'],
                border_radius=MENU_BUTTON_BORDER_RADIUS
            )
            
            # Draw button text
            text = self.font_button.render(button['text'], True, TEXT_COLOR)
            text_rect = text.get_rect(center=button['rect'].center)
            self.screen.blit(text, text_rect)
        
        pygame.display.flip() 