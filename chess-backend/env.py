

class EnvSave:
    
    def __init__(self):
        pass
    
    def save_to_file(self, filename):
        ''' Saves an EnvSave obj to a file '''
        pass

    @classmethod
    def load_file(cls, filename):
        ''' Load an EnvSave obj from a save file '''
        pass

class ChessEnv:

    def __init__(self):
        pass

    def reset(self):
        pass

    def step(self, action):
        pass

    def set_state(self, state:"EnvSave"):
        pass

    def render(self):
        ''' Prints the board position in console '''
        pass

    def save(self):
        ''' Returns EnvSave obj with current game state'''
        pass