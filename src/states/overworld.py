import pygame
import random
from .base_state import BaseState
from ..pokemon import Pokemon
from ..constants import *

class Overworld(BaseState):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Map data (simplified)
        self.map_width = 32
        self.map_height = 24
        self.tiles = self.generate_map()
        
        # NPCs and buildings
        self.pokemon_center = pygame.Rect(10 * TILE_SIZE, 5 * TILE_SIZE, TILE_SIZE * 2, TILE_SIZE * 2)
        self.gym = pygame.Rect(20 * TILE_SIZE, 8 * TILE_SIZE, TILE_SIZE * 2, TILE_SIZE * 2)
        
        # Wild Pokemon areas
        self.grass_tiles = []
        for y in range(self.map_height):
            for x in range(self.map_width):
                if self.tiles[y][x] == 'grass':
                    self.grass_tiles.append((x, y))
    
    def generate_map(self):
        # Simple map generation
        tiles = []
        for y in range(self.map_height):
            row = []
            for x in range(self.map_width):
                if x == 0 or x == self.map_width - 1 or y == 0 or y == self.map_height - 1:
                    row.append('tree')
                elif random.random() < 0.3:
                    row.append('grass')
                elif random.random() < 0.1:
                    row.append('tree')
                else:
                    row.append('ground')
            tiles.append(row)
        return tiles
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Check for interactions
                player_tile_x = int(self.game.player.x // TILE_SIZE)
                player_tile_y = int(self.game.player.y // TILE_SIZE)
                
                # Check Pokemon Center
                if self.pokemon_center.collidepoint(self.game.player.x, self.game.player.y):
                    self.game.change_state('pokemon_center')
                
                # Check Gym
                elif self.gym.collidepoint(self.game.player.x, self.game.player.y):
                    self.start_gym_battle()
            
            elif event.key == pygame.K_m:
                self.game.change_state('menu')
    
    def update(self, dt):
        keys = pygame.key.get_pressed()
        old_x, old_y = self.game.player.x, self.game.player.y
        
        # Player movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.game.player.x -= self.game.player.speed * dt
            self.game.player.direction = 'left'
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.game.player.x += self.game.player.speed * dt
            self.game.player.direction = 'right'
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            self.game.player.y -= self.game.player.speed * dt
            self.game.player.direction = 'up'
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.game.player.y += self.game.player.speed * dt
            self.game.player.direction = 'down'
        
        # Collision detection
        player_tile_x = int(self.game.player.x // TILE_SIZE)
        player_tile_y = int(self.game.player.y // TILE_SIZE)
        
        if (player_tile_x < 0 or player_tile_x >= self.map_width or 
            player_tile_y < 0 or player_tile_y >= self.map_height or
            self.tiles[player_tile_y][player_tile_x] == 'tree'):
            self.game.player.x, self.game.player.y = old_x, old_y
        
        # Random wild Pokemon encounters in grass
        if self.tiles[player_tile_y][player_tile_x] == 'grass' and random.random() < 0.001:
            self.start_wild_battle()
    
    def start_wild_battle(self):
        wild_species = random.choice(['Rattata', 'Zubat', 'Geodude'])
        wild_level = random.randint(3, 8)
        wild_pokemon = Pokemon(wild_species, wild_level)
        self.game.change_state('battle', wild_pokemon=wild_pokemon)
    
    def start_gym_battle(self):
        gym_pokemon = Pokemon('Geodude', level=15)
        self.game.change_state('battle', gym_pokemon=gym_pokemon, is_gym=True)
    
    def draw(self, screen):
        screen.fill(GREEN)
        
        # Draw map
        for y in range(self.map_height):
            for x in range(self.map_width):
                tile_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                
                if self.tiles[y][x] == 'ground':
                    pygame.draw.rect(screen, LIGHT_GRAY, tile_rect)
                elif self.tiles[y][x] == 'grass':
                    pygame.draw.rect(screen, GREEN, tile_rect)
                elif self.tiles[y][x] == 'tree':
                    pygame.draw.rect(screen, DARK_GRAY, tile_rect)
        
        # Draw buildings
        pygame.draw.rect(screen, RED, self.pokemon_center)
        pygame.draw.rect(screen, BLUE, self.gym)
        
        # Draw building labels
        pc_text = self.small_font.render("Pokemon Center", True, WHITE)
        screen.blit(pc_text, (self.pokemon_center.x, self.pokemon_center.y - 25))
        
        gym_text = self.small_font.render("Gym", True, WHITE)
        screen.blit(gym_text, (self.gym.x, self.gym.y - 25))
        
        # Draw player
        player_rect = pygame.Rect(self.game.player.x - 8, self.game.player.y - 8, 16, 16)
        pygame.draw.rect(screen, YELLOW, player_rect)
        
        # Draw UI
        self.draw_ui(screen)
    
    def draw_ui(self, screen):
        # Player info
        info_text = self.small_font.render(f"Player: {self.game.player.name}", True, BLACK)
        screen.blit(info_text, (10, 10))
        
        money_text = self.small_font.render(f"Money: ${self.game.player.money}", True, BLACK)
        screen.blit(money_text, (10, 35))
        
        # Active Pokemon info
        active_pokemon = self.game.player.get_active_pokemon()
        if active_pokemon:
            pokemon_text = self.small_font.render(f"{active_pokemon.species} Lv.{active_pokemon.level}", True, BLACK)
            screen.blit(pokemon_text, (10, 60))
            
            hp_text = self.small_font.render(f"HP: {active_pokemon.current_hp}/{active_pokemon.stats['hp']}", True, BLACK)
            screen.blit(hp_text, (10, 85))
        
        # Controls
        controls = [
            "WASD/Arrow Keys: Move",
            "SPACE: Interact",
            "M: Menu"
        ]
        
        for i, control in enumerate(controls):
            control_text = self.small_font.render(control, True, BLACK)
            screen.blit(control_text, (SCREEN_WIDTH - 200, 10 + i * 25))