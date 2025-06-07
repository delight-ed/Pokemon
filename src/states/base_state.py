class BaseState:
    def __init__(self, game):
        self.game = game
    
    def enter(self, **kwargs):
        pass
    
    def handle_event(self, event):
        pass
    
    def update(self, dt):
        pass
    
    def draw(self, screen):
        pass