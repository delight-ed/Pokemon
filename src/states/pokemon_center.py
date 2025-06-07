import pygame
from .base_state import BaseState
from ..constants import *

class PokemonCenter(BaseState):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.nurse_text = "Welcome to the Pokemon Center!"
        self.text_timer = 0
        self.healing = False
    
    def enter(self, **kwargs):
        self.nurse_text = "Welcome to the Pokemon Center!"
        self.text_timer = 0
        self.healing = False
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not self.healing:
                self.heal_pokemon()
            elif event.key == pygame.K_ESCAPE:
                self.game.change_state('overworld')
    
    def heal_pokemon(self):
        self.healing = True
        self.game.player.heal_all_pokemon()
        self.nurse_text = "Your Pokemon have been healed to full health!"
        self.text_timer = 3.0
    
    def update(self, dt):
        if self.text_timer > 0:
            self.text_timer -= dt
            if self.text_timer <= 0:
                self.healing = False
                self.nurse_text = "Come back anytime!"
    
    def draw(self, screen):
        screen.fill(WHITE)
        
        # Draw Pokemon Center interior
        pygame.draw.rect(screen, RED, (0, 0, SCREEN_WIDTH, 100))
        
        # Title
        title = self.font.render("POKEMON CENTER", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 30))
        
        # Nurse Joy (simplified)
        nurse_rect = pygame.Rect(SCREEN_WIDTH // 2 - 25, 150, 50, 100)
        pygame.draw.rect(screen, (255, 192, 203), nurse_rect)  # Pink
        
        # Nurse text
        nurse_text_surface = self.font.render(self.nurse_text, True, BLACK)
        text_rect = nurse_text_surface.get_rect(center=(SCREEN_WIDTH // 2, 300))
        screen.blit(nurse_text_surface, text_rect)
        
        # Instructions
        if not self.healing:
            instruction = self.small_font.render("SPACE: Heal Pokemon    ESC: Leave", True, BLACK)
            screen.blit(instruction, (SCREEN_WIDTH // 2 - instruction.get_width() // 2, 400))
        
        # Show Pokemon status
        y_pos = 450
        for i, pokemon in enumerate(self.game.player.pokemon_team):
            status_color = GREEN if not pokemon.is_fainted() else RED
            pokemon_status = self.small_font.render(
                f"{pokemon.species}: {pokemon.current_hp}/{pokemon.stats['hp']} HP", 
                True, status_color
            )
            screen.blit(pokemon_status, (50, y_pos + i * 25))