'''
Custom datatypes to be used in the chess application.
 - Board
 - Move
'''


# --------------------------------------------------------------------
'''
Imports
'''

from Chess_App.app import move
from convert import arr_to_dict, dict_to_arr
from numpy import ndarray as nparray
import get
import indicator
from copy import deepcopy
from typing import Tuple

# --------------------------------------------------------------------
'''
Imported Variables File Names
'''

var_folder = '../chess/vars/'
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
    castle_direction = {0:0, -5:((25, 23), (21, 24)), -6:((25,27), (28, 26)), 5:((95, 93), (91, 94)), 6:((95, 97), (98, 96))}

    # conversion from piece index to piece name
    index_to_name = {None: 'castle', 0:'empty cell', 1:'pawn', -1:'pawn', 2:'knight', -2:'knight', 3:'bishop', -3:'bishop', 4:'rook', -4:'rook', 
                     5:'queen', -5:'queen', 6:'king', -6:'king'}

    # castle type names
    castle_names = {-5:'Black Queenside Castle', -6:'Black Kingside Castle', 5: 'White Queenside Castle', 6:'White Kingside Castle'}

    # persistance files
    data_folder = "C:/Users/lenovo/Desktop/Coding/VSC Projects/Chess_App/data/"
    history_file = "move_history.txt"


    ## Initilization Methods
    def __init__(self,side:int, start_cell:int, final_cell:int, castle_type:int = 0, promo:int = 0):
        '''
        Initialization function.

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
        self.castle_moves = self.castle_direction[castle_type]
        self.promo = promo


    ## Display Methods
    def __repr__(self) -> str:

        '''
        Print move initialization parameters
        '''
        
        return f'Move({self.side}, {self.start}, {self.final}, {self.castle_type}, {self.promo})'


    def info_str(self, show=True) -> str:
        
        '''
        Print str with additional details on the moving piece and the captured piece (if any).
        Method self.add_board() must be run prior to running this method.
        
        Print format:
        $Move_initialization_parameters$: $moving_piece_name$ -> $captured_piece_name$ (if no capture = 'empty cell')
        '''
        try:
            parameters = f'Move({self.side}, {self.start}, {self.final}, {self.castle_type}, {self.promo}): '
            if self.start == 0:
                movement = f'{self.castle_names[self.castle_type]}'
            else:
                movement = f'{self.index_to_name[get.index(self.board, self.start)]} -> ' \
                    + f'{self.index_to_name[get.index(self.board, self.final)]}'
            output = parameters + movement
        except AttributeError:
            output = "AttributeError: board attribute of Move object not found.\nPlease run the add_board() method of this object before running this method"            

        if show:
            print(output)
        else:
            return output

    def info(self, show=True) -> Tuple[int]:

        '''
        Print tuple with additional details on the moving piece and the captured piece (if any).
        Method self.add_board() must be run prior to running this method.

        Tuple format:
        (side, start, final, castle_type, promo, moving_piece_index, captured_piece_index)
        '''

        try:
            output = (self.side, self.start, self.final, self.castle_type, self.promo, None, None)
            if self.start != 0:
                output[-2] = get.index(self.board, self.start)
                output[-1] = get.index(self.board, self.final)
        except AttributeError:
            output = "AttributeError: board attribute of Move object not found.\nPlease run the add_board() method of this object before running this method" 

        if show:
            print(output)
        else:
            return output



    ## Add Attributes
    def add_board(self, board:"Board") -> None:
        '''
        Add the board that the move is related to under this move.
        For display purposes: self.print_det()
        '''
        self.board = board

    ## Conversion Methods
    def __hash__(self) -> int:

        '''
        Returns the same hash for Moves with the same parameters.

        Enables __eq__ (==) to return True if 2 Moves have the same parameters.
        '''
        return hash((self.side, self.start, self.final, self.castle_type, self.promo))

    def to_tuple(self) -> Tuple[int]:

        '''
        Returns a tuple containing the initialization parameters for the move.
        '''

        return (self.side, self.start, self.final, self.castle_type, self.promo)


    ## Comparison Methods
    def __eq__(self, other:"Move") -> bool:

        '''
        Override the usual equals operator to return True if the side, start, final, castle_type and promo \
        attributes of 2 Move instances are the same.
        '''
        for key in self.__dict__.keys():
            if self.__dict__[key] != other.__dict__[key]:
                return False
        return True


class Board:

    '''
    Custom DataType used to represent a chessboard position.
    Contains:
        - Position of all pieces (dict)
        - Castling status/availability
        - King cells
        - Check status
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

    # piece types that threaten a position from a given direction
    with open(var_folder + threats_name, 'r') as f:
        threats = eval(f.read())

    # conversion of castling type symbol to rook cell
    castle_to_rook_cell = {-5:21, -6:28, 5:91, 6:98}

    # index of slider pieces that are threats from certain directions
    slider_threats = {-11:[3, 5], -10:[4, 5], -9:[3, 5], -1:[4, 5], 1:[4, 5], 9:[3, 5], 10:[4, 5], 11:[3, 5]}

    # persistance files
    data_folder = "C:/Users/lenovo/Desktop/Coding/VSC Projects/Chess_App/data/"
    save_file = "save.txt"


    ## Instance Initialization
    def __init__(self, side_to_move:int, dict_position:dict, castle_status:dict = {-5:True, -6:True, 5:True, 6:True}, stalemate_counter=0) -> None:

        '''
        Initialize Board DataType with dict.
        '''
        
        self.side_to_move = side_to_move
        self.dict = dict_position
        self.castle_status = castle_status
        self.find_king()
        self.add_check_status()
        self.legal = set()
        self.stalemate_counter = stalemate_counter
    
    @classmethod
    def from_arr(cls, arr:nparray, castle_status:dict = {-5:True, -6:True, 5:True, 6:True}, stalemate_counter=0) -> "Board":

        '''
        Initializing Board instance with np.ndarray.
        '''

        return cls(arr_to_dict(arr), castle_status, stalemate_counter)

    @classmethod
    def from_file(cls, filename:str = None) -> "Board":
        
        '''
        Load board from text file.
        '''

        if filename == None:
            filename = cls.save_file

        try:
            with open(cls.data_folder + cls.save_file, 'r') as f:
                pos_dict, castle_status, stalemate_counter = eval(f.read())
        except FileNotFoundError:
            return "Save file is not found"
        except:
            return "Unknown Error Occured."

        return cls(pos_dict, castle_status, stalemate_counter)

    def copy(self) -> "Board":

        '''
        Returns a copy of the Board instance.
        '''

        return deepcopy(self)


    ## Conversion Methods
    def to_arr(self) -> nparray: 

        '''
        Returns the board position as a np.ndarray.
        '''

        return dict_to_arr(self.dict)


    ## Display Methods
    def pretty_print(self) -> str:
        
        '''
        Print board position and castle status prettily

        Print format:
        Board (as array for now) (add row and column numbers later on)
        Castle status explained with names for each castle type
        '''
        
        output_str = str(self.to_arr()) + \
            f'\nCastle Status:\n  Black Queenside: {self.castle_status[21]}\n        Kingside: {self.castle_status[28]}' + \
            f'\n  White Queenside: {self.castle_status[91]}\n        Kingside: {self.castle_status[98]}' 

    def __repr__(self):
        
        '''
        Print method. Prints the board position and castle status.
        '''
        
        return str(self.to_arr()) + f'\n{self.castle_status.values()}'

    def info(self, show=True):

        '''
        Prints all relevant information about the Board object.

        Info displayed:
            - position
            - castle_status
            - check_status
            - legal_moves
        '''

        output = str(self.to_arr()) + \
            f'\nCastle Status: {self.castle_status.values()}' + \
            f'\nCheck Status: {self.check}' + \
            f'\nLegal Moves:\n'
        
        for move in self.legal:
            output += f'  {move.info(show=False)}'

        if show:
            print(output)
        else:
            return output


    ## Add Attributes
    def find_king(self) -> None:

        '''
        Gets the cell of the kings for both sides and save it as an dictionary (instance attribute) king_pos.
        '''

        self.king_pos = {
            -1: list(self.dict.keys())[list(self.dict.values()).index(-6)], 
            1: list(self.dict.keys())[list(self.dict.values()).index(6)]
        }

    def add_check_status(self) -> None:
        
        '''
        See if the either side is under check and save the check status for both sides
        '''

        self.check = {
            -1: indicator.check(self, -1),
            1: indicator.check(self, 1)
        }

    def add_legal(self, move:Move) -> None:

        '''
        Add a single legal move to the Board's collection of legal moves.
        '''
        
        self.legal.add(move)


    ## Move Methods
    def move(self, move:Move, update=True) -> "Board":

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
        if update:
            self.update_castle(move)
            self.update_check()
            self.find_king()
            self.legal = set()
            self.save()

        return self

    def move_copy(self, move:Move, update=True) -> "Board":

        '''
        Spawns a new Board object that contains the position after the given move is made.
        The current Board instance is not affected.
        '''

        new_board = self.copy()

        return new_board.move(move, update)


    ## Update Methods
    def update_castle(self, move:Move) -> None:
        
        '''
        Checks the move made and edits the castle status accordingly
        '''

        # if castling was not done
        if move.castle_type == 0:
            # if rooks moved from initial cell or rook is captured
            rook_to_castle_type = {21:-5, 28:-6, 91:5, 98:6}
            if move.start in rook_to_castle_type:
                self.castle_status[rook_to_castle_type[move.start]] = False
            elif move.final in rook_to_castle_type:
                self.castle_status[rook_to_castle_type[move.final]] = False
            # if king moved from initial cell
            elif move.start == 25:
                self.castle_status[-5], self.castle_status[-6] = False, False
            elif move.start == 95:
                self.castle_status[5], self.castle_status[6] = False, False

        # if castling was done
        else:
            if move.castle_type <= 2:
                self.castle_status[1], self.castle_status[2] = False, False
            else:
                self.castle_status[3], self.castle_status[4] = False, False

    def update_check(self) -> None:
        
        '''
        Updates the check_status for both sides.
        '''
        
        for side in [-1, 1]:
            self.check[side] = indicator.check(self, side)

    def update_counter(self, move:Move) -> None:

        '''
        Updates the stalemate counter.

        Resets the counter to 0 if a capture has been made or a pawn has been moved.
        Increments the counter by 1 otherwise.

        If the counter reaches 50, stalemate has been achieved.
        '''

        move.add_board(self)
        move_info = move.info(show=False)
        # if pawn is moved or a piece is captured
        if move_info[-2] == 1 or move_info in set([-1, -2, -3, -4, -5, -6, 1, 2, 3, 4, 5, 6]):
            self.stalemate_counter = 0
        else:
            self.stalemate_counter += 1


    ## Persistance Methods
    def save(self, filename:str = None) -> None:
        
        '''
        Save board information (position and castle_status) as a dict in a text file.

        Optional input: filename -- file name to save the board
        '''
        
        if filename == None:
            filename = self.save_file

        with open(self.data_folder + filename, 'w') as f:
            f.write(str((self.dict, self.castle_status)))