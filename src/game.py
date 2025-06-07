import pygame
import sys
from .states.overworld import Overworld
from .states.battle import Battle
from .states.menu import Menu
from .states.pokemon_center import PokemonCenter
from .player import Player
from .constants import *

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pokemon Adventure")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Game states
        self.states = {
            'overworld': Overworld(self),
            'battle': Battle(self),
            'menu': Menu(self),
            'pokemon_center': PokemonCenter(self)
        }
        self.current_state = 'overworld'
        
        # Player
        self.player = Player()
        
    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.states[self.current_state].handle_event(event)
            
            self.states[self.current_state].update(dt)
            self.states[self.current_state].draw(self.screen)
            
            pygame.display.flip()
    
    def change_state(self, new_state, **kwargs):
        if new_state in self.states:
            self.current_state = new_state
            self.states[new_state].enter(**kwargs)