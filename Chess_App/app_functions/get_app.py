'''
Functions used in the application to retrieve information about the board saved in the save file.
'''

# --------------------------------------------------------------------
'''
Imports
'''

from chess import convert, legal, get
from chess.dtype import Board
from typing import Tuple, Dict, List
from numpy import ndarray as nparray


# --------------------------------------------------------------------
'''
Data Storage File Names
'''

data_folder = "../data/"
save_file = "save.txt"

# --------------------------------------------------------------------
'''
Function Definitions
'''

def board() -> Tuple[nparray, Dict[str:bool]]:
    
    '''
    Returns the position and castle status in the save file.
    '''

    # read board position and castle status from save file
    with open(data_folder + save_file, 'r') as f:
        board_dict, castle_status = eval(f.read())

    # convert dict position to np.ndarray
    board_arr = convert.dict_to_arr(board_dict)

    return board_arr, castle_status


def legal(side:int) -> List[Tuple[int]]:

    '''
    Returns a list containing all the legal moves available for a given side for the board in save file.

    Input:
        - side : int ->  -1 for black, 1 for white
    '''

    # Parameter Checking
    if side not in [-1, 1]:
        return "Input Parameter Error: side.\nside expects an integer which can be either -1 or 1.\n-1: black, 1: white"

    # load board from save file
    board = Board.from_file()

    # generator for legal moves of the given side
    legal_moves = legal.board(board, side)

    # add every move into a list (as a tuple) and return it
    output = []
    for move in legal_moves:
        output.append(move.to_tuple())

    return output

def check(side) -> bool:

    '''
    Returns the check status for a given side for the board in save file.

    Input:
        - side : int ->  -1 for black, 1 for white
    '''

    # Parameter Checking
    if side not in [-1, 1]:
        return "Input Parameter Error: side.\nside expects an integer which can be either -1 or 1.\n-1: black, 1: white"

    # load board from save file
    board = Board.from_file()

    return board.check[side]


def game_state() -> bool:

    '''
    Returns the game state for the board in save file. 
    Game state information includes check status for both sides and checkmate/stalemate status.

    Output: Tuple(black_check, white_check, black_checkmated, white_checkmated, stalemate)
        - black_check : bool -- True if black if under check
        - white_check : bool -- True if white is under check
        - black_checkmated : bool -- True if white has won the game
        - white_checkmated : bool -- True if black has won the game
        - stalemate : bool -- True if a stalemate/tie has been achieved
    '''

    # load board from save file
    board = Board.from_file()

    # checkmate and stalemate
    gamestate = get.game_state(board)

    # combine check, checkmate and stalemate status
    output = [board.check[-1], board.check[1]] + gamestate

    return output