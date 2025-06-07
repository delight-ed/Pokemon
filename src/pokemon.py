import random
from .constants import TYPE_EFFECTIVENESS, MOVES_DB

class Pokemon:
    def __init__(self, species, level=5):
        self.species = species
        self.level = level
        self.exp = 0
        self.exp_to_next = self.calculate_exp_to_next()
        
        # Get species data
        species_data = POKEMON_DATA.get(species, POKEMON_DATA['Pikachu'])
        self.types = species_data['types']
        self.base_stats = species_data['base_stats']
        self.sprite_url = species_data['sprite']
        self.moves = species_data['moves'][:4]  # Max 4 moves
        
        # Calculate actual stats
        self.stats = self.calculate_stats()
        self.current_hp = self.stats['hp']
        self.status = None  # poison, burn, sleep, etc.
        
        # Move PP
        self.move_pp = {}
        for move in self.moves:
            if move in MOVES_DB:
                self.move_pp[move] = MOVES_DB[move]['pp']
    
    def calculate_stats(self):
        stats = {}
        for stat, base in self.base_stats.items():
            if stat == 'hp':
                stats[stat] = int(((2 * base + 31) * self.level) / 100) + self.level + 10
            else:
                stats[stat] = int(((2 * base + 31) * self.level) / 100) + 5
        return stats
    
    def calculate_exp_to_next(self):
        return int(1.2 * (self.level ** 3))
    
    def gain_exp(self, amount):
        self.exp += amount
        while self.exp >= self.exp_to_next:
            self.level_up()
    
    def level_up(self):
        self.exp -= self.exp_to_next
        self.level += 1
        old_stats = self.stats.copy()
        self.stats = self.calculate_stats()
        self.current_hp += (self.stats['hp'] - old_stats['hp'])
        self.exp_to_next = self.calculate_exp_to_next()
        return True
    
    def take_damage(self, damage):
        self.current_hp = max(0, self.current_hp - damage)
        return self.current_hp <= 0
    
    def heal(self, amount=None):
        if amount is None:
            self.current_hp = self.stats['hp']
        else:
            self.current_hp = min(self.stats['hp'], self.current_hp + amount)
    
    def is_fainted(self):
        return self.current_hp <= 0
    
    def can_use_move(self, move):
        return move in self.move_pp and self.move_pp[move] > 0
    
    def use_move(self, move, target):
        if not self.can_use_move(move):
            return None
        
        self.move_pp[move] -= 1
        move_data = MOVES_DB[move]
        
        # Calculate damage
        if move_data['power'] > 0:
            # Damage calculation
            attack_stat = self.stats['attack'] if move_data['category'] == 'Physical' else self.stats['special_attack']
            defense_stat = target.stats['defense'] if move_data['category'] == 'Physical' else target.stats['special_defense']
            
            # Base damage formula
            damage = ((((2 * self.level + 10) / 250) * (attack_stat / defense_stat) * move_data['power']) + 2)
            
            # STAB (Same Type Attack Bonus)
            if move_data['type'] in self.types:
                damage *= 1.5
            
            # Type effectiveness
            effectiveness = 1.0
            for target_type in target.types:
                if move_data['type'] in TYPE_EFFECTIVENESS:
                    effectiveness *= TYPE_EFFECTIVENESS[move_data['type']].get(target_type, 1.0)
            
            damage *= effectiveness
            
            # Random factor
            damage *= random.uniform(0.85, 1.0)
            damage = int(damage)
            
            # Apply damage
            target.take_damage(damage)
            
            return {
                'damage': damage,
                'effectiveness': effectiveness,
                'critical': False  # Simplified for now
            }
        
        return {'damage': 0, 'effectiveness': 1.0, 'critical': False}

# Pokemon species database
POKEMON_DATA = {
    'Pikachu': {
        'types': ['Electric'],
        'base_stats': {'hp': 35, 'attack': 55, 'defense': 40, 'special_attack': 50, 'special_defense': 50, 'speed': 90},
        'sprite': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png',
        'moves': ['Thunder Shock', 'Tackle', 'Thunderbolt']
    },
    'Charmander': {
        'types': ['Fire'],
        'base_stats': {'hp': 39, 'attack': 52, 'defense': 43, 'special_attack': 60, 'special_defense': 50, 'speed': 65},
        'sprite': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png',
        'moves': ['Ember', 'Scratch', 'Flamethrower']
    },
    'Squirtle': {
        'types': ['Water'],
        'base_stats': {'hp': 44, 'attack': 48, 'defense': 65, 'special_attack': 50, 'special_defense': 64, 'speed': 43},
        'sprite': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/7.png',
        'moves': ['Water Gun', 'Tackle', 'Surf']
    },
    'Bulbasaur': {
        'types': ['Grass', 'Poison'],
        'base_stats': {'hp': 45, 'attack': 49, 'defense': 49, 'special_attack': 65, 'special_defense': 65, 'speed': 45},
        'sprite': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png',
        'moves': ['Vine Whip', 'Tackle', 'Solar Beam']
    },
    'Geodude': {
        'types': ['Rock', 'Ground'],
        'base_stats': {'hp': 40, 'attack': 80, 'defense': 100, 'special_attack': 30, 'special_defense': 30, 'speed': 20},
        'sprite': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/74.png',
        'moves': ['Tackle', 'Tackle', 'Tackle']
    },
    'Zubat': {
        'types': ['Poison', 'Flying'],
        'base_stats': {'hp': 40, 'attack': 45, 'defense': 35, 'special_attack': 30, 'special_defense': 40, 'speed': 55},
        'sprite': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/41.png',
        'moves': ['Tackle', 'Tackle', 'Tackle']
    },
    'Rattata': {
        'types': ['Normal'],
        'base_stats': {'hp': 30, 'attack': 56, 'defense': 35, 'special_attack': 25, 'special_defense': 35, 'speed': 72},
        'sprite': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/19.png',
        'moves': ['Tackle', 'Tackle', 'Tackle']
    }
}