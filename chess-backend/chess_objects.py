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

    # mapping from castle type to change in position
    castle_positions_mapping = {0:0, -5:((25, 23), (21, 24)), -6:((25,27), (28, 26)), 5:((95, 93), (91, 94)), 6:((95, 97), (98, 96))}

    # castle type names mapping
    castle_names = {-5:'Black Queenside Castle', -6:'Black Kingside Castle', 5: 'White Queenside Castle', 6:'White Kingside Castle'}

    def __init__(self,side:int, start_cell:int, final_cell:int, castle_type:int = 0, promo:int = 0):
        '''
        Inputs:
            - side: {-1:black, 1:white}
            - start_cell -- initial cell of piece to be moved
            - final_cell -- destination where the piece will be moved
            - castle_type (optional) -- type of castle = {0:no castle, -5:black queenside, -6:black kingside, 5: white queenside, 6:white kingside} 
            - promo (optional) -- promotion value for pawn promotion (index of the piece which the pawn will be promoted to)
        '''
        self.side = side
        self.start = start_cell
        self.final = final_cell
        self.castle_type = castle_type
        self.castle_positions = self.castle_direction[castle_type]
        self.promo = promo

    def __repr__(self) -> str:
        ''' Print Move with initialization parameters '''
        return f'Move({self.side}, {self.start}, {self.final}, {self.castle_type}, {self.promo})'

    def __hash__(self) -> int:  # to allow __eq__ to be defined
        return hash((self.side, self.start, self.final, self.castle_type, self.promo))

    def __eq__(self, other:"Move"):
        ''' Return True if self and other have the same init params. False otherwise '''
        comparison_attr = ["side", "start", "final", "castle_type", "promo"]  # attributes to compare
        for key in comparison_attr:
            if self.__dict__[key] != other.__dict__[key]:
                return False
        return True

    def to_tuple(self):
        ''' Return init params for the move in a tuple '''
        return (self.side, self.start, self.final, self.castle_type, self.promo)

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