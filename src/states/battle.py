import pygame
import random
from .base_state import BaseState
from ..constants import *

class Battle(BaseState):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        self.player_pokemon = None
        self.enemy_pokemon = None
        self.is_gym = False
        
        self.battle_state = 'menu'  # menu, attack, switch, item, animation
        self.selected_move = 0
        self.battle_text = []
        self.text_timer = 0
        self.animation_timer = 0
        
    def enter(self, wild_pokemon=None, gym_pokemon=None, is_gym=False):
        self.player_pokemon = self.game.player.get_active_pokemon()
        self.enemy_pokemon = wild_pokemon or gym_pokemon
        self.is_gym = is_gym
        self.battle_state = 'menu'
        self.selected_move = 0
        self.battle_text = [f"A wild {self.enemy_pokemon.species} appeared!" if wild_pokemon else f"Gym Leader sent out {self.enemy_pokemon.species}!"]
        self.text_timer = 2.0
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.battle_state == 'menu':
                if event.key == pygame.K_1:
                    self.battle_state = 'attack'
                elif event.key == pygame.K_2:
                    self.run_away()
                elif event.key == pygame.K_3:
                    self.use_item()
            
            elif self.battle_state == 'attack':
                if event.key == pygame.K_1 and len(self.player_pokemon.moves) > 0:
                    self.use_move(0)
                elif event.key == pygame.K_2 and len(self.player_pokemon.moves) > 1:
                    self.use_move(1)
                elif event.key == pygame.K_3 and len(self.player_pokemon.moves) > 2:
                    self.use_move(2)
                elif event.key == pygame.K_4 and len(self.player_pokemon.moves) > 3:
                    self.use_move(3)
                elif event.key == pygame.K_ESCAPE:
                    self.battle_state = 'menu'
    
    def use_move(self, move_index):
        if move_index < len(self.player_pokemon.moves):
            move = self.player_pokemon.moves[move_index]
            
            if not self.player_pokemon.can_use_move(move):
                self.battle_text = [f"{move} has no PP left!"]
                self.text_timer = 1.5
                return
            
            # Player attacks
            result = self.player_pokemon.use_move(move, self.enemy_pokemon)
            self.process_attack_result(self.player_pokemon, self.enemy_pokemon, move, result)
            
            # Check if enemy fainted
            if self.enemy_pokemon.is_fainted():
                self.battle_text.append(f"Enemy {self.enemy_pokemon.species} fainted!")
                self.end_battle(victory=True)
                return
            
            # Enemy attacks back
            enemy_move = random.choice(self.enemy_pokemon.moves)
            enemy_result = self.enemy_pokemon.use_move(enemy_move, self.player_pokemon)
            self.process_attack_result(self.enemy_pokemon, self.player_pokemon, enemy_move, enemy_result)
            
            # Check if player Pokemon fainted
            if self.player_pokemon.is_fainted():
                self.battle_text.append(f"{self.player_pokemon.species} fainted!")
                if not self.game.player.has_usable_pokemon():
                    self.end_battle(victory=False)
                else:
                    # Switch to next Pokemon
                    self.switch_pokemon()
            
            self.battle_state = 'menu'
            self.text_timer = 3.0
    
    def process_attack_result(self, attacker, defender, move, result):
        if result:
            damage = result['damage']
            effectiveness = result['effectiveness']
            
            self.battle_text.append(f"{attacker.species} used {move}!")
            
            if damage > 0:
                if effectiveness > 1.0:
                    self.battle_text.append("It's super effective!")
                elif effectiveness < 1.0:
                    self.battle_text.append("It's not very effective...")
                
                self.battle_text.append(f"{defender.species} took {damage} damage!")
    
    def switch_pokemon(self):
        for pokemon in self.game.player.pokemon_team:
            if not pokemon.is_fainted():
                self.player_pokemon = pokemon
                self.battle_text.append(f"Go, {pokemon.species}!")
                break
    
    def run_away(self):
        if not self.is_gym:
            self.battle_text = ["You ran away safely!"]
            self.text_timer = 1.5
            self.end_battle(victory=False)
        else:
            self.battle_text = ["You can't run from a gym battle!"]
            self.text_timer = 1.5
    
    def use_item(self):
        if 'Potion' in self.game.player.items and self.game.player.items['Potion'] > 0:
            self.player_pokemon.heal(20)
            self.game.player.items['Potion'] -= 1
            self.battle_text = [f"Used Potion! {self.player_pokemon.species} recovered 20 HP!"]
            self.text_timer = 2.0
        else:
            self.battle_text = ["No items to use!"]
            self.text_timer = 1.5
    
    def end_battle(self, victory):
        if victory:
            exp_gained = self.enemy_pokemon.level * 50
            self.player_pokemon.gain_exp(exp_gained)
            self.battle_text.append(f"{self.player_pokemon.species} gained {exp_gained} EXP!")
            
            if self.is_gym:
                self.game.player.badges.append("Boulder Badge")
                self.battle_text.append("You won the Boulder Badge!")
        
        self.text_timer = 3.0
        pygame.time.set_timer(pygame.USEREVENT + 1, 3000)  # Return to overworld after 3 seconds
    
    def update(self, dt):
        if self.text_timer > 0:
            self.text_timer -= dt
        
        # Handle return to overworld
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT + 1:
                self.game.change_state('overworld')
                pygame.time.set_timer(pygame.USEREVENT + 1, 0)
    
    def draw(self, screen):
        screen.fill(LIGHT_GRAY)
        
        # Draw battle background
        pygame.draw.rect(screen, GREEN, (0, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
        
        # Draw Pokemon
        if self.player_pokemon:
            # Player Pokemon (back sprite simulation)
            player_rect = pygame.Rect(150, SCREEN_HEIGHT - 200, 100, 100)
            pygame.draw.rect(screen, YELLOW, player_rect)
            
            player_name = self.font.render(f"{self.player_pokemon.species} Lv.{self.player_pokemon.level}", True, BLACK)
            screen.blit(player_name, (150, SCREEN_HEIGHT - 250))
            
            # HP bar
            hp_ratio = self.player_pokemon.current_hp / self.player_pokemon.stats['hp']
            hp_bar_width = 200
            hp_bar = pygame.Rect(150, SCREEN_HEIGHT - 230, hp_bar_width, 20)
            pygame.draw.rect(screen, RED, hp_bar)
            pygame.draw.rect(screen, GREEN, (hp_bar.x, hp_bar.y, hp_bar_width * hp_ratio, hp_bar.height))
            
            hp_text = self.small_font.render(f"HP: {self.player_pokemon.current_hp}/{self.player_pokemon.stats['hp']}", True, BLACK)
            screen.blit(hp_text, (150, SCREEN_HEIGHT - 210))
        
        if self.enemy_pokemon:
            # Enemy Pokemon (front sprite simulation)
            enemy_rect = pygame.Rect(SCREEN_WIDTH - 250, 100, 100, 100)
            pygame.draw.rect(screen, RED, enemy_rect)
            
            enemy_name = self.font.render(f"{self.enemy_pokemon.species} Lv.{self.enemy_pokemon.level}", True, BLACK)
            screen.blit(enemy_name, (SCREEN_WIDTH - 250, 50))
            
            # HP bar
            hp_ratio = self.enemy_pokemon.current_hp / self.enemy_pokemon.stats['hp']
            hp_bar_width = 200
            hp_bar = pygame.Rect(SCREEN_WIDTH - 250, 70, hp_bar_width, 20)
            pygame.draw.rect(screen, RED, hp_bar)
            pygame.draw.rect(screen, GREEN, (hp_bar.x, hp_bar.y, hp_bar_width * hp_ratio, hp_bar.height))
        
        # Draw battle menu
        if self.battle_state == 'menu':
            self.draw_battle_menu(screen)
        elif self.battle_state == 'attack':
            self.draw_move_menu(screen)
        
        # Draw battle text
        self.draw_battle_text(screen)
    
    def draw_battle_menu(self, screen):
        menu_rect = pygame.Rect(50, SCREEN_HEIGHT - 150, SCREEN_WIDTH - 100, 100)
        pygame.draw.rect(screen, WHITE, menu_rect)
        pygame.draw.rect(screen, BLACK, menu_rect, 3)
        
        options = ["1. Attack", "2. Run", "3. Item"]
        for i, option in enumerate(options):
            option_text = self.font.render(option, True, BLACK)
            screen.blit(option_text, (70, SCREEN_HEIGHT - 130 + i * 30))
    
    def draw_move_menu(self, screen):
        menu_rect = pygame.Rect(50, SCREEN_HEIGHT - 150, SCREEN_WIDTH - 100, 100)
        pygame.draw.rect(screen, WHITE, menu_rect)
        pygame.draw.rect(screen, BLACK, menu_rect, 3)
        
        for i, move in enumerate(self.player_pokemon.moves):
            if i < 4:  # Max 4 moves
                pp = self.player_pokemon.move_pp.get(move, 0)
                move_text = f"{i+1}. {move} (PP: {pp})"
                color = BLACK if pp > 0 else GRAY
                option_text = self.font.render(move_text, True, color)
                screen.blit(option_text, (70, SCREEN_HEIGHT - 130 + i * 20))
        
        back_text = self.small_font.render("ESC: Back", True, BLACK)
        screen.blit(back_text, (70, SCREEN_HEIGHT - 60))
    
    def draw_battle_text(self, screen):
        text_rect = pygame.Rect(50, SCREEN_HEIGHT - 300, SCREEN_WIDTH - 100, 100)
        pygame.draw.rect(screen, WHITE, text_rect)
        pygame.draw.rect(screen, BLACK, text_rect, 3)
        
        for i, text in enumerate(self.battle_text[-3:]):  # Show last 3 messages
            text_surface = self.small_font.render(text, True, BLACK)
            screen.blit(text_surface, (70, SCREEN_HEIGHT - 280 + i * 25))