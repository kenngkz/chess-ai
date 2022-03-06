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

import constants
import utils

class Move:

    # mapping from castle type to change in position
    castle_positions_mapping = {0:0, -5:((25, 23), (21, 24)), -6:((25,27), (28, 26)), 5:((95, 93), (91, 94)), 6:((95, 97), (98, 96))}

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
    
    def __init__(self, position=constants.initial_board_position):
        ''' Initialize Board from dict '''
        self.position = self._position_add_pieces(position)
        self.castle_status = {-5:True, -6:True, 5:True, 6:True}  # tracks whether castling is allowed
        self.king_position = self._get_king_position(position)

    @classmethod
    def load_array(cls, array):
        ''' Initilize Board from array '''
        return cls(utils.arr_to_dict(array))

    # GET functions

    def occupant(self, cell):
        ''' Get occupant object in given cell '''
        return self.position.get(cell, EmptyCell)

    def valid_cell(self, cell):
        ''' Return True if the given cell is valid '''
        return cell in constants.valid_cells

    def to_arr(self):
        ''' Returns an array representation of the Board position '''
        return utils.dict_to_arr(self.position)

    def _get_king_position(self, position):
        ''' Returns the positions of the 2 kings '''
        king_position = {}
        for cell, index in position.items():
            if abs(index) == 6:
                king_position[index] = cell
        return king_position

    # PUT functions (changes some attr of Board obj)

    def move_piece(self, start_cell, end_cell):
        ''' Moves a piece from given start_cell to the end_cell '''
        piece = self.position.pop(start_cell)  # raises KeyError if no piece exists in start_cell
        self.position[end_cell] = piece
        if piece is King:
            self.king_position[piece.side*6] = end_cell

    # Miscellaneous functions

    def _position_add_pieces(self, position:dict) -> dict:
        # mapping of piece index to Piece objects
        piece_mapping = {1:Pawn, 2:Knight, 3:Bishop, 4:Rook, 5:Queen, 6:King}
        return {
            cell : piece_mapping[abs(index)](utils.sign(index), cell)  # piece_mapping[] returns a Piece subclass, (sign(index), cell) initializes the object
             for cell, index in position.items()
            }

    def __repr__(self):
        # board position
        out = "     0  1  2  3  4  5  6  7  \n  +-------------------------+\n"
        for row in range(8):
            row_str = str(row) + " | "
            for col in range(8):
                row_str += f" {self.occupant(21 + 10*row + col).symbol} "
            out += row_str + "|\n"
        out += "  +-------------------------+\n"
        # castle status
        enabled_disabled_mapping = {True:"Enabled", False:"Disabled"}
        out += "Castle Status:\n"
        for castle_type, status in self.castle_status.items():
            out += f"    {constants.castle_names[castle_type]} -- {enabled_disabled_mapping[status]}\n"
        return out


######################
###     PIECES     ###
######################

class EmptyCell:
    name = "Empty cell"
    symbol = "-"

class Piece(ABC):
    '''
    Abstract class used to build each Piece Type: Pawn, Knight, Bishop, Rook, Queen, King

    All Pieces share the same move_cell() function to change their cell
    '''
    side_name_mapping = {1:"White", -1:"Black"}

    def __init__(self, side, cell):
        self.side = side
        self.cell = cell
        self.name = f"{self.side_name_mapping[side]} {self.class_name}"
        self.symbol = self.class_symbol.upper() if self.side>0 else self.class_symbol

    @abstractmethod
    def prelegal_moves(self, board:"Board"):
        pass

    @property
    @abstractmethod
    def move_range(self):
        ''' Movement range of a piece without considering other pieces or cell validity '''
        pass

    @property
    @abstractmethod
    def class_name(self):
        ''' Name of the piece '''
        pass

    @property
    @abstractmethod
    def class_symbol(self):
        ''' Symbol of the piece type '''
        pass

    def move_cell(self, move:"Move"):
        pass   # TODO

class Pawn(Piece):

    # movement range of pawns are dependent on the side. assign move_range when Pawn obj is initialized
    move_range = None
    class_name = "pawn"
    class_symbol = "p"

    def __init__(self, side, position):
        super().__init__(side, position)
        self.move_range = constants.pawn_move_range[side]  # overload move_range for each Pawn depending on its side

    def prelegal_moves(self, board: "Board"):
        return super().prelegal_moves(board)  # TODO

class Knight(Piece):
    move_range = [-12, -21, -19, -8, 12, 21, 19, 8]
    class_name = "knight"
    class_symbol = "n"

    def prelegal_moves(self, board: "Board"):
        return super().prelegal_moves(board)  # TODO

class Bishop(Piece):
    move_range = [-11, -9, 11, 9]
    class_name = "bishop"
    class_symbol = "b"

    def prelegal_moves(self, board: "Board"):
        return super().prelegal_moves(board)  # TODO

class Rook(Piece):
    move_range = [-1, -10, 1, 10]
    class_name = "rook"
    class_symbol = "r"

    def prelegal_moves(self, board: "Board"):
        return super().prelegal_moves(board)  # TODO

class Queen(Piece):
    move_range = [-1, -11, -10, -9, 1, 11, 10, 9]
    class_name = "queen"
    class_symbol = "q"

    def prelegal_moves(self, board: "Board"):
        return super().prelegal_moves(board)  # TODO

class King(Piece):
    move_range = [-1, -11, -10, -9, 1, 11, 10, 9]
    class_name = "king"
    class_symbol = "k"

    def prelegal_moves(self, board: "Board"):
        return super().prelegal_moves(board)  # TODO