'''
Manages and runs the chess game.
'''

from chess_objects import Board, Move

class GameSave:
    pass  # TODO

class Game:

    def __init__(self):
        self.board = Board()

    @classmethod
    def load(cls):
        pass # TODO

    def game_over(self):
        '''
        Checks if game is over. 
        Returns None if not over, 0 if stalemate, 1 if White wins and -1 if Black wins
        '''
        pass