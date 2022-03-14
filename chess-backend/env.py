from game import Game
import utils

import numpy as np

# class EnvSave:
    
#     def __init__(self):
#         pass
    
#     def save_to_file(self, filename):
#         ''' Saves an EnvSave obj to a file '''
#         pass

#     @classmethod
#     def load_file(cls, filename):
#         ''' Load an EnvSave obj from a save file '''
#         pass

class ChessEnv:
    '''
    Chess-v0

    observation structure: list of len 70
        - 64 entries specifying the piece index in each cell (order: row1col1, row1col2, ...)
        - 4 entries specifying the castle status (whether castling is allowed for each castle type)
            - order: black queenside, black queenside, white queenside, white kingside
        - 2 entries specifying whether each side is under check (order: white, black)
    '''

    def __init__(self, opponent=None):
        self.game = None
        self.opponent = opponent

    @classmethod  # do i need this? can use set_state instead
    def load(self, filepath):
        pass

    def reset(self):
        self.game = Game()
        self.game.all_legal_moves()
        self.action_space = self.game.legal_moves
        return tuple([*utils.dict_to_arr(self.game.board.position).flatten(), *list(self.game.castle_status.values()), *self.game.check_status.values()])

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