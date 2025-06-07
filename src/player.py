from .pokemon import Pokemon

class Player:
    def __init__(self):
        self.name = "Ash"
        self.x = 400
        self.y = 300
        self.speed = 150
        self.direction = 'down'
        
        # Pokemon team (max 6)
        self.pokemon_team = [
            Pokemon('Pikachu', level=10),
            Pokemon('Charmander', level=8)
        ]
        
        # Items
        self.items = {
            'Potion': 5,
            'Pokeball': 10,
            'Super Potion': 2
        }
        
        # Game progress
        self.badges = []
        self.money = 1000
        
    def get_active_pokemon(self):
        for pokemon in self.pokemon_team:
            if not pokemon.is_fainted():
                return pokemon
        return None
    
    def has_usable_pokemon(self):
        return any(not p.is_fainted() for p in self.pokemon_team)
    
    def heal_all_pokemon(self):
        for pokemon in self.pokemon_team:
            pokemon.heal()
            # Restore PP
            for move in pokemon.moves:
                if move in pokemon.move_pp:
                    pokemon.move_pp[move] = pokemon.move_pp.get(move, 0) + 10
    
    def add_pokemon(self, pokemon):
        if len(self.pokemon_team) < 6:
            self.pokemon_team.append(pokemon)
            return True
        return False