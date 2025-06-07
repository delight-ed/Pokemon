import pygame
from .base_state import BaseState
from ..constants import *

class Menu(BaseState):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.selected_option = 0
        self.menu_options = ['Pokemon', 'Items', 'Save', 'Back']
        self.submenu = None
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.submenu is None:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    self.select_option()
                elif event.key == pygame.K_ESCAPE:
                    self.game.change_state('overworld')
            else:
                if event.key == pygame.K_ESCAPE:
                    self.submenu = None
    
    def select_option(self):
        option = self.menu_options[self.selected_option]
        if option == 'Pokemon':
            self.submenu = 'pokemon'
        elif option == 'Items':
            self.submenu = 'items'
        elif option == 'Save':
            self.save_game()
        elif option == 'Back':
            self.game.change_state('overworld')
    
    def save_game(self):
        # Simplified save system
        print("Game saved!")  # In a real game, this would save to a file
    
    def update(self, dt):
        pass
    
    def draw(self, screen):
        screen.fill(DARK_GRAY)
        
        if self.submenu is None:
            self.draw_main_menu(screen)
        elif self.submenu == 'pokemon':
            self.draw_pokemon_menu(screen)
        elif self.submenu == 'items':
            self.draw_items_menu(screen)
    
    def draw_main_menu(self, screen):
        title = self.font.render("MENU", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
        
        for i, option in enumerate(self.menu_options):
            color = YELLOW if i == self.selected_option else WHITE
            option_text = self.font.render(option, True, color)
            screen.blit(option_text, (SCREEN_WIDTH // 2 - option_text.get_width() // 2, 200 + i * 50))
    
    def draw_pokemon_menu(self, screen):
        title = self.font.render("POKEMON", True, WHITE)
        screen.blit(title, (50, 50))
        
        for i, pokemon in enumerate(self.game.player.pokemon_team):
            y_pos = 120 + i * 80
            
            # Pokemon info
            name_text = self.font.render(f"{pokemon.species} Lv.{pokemon.level}", True, WHITE)
            screen.blit(name_text, (50, y_pos))
            
            hp_text = self.small_font.render(f"HP: {pokemon.current_hp}/{pokemon.stats['hp']}", True, WHITE)
            screen.blit(hp_text, (50, y_pos + 25))
            
            status = "Fainted" if pokemon.is_fainted() else "OK"
            status_color = RED if pokemon.is_fainted() else GREEN
            status_text = self.small_font.render(f"Status: {status}", True, status_color)
            screen.blit(status_text, (50, y_pos + 45))
        
        back_text = self.small_font.render("ESC: Back", True, WHITE)
        screen.blit(back_text, (50, SCREEN_HEIGHT - 50))
    
    def draw_items_menu(self, screen):
        title = self.font.render("ITEMS", True, WHITE)
        screen.blit(title, (50, 50))
        
        y_pos = 120
        for item, quantity in self.game.player.items.items():
            if quantity > 0:
                item_text = self.font.render(f"{item}: {quantity}", True, WHITE)
                screen.blit(item_text, (50, y_pos))
                y_pos += 40
        
        back_text = self.small_font.render("ESC: Back", True, WHITE)
        screen.blit(back_text, (50, SCREEN_HEIGHT - 50))