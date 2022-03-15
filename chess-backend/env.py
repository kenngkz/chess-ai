from game import Game, GameState
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
        self.action_space = self.game.legal_moves[self.game.player_to_move]
        return tuple([*utils.dict_to_arr(self.game.board.position).flatten(), *list(self.game.castle_status.values()), *self.game.check_status.values()])

    def step(self, action):
        assert action in self.action_space, f"Action {action} not in action_space"
        self.game.make_move(action, permanent=True)
        self.game.all_legal_moves()
        self.action_space = self.game.legal_moves[self.game.player_to_move]
        obs = tuple([*utils.dict_to_arr(self.game.board.position).flatten(), *list(self.game.castle_status.values()), *self.game.check_status.values()])
        done = self.game.game_over() != None
        return obs, self.action_space, done, None

    def set_state(self, gamestate:"GameState", opponent=None):
        self.game = Game.load()

    def render(self):
        ''' Prints the board position in console '''
        pass

    def render_actions(self):
        ''' Prints the legal moves in console '''
        pass

    def save(self):
        ''' Returns EnvSave obj with current game state'''
        pass