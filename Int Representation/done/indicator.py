##### INDICATOR FUNCTIONS #####
''' Returns booleans when called'''

# IMPORTS
import numpy as np

# GLOBAL VAR
# define the cells that are on board as valid cells
with open('done/vars/valid_cells.txt', 'r') as f:
    valid_cells = eval(f.read())

### FUNCTION DEFINITIONS ###

def is_opponent(board:dict, cell:int, side:int) -> int or None:
    '''
    Returns a boolean indicating whether the piece in a given cell is an opponent. 
    Returns None if given cell is off board
    '''
    if cell in valid_cells:
        if cell in board:
            if np.sign(board[cell]) == -side:
                return True
            return False
        return False


def is_traversible(board:dict, cell:int, side:int) -> int or None:
    '''
    Returns a boolean indicating whether the piece in a given cell is an opponent or empty cell. 
    Returns None if given cell is off board
    Returns True if given cell contains ally
    '''
    if cell in valid_cells:
        if cell in board:
            if np.sign(board[cell]) == -side:
                return True
            return False
        return True
    return False