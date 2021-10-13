'''
Custom datatypes to be used in the chess application.
 - Board
 - Move
'''


# --------------------------------------------------------------------
'''
Imports
'''

from func.convert import arr_to_dict, dict_to_arr, sign
from numpy import ndarray as nparray
import prelegal
import indicator
from copy import deepcopy

# --------------------------------------------------------------------
'''
Imported Variables File Names
'''

var_folder = 'C:/Users/lenovo/Desktop/Coding/VSC Projects/Ches_Dev/ChessAI_3/vars/'
ini_board_name = 'ini_board.txt'
valid_cells_name = 'valid_cells.txt'
piece_dirs_name = 'piece_dirs.txt'
threats_name = 'threats.txt'


# --------------------------------------------------------------------
'''
DataTypes Definitions
'''


class Move:

    '''
    Custom DataType used to represent moves. 
    Castle and pawn promotion are optional input data.
    '''

    ## Class Attributes
    # represents the moves to make when a castle is done
    castle_direction = {0:0, 1:((25, 23), (21, 24)), 2:((25,27), (28, 26)), 3:((95, 93), (91, 94)), 4:((95, 97), (98, 96))}


    def __init__(self,side:int, start_cell:int, final_cell:int, castle_type:int = 0, promo:int = 0):
        '''
        Initialization function.

        Inputs:
            - side: {-1:black, 1:white}
            - start_cell -- initial cell of piece to be moved
            - final_cell -- destination where the piece will be moved
            - castle_type -- type of castle = {0:black queenside, 1:black kingside, 2: white queenside, 3:white kingside} 
            - promo -- promotion value for pawn promotion (index of the piece which the pawn will be promoted to)
        '''
        self.side = side
        self.start = start_cell
        self.final = final_cell
        self.castle_type = castle_type
        self.castle_moves = self.castle_direction[castle_type]
        self.promo = promo

    def __repr__(self):
        return f'Move({self.side}, {self.start}, {self.final}, {self.castle_type}, {self.promo})'


class Board:

    '''
    Custom DataType used to represent a chessboard position.
    Contains:
      - Position of all pieces (dict)
      - Castling status/availability
      - King cells
      - Check status
      - (?) Prelegal moves  -  only generated after initilization  (maybe prelegal is not needed)
      - (?) Legal moves  -  only generated after initialization
      - (?) White and Black side list of pieces in order [pawn, knight, bishop, rook, queen, king]  -  then dont need king_cells attr

    (?) Representation of positions of pieces might need a np.ndarray dtype as well. 
        To do in future as all functions used the dict board representation.

    Inititialization Methods:
      - __init__ -- using dict to show position
    
    '''

    ## Class Attributes
    # cells numbers which represent cells that are on the board
    with open(var_folder + valid_cells_name, 'r') as f:
        valid_cells = eval(f.read())

    # movement directions for all the pieces
    with open(var_folder + piece_dirs_name, 'r') as f:
        piece_dirs = eval(f.read())

    # prelegal functions to run for each piece index
    piece_types_pre = {
        1:prelegal.pawn, 
        2:prelegal.leaper, 
        3:prelegal.slider, 
        4:prelegal.slider, 
        5:prelegal.slider, 
        6:prelegal.leaper
    }

    # piece types that threaten a position from a given direction
    with open(var_folder + threats_name, 'r') as f:
        threats = eval(f.read())

    # conversion of castling type symbol to rook cell
    castle_to_rook_cell = {-6:21, -5:28, 6:91, 5:98}

    # index of slider pieces that are threats from certain directions
    slider_threats = {-11:[3, 5], -10:[4, 5], -9:[3, 5], -1:[4, 5], 1:[4, 5], 9:[3, 5], 10:[4, 5], 11:[3, 5]}

    ## Instance Initialization
    # Initialization using dict
    def __init__(self, dict_position:dict, castle_status:dict = {-6:True, -5:True, 6:True, 5:True}) -> None:

        '''
        Initialize Board DataType with dict.
        '''
        
        self.dict = dict_position
        self.castle_status = {self.castle_to_rook_cell[symbol]:boolean for symbol, boolean in castle_status.items()}
        self.find_king()
        self.add_check_status()
    
    # Initialization using np.ndarray
    @classmethod
    def from_arr(cls, arr:nparray, castle_status:dict = {-6:True, -5:True, 6:True, 5:True}) -> "Board":

        '''
        Initializing Board instance with np.ndarray.
        '''

        return cls(arr_to_dict(arr), castle_status)

    def copy(self):

        '''
        Returns a copy of the Board instance.
        '''

        return deepcopy(self)


    ## Conversion Methods
    # convert position to np array
    def to_arr(self) -> nparray: 

        '''
        Returns the board position as a np.ndarray.
        '''

        return dict_to_arr(self.dict)


    ## Display Methods
    # called when print() is called
    def pretty_print(self) -> str:
        return str(self.to_arr()) + \
            f'\nCastle Status:\n  Black Queenside: {self.castle_status[21]}\n        Kingside: {self.castle_status[28]}' + \
            f'\n  White Queenside: {self.castle_status[91]}\n        Kingside: {self.castle_status[98]}' 

    def __repr__(self):
        return str(self.to_arr()) + f'\n{self.castle_status.values()}'


    ## Add Attributes
    # Save the cell of the kings of both sides
    def find_king(self) -> None:

        '''
        Gets the cell of the kings for both sides and save it as an dictionary (instance attribute) king_pos.
        '''

        self.king_pos = {
            -1: list(self.dict.keys())[list(self.dict.values()).index(-6)], 
            1: list(self.dict.keys())[list(self.dict.values()).index(6)]
        }

    # Save the check status for both sides (True if side is under check)
    def add_check_status(self) -> None:
        
        '''
        See if the either side is under check and save the check status for both sides
        '''

        self.check = {
            -1: indicator.check(self, -1),
            1: indicator.check(self, 1)
        }

    ## Edit Existing Attributes
    # edit position and castle status
    def move(self, move:Move) -> "Board":
        '''
        Performs the move and edits the Board instance information to contain the position after given move is made.
        The current Board instance is affected.
        '''
        
        # if not a castle move
        if move.castle_type == 0:
            # edit the piece in final cell
            if move.promo == 0:
                self.dict[move.final] = self.dict[move.start]
            else:
                self.dict[move.final] = move.promo
            # delete the piece in start cell
            del self.dict[move.start]        

        # if castle move
        else:
            # edit the pieces in final cells (rook and king)
            self.dict[move.castle_moves[0][1]] = self.dict[move.castle_moves[0][0]]
            self.dict[move.castle_moves[1][1]] = self.dict[move.castle_moves[1][0]]
            # delete the pieces in start cells
            del self.dict[move.castle_moves[0][0]]
            del self.dict[move.castle_moves[1][0]]

        # update the corresponding castle status
        self.update_castle(move)

        return self

    def move_copy(self, move:Move) -> "Board":

        '''
        Spawns a new Board object that contains the position after the given move is made.
        The current Board instance is not affected.
        '''

        new_board = self.copy()

        return new_board.move(move)

    def update_castle(self, move:Move) -> None:
        
        '''
        Checks the move made and edits the castle status accordingly
        '''

        # if castling was not done
        if move.castle_type == 0:
            # if rooks moved from initial cell
            if move.start in self.castle_status:
                self.castle_status[move.start] = False
            # if king moved from initial cell
            elif move.start == 25:
                self.castle_status[1], self.castle_status[2] = False, False
            elif move.start == 95:
                self.castle_status[3], self.castle_status[4] = False, False

        else:
            if move.castle_type <= 2:
                self.castle_status[1], self.castle_status[2] = False, False
            else:
                self.castle_status[3], self.castle_status[4] = False, False
