##### GET FUNCTIONS #####
'''Returns information about the board'''

# IMPORTS
import numpy as np

# GLOBAL VAR
# define the cells that are on board as valid cells
with open('done/vars/valid_cells.txt', 'r') as f:
    valid_cells = eval(f.read())

### FUNCTION DEFINITIONS ###

def get_piece(board:dict, cell:int) -> int or None:
    '''
    Returns the piece code of the piece in a given cell. 
    Returns None if given cell is off board
    '''
    if cell in valid_cells:  # valid_cells is global var
        if cell in board:
            return board[cell]
        else:
            return 0


def get_occupant(board:dict, cell:int) -> int or None:
    '''
    Returns the side of the piece in a given cell. 
    Returns None if given cell is off board
    '''
    if cell in valid_cells:  # valid_cells is global var
        if cell in board:
            return np.sign(board[cell])
        else:
            return 0