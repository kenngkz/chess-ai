'''
Chess objects used in the environment.
This script contains definitions for:
1. Move
2. Board
3. Piece - Constructor for building each individual piece
4. Pawn
6. Knight
7. Bishop
8. Rook
9. Queen
10. King
'''

from abc import ABC, abstractmethod

from constants import pawn_move_range

class Move:
    pass

class Board:
    pass

class Piece(ABC):
    '''
    Abstract class used to build each Piece Type: Pawn, Knight, Bishop, Rook, Queen, King

    All Pieces share the same move_position() function to change their position
    '''
    @abstractmethod
    def prelegal_moves(self, board:"Board"):
        pass

    @property
    @abstractmethod
    def move_range(self):
        ''' Movement range of a piece without considering other pieces or cell validity '''
        pass

    def move_position(self, move:"Move"):
        pass   # TODO

class Pawn(Piece):
    
    # movement range of pawns are dependent on the side. assign move_range when Pawn obj is initialized
    move_range = None

    def __init__(self, side, position):
        self.side = side
        self.position = position
        self.move_range = pawn_move_range[side]

    def prelegal_moves(self, board: "Board"):
        return super().prelegal_moves(board)  # TODO

class Knight(Piece):
    move_range = [-12, -21, -19, -8, 12, 21, 19, 8]

    def __init__(self, side, position):
        self.side = side
        self.position = position

    def prelegal_moves(self, board: "Board"):
        return super().prelegal_moves(board)  # TODO

class Bishop(Piece):
    move_range = [-11, -9, 11, 9]

    def __init__(self, side, position):
        self.side = side
        self.position = position

    def prelegal_moves(self, board: "Board"):
        return super().prelegal_moves(board)  # TODO

class Rook(Piece):
    move_range = [-1, -10, 1, 10]

    def __init__(self, side, position):
        self.side = side
        self.position = position

    def prelegal_moves(self, board: "Board"):
        return super().prelegal_moves(board)  # TODO

class Queen(Piece):
    move_range = [-1, -11, -10, -9, 1, 11, 10, 9]

    def __init__(self, side, position):
        self.side = side
        self.position = position

    def prelegal_moves(self, board: "Board"):
        return super().prelegal_moves(board)  # TODO

class King(Piece):
    move_range = [-1, -11, -10, -9, 1, 11, 10, 9]

    def __init__(self, side, position):
        self.side = side
        self.position = position

    def prelegal_moves(self, board: "Board"):
        return super().prelegal_moves(board)  # TODO