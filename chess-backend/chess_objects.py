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
from copy import deepcopy
from tracemalloc import start

import constants
import utils

class Move:

    # start_cells and final_cells for castle types
    castle_move_cells_mapping = {0:None, -5:((25, 23), (21, 24)), -6:((25,27), (28, 26)), 5:((95, 93), (91, 94)), 6:((95, 97), (98, 96))}

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
        self.castle_move_cells = self.castle_move_cells_mapping[castle_type]
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
                king_position[utils.sign(index)] = cell
        return king_position

    # PUT functions (changes some attr of Board obj)

    def move_piece(self, start_cell, final_cell):
        ''' Moves a piece from given start_cell to the final_cell '''
        # print(f"Piece Moved: {self.occupant(start_cell)}. Cell movement: {start_cell} -> {final_cell}")
        piece = self.position.pop(start_cell)  # raises KeyError if no piece exists in start_cell
        self.position[final_cell] = piece
        piece.move_cell(final_cell)
        if piece is King:
            self.king_position[piece.side*6] = final_cell

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
        out = "     1  2  3  4  5  6  7  8  \n  +-------------------------+\n"
        for row in range(8):
            row_str = str(row+2) + " | "
            for col in range(8):
                row_str += f" {self.occupant(21 + 10*row + col).symbol} "
            out += row_str + "|\n"
        out += "  +-------------------------+\n"
        return out

    def copy(self):
        new_board = Board({21:6, 23:-6})
        new_board.position = deepcopy(self.position)
        new_board.king_position = self.king_position.copy()
        return new_board


######################
###     PIECES     ###
######################

class EmptyCell:
    name = "Empty cell"
    symbol = "-"
    side = None

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
        ''' Prelegal moves of a piece '''
        pass

    @abstractmethod
    def threat_map_contribution(self, board:"Board", include_forward=False):
        ''' Threat map contribution of a piece '''
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

    def move_cell(self, new_cell):
        self.cell = new_cell

    def info(self):
        return (f"Piece - Name: {self.name}, Cell: {self.cell}")

class Leaper(Piece):
    ''' Abstract subclass of Piece for Leaper pieces that have common function prelegal_moves() '''

    def prelegal_moves(self, board: "Board"):
        ''' Prelegal moves of a piece '''
        valid_prelegal_cells = []
        for direction in self.move_range:
            new_cell = self.cell + direction
            new_cell_occupant = board.occupant(new_cell)
            if board.valid_cell(new_cell):
                if new_cell_occupant is EmptyCell or new_cell_occupant.side != self.side:
                    valid_prelegal_cells.append(new_cell)
        return [Move(self.side, self.cell, new_cell) for new_cell in valid_prelegal_cells]

    def threat_map_contribution(self, board:"Board", include_forward=False):
        ''' Yield threat map contribution by the Leaper Piece obj '''
        for direction in self.move_range:
            new_cell = self.cell + direction
            if board.valid_cell(new_cell):
                yield new_cell

class Slider(Piece):
    ''' Abstract subclass of Piece for Slider pieces that have common function prelegal_moves() '''
    def prelegal_moves(self, board: "Board"):
        ''' Prelegal moves of a piece '''
        valid_prelegal_cells = []
        for direction in self.move_range:
            for offset_magnitude in [1, 2, 3, 4, 5, 6, 7]:
                new_cell = self.cell + direction * offset_magnitude
                if board.valid_cell(new_cell):
                    occupant = board.occupant(new_cell)
                    if not occupant is EmptyCell:
                        if occupant.side != self.side:
                            valid_prelegal_cells.append(new_cell)
                        break
                    else:
                        valid_prelegal_cells.append(new_cell)
                else:
                    break
        return [Move(self.side, self.cell, new_cell) for new_cell in valid_prelegal_cells]

    def threat_map_contribution(self, board:"Board", include_forward=False):
        ''' YIelds threat map contribution of a Slider Piece obj '''
        for direction in self.move_range:
            for offset_magnitude in range(1, 8):
                new_cell = self.cell + direction * offset_magnitude
                if board.valid_cell(new_cell):
                    yield new_cell
                    occupant = board.occupant(new_cell)
                    if not occupant is EmptyCell:
                        break
                else:
                    break

class Pawn(Piece):

    # movement range of pawns are dependent on the side. assign move_range when Pawn obj is initialized
    move_range = None
    class_name = "pawn"
    class_symbol = "p"

    def __init__(self, side, cell):
        super().__init__(side, cell)
        self.move_range = constants.pawn_move_range[side]  # overload move_range for each Pawn depending on its side

    def prelegal_moves(self, board: "Board"):
        ''' Prelegal moves of a pawn '''
        valid_prelegal_moves = []
        candidate_cell = self.cell + self.move_range[0]
        # forward moves
        if board.valid_cell(candidate_cell):
            occupant = board.occupant(candidate_cell)
            if occupant is EmptyCell:
                valid_prelegal_moves.append(Move(self.side, self.cell, candidate_cell))
                candidate_cell = self.cell + self.move_range[1]
                jump_allowed = self.cell//10==8 if self.side == 1 else self.cell//10==3
                if jump_allowed:
                    if board.valid_cell(candidate_cell):
                        if board.occupant(candidate_cell) is EmptyCell:
                            valid_prelegal_moves.append(Move(self.side, self.cell, candidate_cell))
        # capture moves
        candidate_cells = [self.cell+self.move_range[2], self.cell+self.move_range[3]]
        for candidate_cell in candidate_cells:
            if board.valid_cell(candidate_cell):
                if board.occupant(candidate_cell).side == -self.side:
                    valid_prelegal_moves.append(Move(self.side, self.cell, candidate_cell))
        # if in promotion position (2nd last row), convert all moves into promotion moves
        promo_allowed = self.cell//10==3 if self.side == 1 else self.cell//10==8
        if promo_allowed:
            return [Move(self.side, self.cell, move.final, 0, promo_val) for promo_val in [2, 3, 4, 5] for move in valid_prelegal_moves]
        return valid_prelegal_moves

    def threat_map_contribution(self, board: "Board", include_forward=False):
        ''' Yield threat map contribution cells of a Pawn object '''
        candidate_cells = [self.cell+self.move_range[2], self.cell+self.move_range[3]]
        for candidate_cell in candidate_cells:
            if board.valid_cell(candidate_cell):
                yield candidate_cell
        if include_forward:
            candidate_cell = self.cell + self.move_range[0]
            if board.occupant(candidate_cell) is EmptyCell:
                yield candidate_cell
                jump_allowed = self.cell//10==8 if self.side == 1 else self.cell//10==3
                candidate_cell = self.cell + self.move_range[1]
                if jump_allowed:  # if pawn is in starting row
                    if board.occupant(candidate_cell) is EmptyCell:
                        yield candidate_cell

    def candidate_move_cell(self, board:"Board"):
        # forward move cells
        candidate_cell = self.cell + self.move_range[0]
        if board.occupant(candidate_cell) is EmptyCell:
            yield candidate_cell, False  # 2nd output indicates whether or not to include in threat_map
            jump_allowed = self.cell//10==8 if self.side == 1 else self.cell//10==3
            candidate_cell = self.cell + self.move_range[1]
            if jump_allowed:  # if pawn is in starting row
                if board.occupant(candidate_cell) is EmptyCell:
                    yield candidate_cell, False
        # capture move cells
        candidate_cells = [self.cell+self.move_range[2], self.cell+self.move_range[3]]
        for candidate_cell in candidate_cells:
            if board.valid_cell(candidate_cell):
                yield candidate_cell, True
        

class Knight(Leaper):
    move_range = [-12, -21, -19, -8, 12, 21, 19, 8]
    class_name = "knight"
    class_symbol = "n"

class Bishop(Slider):
    move_range = [-11, -9, 11, 9]
    class_name = "bishop"
    class_symbol = "b"

class Rook(Slider):
    move_range = [-1, -10, 1, 10]
    class_name = "rook"
    class_symbol = "r"

class Queen(Slider):
    move_range = [-1, -11, -10, -9, 1, 11, 10, 9]
    class_name = "queen"
    class_symbol = "q"

class King(Leaper):
    move_range = [-1, -11, -10, -9, 1, 11, 10, 9]
    class_name = "king"
    class_symbol = "k"