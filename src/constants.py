# Screen dimensions
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60

# Tile size
TILE_SIZE = 32

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (64, 64, 64)

# Pokemon types
POKEMON_TYPES = [
    'Normal', 'Fire', 'Water', 'Electric', 'Grass', 'Ice',
    'Fighting', 'Poison', 'Ground', 'Flying', 'Psychic',
    'Bug', 'Rock', 'Ghost', 'Dragon', 'Dark', 'Steel', 'Fairy'
]

# Type effectiveness chart (multiplier)
TYPE_EFFECTIVENESS = {
    'Fire': {'Grass': 2.0, 'Ice': 2.0, 'Bug': 2.0, 'Steel': 2.0, 'Water': 0.5, 'Fire': 0.5, 'Rock': 0.5, 'Dragon': 0.5},
    'Water': {'Fire': 2.0, 'Ground': 2.0, 'Rock': 2.0, 'Water': 0.5, 'Grass': 0.5, 'Dragon': 0.5},
    'Electric': {'Water': 2.0, 'Flying': 2.0, 'Electric': 0.5, 'Grass': 0.5, 'Dragon': 0.5, 'Ground': 0.0},
    'Grass': {'Water': 2.0, 'Ground': 2.0, 'Rock': 2.0, 'Fire': 0.5, 'Grass': 0.5, 'Poison': 0.5, 'Flying': 0.5, 'Bug': 0.5, 'Dragon': 0.5, 'Steel': 0.5},
    'Normal': {'Rock': 0.5, 'Ghost': 0.0, 'Steel': 0.5},
    'Fighting': {'Normal': 2.0, 'Ice': 2.0, 'Rock': 2.0, 'Dark': 2.0, 'Steel': 2.0, 'Poison': 0.5, 'Flying': 0.5, 'Psychic': 0.5, 'Bug': 0.5, 'Fairy': 0.5, 'Ghost': 0.0},
    'Poison': {'Grass': 2.0, 'Fairy': 2.0, 'Poison': 0.5, 'Ground': 0.5, 'Rock': 0.5, 'Ghost': 0.5, 'Steel': 0.0},
    'Ground': {'Fire': 2.0, 'Electric': 2.0, 'Poison': 2.0, 'Rock': 2.0, 'Steel': 2.0, 'Grass': 0.5, 'Bug': 0.5, 'Flying': 0.0},
    'Flying': {'Electric': 0.5, 'Rock': 0.5, 'Steel': 0.5, 'Grass': 2.0, 'Fighting': 2.0, 'Bug': 2.0},
    'Psychic': {'Fighting': 2.0, 'Poison': 2.0, 'Psychic': 0.5, 'Steel': 0.5, 'Dark': 0.0},
    'Bug': {'Grass': 2.0, 'Psychic': 2.0, 'Dark': 2.0, 'Fire': 0.5, 'Fighting': 0.5, 'Poison': 0.5, 'Flying': 0.5, 'Ghost': 0.5, 'Steel': 0.5, 'Fairy': 0.5},
    'Rock': {'Fire': 2.0, 'Ice': 2.0, 'Flying': 2.0, 'Bug': 2.0, 'Fighting': 0.5, 'Ground': 0.5, 'Steel': 0.5},
    'Ghost': {'Psychic': 2.0, 'Ghost': 2.0, 'Dark': 0.5, 'Normal': 0.0},
    'Dragon': {'Dragon': 2.0, 'Steel': 0.5, 'Fairy': 0.0},
    'Dark': {'Fighting': 0.5, 'Dark': 0.5, 'Fairy': 0.5, 'Psychic': 2.0, 'Ghost': 2.0},
    'Steel': {'Ice': 2.0, 'Rock': 2.0, 'Fairy': 2.0, 'Fire': 0.5, 'Water': 0.5, 'Electric': 0.5, 'Steel': 0.5},
    'Fairy': {'Fighting': 2.0, 'Dragon': 2.0, 'Dark': 2.0, 'Fire': 0.5, 'Poison': 0.5, 'Steel': 0.5}
}

# Moves database
MOVES_DB = {
    'Tackle': {'type': 'Normal', 'power': 40, 'accuracy': 100, 'pp': 35, 'category': 'Physical'},
    'Scratch': {'type': 'Normal', 'power': 40, 'accuracy': 100, 'pp': 35, 'category': 'Physical'},
    'Ember': {'type': 'Fire', 'power': 40, 'accuracy': 100, 'pp': 25, 'category': 'Special'},
    'Water Gun': {'type': 'Water', 'power': 40, 'accuracy': 100, 'pp': 25, 'category': 'Special'},
    'Thunder Shock': {'type': 'Electric', 'power': 40, 'accuracy': 100, 'pp': 30, 'category': 'Special'},
    'Vine Whip': {'type': 'Grass', 'power': 45, 'accuracy': 100, 'pp': 25, 'category': 'Physical'},
    'Flamethrower': {'type': 'Fire', 'power': 90, 'accuracy': 100, 'pp': 15, 'category': 'Special'},
    'Surf': {'type': 'Water', 'power': 90, 'accuracy': 100, 'pp': 15, 'category': 'Special'},
    'Thunderbolt': {'type': 'Electric', 'power': 90, 'accuracy': 100, 'pp': 15, 'category': 'Special'},
    'Solar Beam': {'type': 'Grass', 'power': 120, 'accuracy': 100, 'pp': 10, 'category': 'Special'},
}