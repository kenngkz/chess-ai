'''
Functions used in the application to manage save files for Board.
'''

# --------------------------------------------------------------------
'''
Imports
'''

from chess import convert
from typing import Tuple, Dict
from numpy import ndarray as nparray

# --------------------------------------------------------------------
'''
Imported Variables File Names
'''

var_folder = '../chess/vars/'
ini_board_name = 'ini_board.txt'

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

def reset() -> None:
    
    '''
    Resets the save file to the initial position and castle status for the chessboard.
    '''

    # initial states
    with open(var_folder + ini_board_name, 'r') as f:
        ini_board = eval(f.read())
    ini_castle_status = {-5:True, -6:True, 5:True, 6:True}
    
    # overwrite save file
    with open(data_folder + save_file, 'w') as f:
        f.write(str((ini_board, ini_castle_status)))

    return "Reset complete."


def set(arr:nparray, castle:Dict[str:bool], filename:str = None) -> str:

    '''
    Sets the save file to a certain board position and castle status. Returns a success message if the edit is successful.
    '''
    
    if type(arr) != nparray:
        from numpy import array
        arr = array(arr)

    if arr.shape != (8, 8):
        return f"Input Parameter Error: board_arr. Invalid array shape.\nboard_arr expects array with shape (8, 8).\
            Got array with shape {arr.shape}"

    board_dict = convert.arr_to_dict(arr)

    if filename == None:
        filename = save_file

    with open(data_folder + filename, 'w') as f:
        f.write(str((board_dict, castle)))

    return f"Save file {filename} updated."