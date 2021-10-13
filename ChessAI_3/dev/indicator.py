'''
Indicator functions that check for the status of different board positions/cells. 
These functions return Booleans or Integers.
 - traversible
 - check
 - legal
'''


# --------------------------------------------------------------------
'''
Imports
'''

from func.convert import sign
import get


# --------------------------------------------------------------------
'''
Function definitions
'''


def traversible(board:"Board", cell:int, side:int) -> bool:
    '''
    Boolen indicator to check if a given cell is occupiable by a given side.

    Returns True if cell is empty or contains an enemy
    Returns False if given cell contains ally or is not on the board
    '''
    if cell in board.valid_cells:
        if cell in board.dict:
            if sign(board.dict[cell]) == -side:
                return True
            return False
        return True
    return False


def check(board:"Board", side:int) -> bool:
    '''
    Boolean indicator to check if a given side is under check for a board position.

    Returns True if the king of the side is under check
    Returns False if the king of the side is not under check
    '''
    
    for lst in board.threats[side]:
        for direction, indexes in lst:
            piece = get.index(board, board.king_pos[side]+direction)
            if piece in indexes:
                return True
            elif piece != 0:
                break
    return False



def legal(board:"Board", move:"Move") -> bool:

    '''
    Boolean indicator to check if a given move is legal.
    Assumes that the given move is prelegal.

    Returns True if move is legal
    Returns False is move is not legal
    '''

    # if check: pseudomove
    if board.check[move.side]:
        new_board = board.move_copy(move)
        return check(new_board, move.side)

    # difference in cell number from moving piece to king. represents the direction + distance from piece to king
    king_to_piece = move.start - board.king_pos[move.side]
    for direction in [-11, -10, -9, -1, 1, 9, 10, 11]:
        if king_to_piece % direction == 0:
            if king_to_piece // direction in list(range(1, 8)):
                piece_behind = get.first_in_direction(board, move.start, direction, 6)
                if piece_behind == -move.side * board.slider_threats[direction]:
                    return False
    return True