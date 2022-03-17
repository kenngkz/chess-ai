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
from typing import Union
import numpy as np

import constants
import utils

###################
###    Board    ###
###################

'''
hashBoard: Store a board position as a hashBoard

hashBoard: c0 + c1*13 + c2*(13**2) + c3*(13**3) + ... c63*(13**63) + cs*(16*64)
    - each hashCell c can take values from 0 - 12 inclusive
        - piece_index = hashCell_val - 6
'''

hash_size = 13  # number of possible states in each hashCell

class Board:
    ''' Interface for all other chess objects '''

    ## Initialization

    def __init__(self, board_data:Union[int, dict, np.array]) -> None:
        if isinstance(board_data, int):
            self._dehash(board_data)
        else:
            if isinstance(board_data, np.ndarray):
                board_data = utils.arr_to_dict(board_data)
            elif isinstance(list(board_data.values())[0], str):
                board_data = {cell:constants.symbol_piece_index_mapping[symbol] for cell, symbol in board_data.values()}
            self.position = {}
            self.king_position = {-1:None, 1:None}
            for padCell in constants.valid_padCells:
                piece = createPiece(board_data.get(padCell, 0), padCell)
                if piece[1] == 6:
                    self.king_position[piece[0]] = padCell
                self.position[padCell] = piece

    def enhash(self) -> int:
        ''' Returns a hashBoard representing the board position and castle status '''
        hashBoard = 0
        for padCell, piece in self.position.items():
            hashBoard += constants.hashCell_param_mapping[constants.padCell_hashCell_mapping[padCell]] * (piece[0]*piece[1] + 6)
        return hashBoard

    def _dehash(self, hashBoard):
        ''' Parses a hashBoard and sets relevant attributes of Board obj according to data in hashBoard '''
        self.position = {}
        self.king_position = {-1:None, 1:None}
        for hashCell in range(64):
            piece_index = hashBoard//constants.hashCell_param_mapping[hashCell]%hash_size - 6
            padCell = utils.dehash_cell(hashCell)
            piece = createPiece(piece_index, padCell)
            if piece[1] == 6:
                self.king_position[piece[0]] = padCell
            self.position[padCell] = piece

    ## Execute movement on Board

    def move_piece(self, start_padCell, end_padCell, promo=0):
        ''' Moves a piece from given start_padCell to the final_cell '''
        piece = self.position.pop(start_padCell)
        start_piece, end_piece = move_piece(piece, end_padCell, promo)
        self.position[end_padCell] = end_piece
        self.position[start_padCell] = start_piece
        
        if piece[1] == 6:
            self.king_position[piece[0]] = end_padCell

    ## Get information about Board

    def valid_cell(self, padCell) -> bool:
        return padCell in constants.valid_padCells

    def occupant(self, padCell) -> "Piece":
        return self.position[padCell]

    ## Miscellaneous

    def __repr__(self):
        out = "     a  b  c  d  e  f  g  h  \n  +-------------------------+\n"
        for row in range(8):
            row_str = str(row+1) + " | "
            for col in range(8):
                side, index, _, _ = self.occupant(21 + 10*row + col)
                row_str += f" {constants.piece_index_symbol_mapping[side*index]} "
            out += row_str + "|\n"
        out += "  +-------------------------+\n"
        return out

    def to_dict(self):
        ''' Retuns a dict representation of the Board position '''
        return {cell:side*index for cell, (side, index, _, _) in self.position.items()}

    def to_arr(self):
        ''' Returns an array representation of the Board position '''
        return utils.dict_to_arr(self.to_dict())

    def copy(self):
        return Board(self.enhash())

##################
###    Move    ###
##################

class Move:

    # start_cells and final_cells for castle types
    castle_move_cells_mapping = {0:None, -5:((25, 23), (21, 24)), -6:((25,27), (28, 26)), 5:((95, 93), (91, 94)), 6:((95, 97), (98, 96))}

    def __init__(self,side:int, start_padCell:int, end_padCell:int, castle_type:int = 0, promo:int = 0):
        '''
        Inputs:
            - side: {-1:black, 1:white}
            - start_cell -- initial cell of piece to be moved
            - final_cell -- destination where the piece will be moved
            - castle_type (optional) -- type of castle = {0:no castle, -5:black queenside, -6:black kingside, 5: white queenside, 6:white kingside} 
            - promo (optional) -- promotion value for pawn promotion (index of the piece which the pawn will be promoted to)
        '''
        self.side = side
        self.start = start_padCell
        self.end = end_padCell
        self.castle_type = castle_type
        self.castle_move_cells = self.castle_move_cells_mapping[castle_type]
        self.promo = promo

    def __repr__(self) -> str:
        ''' Print Move with initialization parameters '''
        return f'Move({self.side}, {utils.pad_to_usercell(self.start)}, {utils.pad_to_usercell(self.end)}, {self.castle_type}, {self.promo})'
        # return f"Move({self.side}, {self.start}, {self.end}, {self.castle_type}, {self.promo})"

    def __hash__(self) -> int:  # to allow __eq__ to be defined
        return hash(self.to_tuple())

    def __eq__(self, other:"Move"):
        ''' Return True if self and other have the same init params. False otherwise '''
        comparison_attr = ["side", "start", "end", "castle_type", "promo"]  # attributes to compare
        for key in comparison_attr:
            if self.__dict__[key] != other.__dict__[key]:
                return False
        return True

    def to_tuple(self):
        ''' Return init params for the move in a tuple '''
        return (self.side, self.start, self.end, self.castle_type, self.promo)

####################
###    PIECES    ###
####################

## Abstract classes

class Piece(ABC):
    '''
    Abstract class used to build each Piece Type: Pawn, Knight, Bishop, Rook, Queen, King

    All Pieces share the same move_cell() function to change their cell
    '''
    side_name_mapping = {1:"White", -1:"Black"}

    def __init__(self, side, padCell):
        self.side = side
        self.cell = padCell
        self.name = f"{self.side_name_mapping[side]} {self.class_name}"
        self.symbol = self.class_symbol.upper() if self.side>0 else self.class_symbol
        self.index = self.class_index*self.side

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

    @property
    @abstractmethod
    def class_index(self):
        ''' Int index of the piece type '''
        pass

    def move_cell(self, new_padCell):
        self.cell = new_padCell

    def info(self):
        return (f"Piece - Name: {self.name}, Cell: {self.cell}")

class Leaper(Piece):
    ''' Abstract subclass of Piece for Leaper pieces that have common function prelegal_moves() '''
    def threat_map_contribution(self, board:"Board", include_forward=False):
        ''' Yield threat map contribution by the Leaper Piece obj '''
        for direction in self.move_range:
            new_padCell = self.cell + direction
            if board.valid_cell(new_padCell):
                yield new_padCell

class Slider(Piece):
    ''' Abstract subclass of Piece for Slider pieces that have common function prelegal_moves() '''
    def threat_map_contribution(self, board:"Board", include_forward=False):
        ''' YIelds threat map contribution of a Slider Piece obj '''
        for direction in self.move_range:
            for offset_magnitude in range(1, 8):
                new_padCell = self.cell + direction * offset_magnitude
                if board.valid_cell(new_padCell):
                    yield new_padCell
                    occupant = board.occupant(new_padCell)
                    if not occupant is EmptyCell:
                        break
                else:
                    break

## Piece Definitions

class Pawn(Piece):

    # movement range of pawns are dependent on the side. assign move_range when Pawn obj is initialized
    move_range = None
    class_name = "pawn"
    class_symbol = "p"
    class_index = 1

    def __init__(self, side, padCell):
        super().__init__(side, padCell)
        self.move_range = constants.pawn_move_range[side]  # overload move_range for each Pawn depending on its side

    def threat_map_contribution(self, board: "Board", include_forward=False):
        ''' Yield threat map contribution cells of a Pawn object '''
        candidate_padCells = [self.cell+self.move_range[2], self.cell+self.move_range[3]]
        for candidate_padCell in candidate_padCells:
            if board.valid_cell(candidate_padCell):
                yield candidate_padCell
        if include_forward:
            candidate_padCell = self.cell + self.move_range[0]
            if board.valid_cell(candidate_padCell):
                if board.occupant(candidate_padCell) is EmptyCell:
                    yield candidate_padCell
                    jump_allowed = self.cell//10==8 if self.side == 1 else self.cell//10==3
                    candidate_padCell = self.cell + self.move_range[1]
                    if jump_allowed:  # if pawn is in starting row
                        if board.occupant(candidate_padCell) is EmptyCell:
                            yield candidate_padCell

    def candidate_move_cell(self, board:"Board"):
        # forward move cells
        candidate_padCell = self.cell + self.move_range[0]
        if isinstance(board.occupant(candidate_padCell), EmptyCell):
            yield candidate_padCell, False  # 2nd output indicates whether or not to include in threat_map
            jump_allowed = self.cell//10==8 if self.side == 1 else self.cell//10==3
            candidate_padCell = self.cell + self.move_range[1]
            if jump_allowed:  # if pawn is in starting row
                if isinstance(board.occupant(candidate_padCell), EmptyCell):
                    yield candidate_padCell, False
        # capture move cells
        candidate_padCells = [self.cell+self.move_range[2], self.cell+self.move_range[3]]
        for candidate_padCell in candidate_padCells:
            if board.valid_cell(candidate_padCell):
                yield candidate_padCell, True
        

class Knight(Leaper):
    move_range = [-12, -21, -19, -8, 12, 21, 19, 8]
    class_name = "knight"
    class_symbol = "n"
    class_index = 2

class Bishop(Slider):
    move_range = [-11, -9, 11, 9]
    class_name = "bishop"
    class_symbol = "b"
    class_index = 3

class Rook(Slider):
    move_range = [-1, -10, 1, 10]
    class_name = "rook"
    class_symbol = "r"
    class_index = 4

class Queen(Slider):
    move_range = [-1, -11, -10, -9, 1, 11, 10, 9]
    class_name = "queen"
    class_symbol = "q"
    class_index = 5

class King(Leaper):
    move_range = [-1, -11, -10, -9, 1, 11, 10, 9]
    class_name = "king"
    class_symbol = "k"
    class_index = 6

########################
###    Empty Cell    ###
########################

class EmptyCell:
    name = "Empty cell"
    symbol = "-"
    side = 0
    class_index = 0
    index = 0

    def __init__(self, index, padCell):
        pass

####################
###    Pieces    ###
####################

'''
Piece = (side, piece_type, piece_padCell, move_range)
'''

## Piece factory
def createPiece(piece_index, padCell):
    ''' Piece factory to create pieces '''
    return (utils.sign(piece_index), abs(piece_index), padCell, constants.piece_index_move_range_mapping[piece_index],)

## Threat map functions
def pawn_threat_map(side:int, padCell:int, move_range:tuple, board:"Board"):
    ''' Generate threat map for pawn '''
    # forward move cells
    candidate_padCell = padCell + move_range[0]
    if board.occupant(candidate_padCell)[0] == 0:
        yield candidate_padCell, False  # 2nd output indicates whether or not to include in threat_map
        jump_allowed = padCell//10==8 if side == 1 else padCell//10==3
        candidate_padCell = padCell + move_range[1]
        if jump_allowed:  # if pawn is in starting row
            if isinstance(board.occupant(candidate_padCell), EmptyCell):
                yield candidate_padCell, False
    # capture move cells
    candidate_padCells = [padCell+move_range[2], padCell+move_range[3]]
    for candidate_padCell in candidate_padCells:
        if board.valid_cell(candidate_padCell):
            yield candidate_padCell, True

def leaper_threat_map(side:int, padCell:int, move_range:tuple, board:"Board"):
    ''' Generate threat map for leaper '''
    for direction in move_range:
        new_padCell = padCell + direction
        if board.valid_cell(new_padCell):
            yield new_padCell, None

def slider_threat_map(side:int, padCell:int, move_range:tuple, board:"Board"):
    ''' Generate threat map for slider '''
    for direction in move_range:
        for offset_magnitude in range(1, 8):
            new_padCell = padCell + direction * offset_magnitude
            if board.valid_cell(new_padCell):
                yield new_padCell, None
                if board.occupant(new_padCell)[0] != 0:
                    break
            else:
                break

def dummy(*args):
    ''' Generate threat map for empty cell '''
    return ()

threat_map_func_mapping = {0:dummy, 1:pawn_threat_map, 2:leaper_threat_map, 3:slider_threat_map, 4:slider_threat_map, 5:slider_threat_map, 6:leaper_threat_map}
def piece_threat_map(piece, board):
    ''' Generate threat map for a given piece '''
    side, piece_index, piece_padCell, move_range = piece
    threat_map_func = threat_map_func_mapping[piece_index]
    for padCell in threat_map_func(side, piece_padCell, move_range, board):
        yield padCell

## Move piece function
def move_piece(piece, new_padCell, new_index):
    side, index, padCell, move_range = piece
    if new_index != 0:
        index = new_index
    return (0, 0, padCell, constants.piece_index_move_range_mapping[0]), (side, index, new_padCell, move_range)