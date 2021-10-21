'''
Get functions to retrieve information from the board. 

Functions:
    - index
    - side
    - first_in_direction
    - between
    - game_state
'''

# --------------------------------------------------------------------
'''
Imports
'''
# --------------------------------------------------------------------

from typing import Union, List
from convert import sign
import legal

# --------------------------------------------------------------------
'''
Function definitions
'''
# --------------------------------------------------------------------

def index(board:"Board", cell:int) -> Union[None, int]:

    '''
    Get the piece in the given cell.

    Return the index (piece number) of the piece in the given cell
    If the given cell is not on the board, returns None
    If the given cell is empty, returns 0
    '''

    if cell in board.valid_cells:
        if cell in board.dict:
            return board.dict[cell]
        else:
            return 0

def side(board:"Board", cell:int) -> Union[None, int]:

    '''
    Get the side of the piece in the given cell.

    Return the sign of the index of the piece in the given cell
    { 1 : white, -1 : black }
    If the given cell is not on the board, returns None
    If the given cell is empty, returns 0
    '''

    # This function is written seperately instead of directly applying np.sign() to index() for performance reasons

    if cell in board.valid_cells:
        if cell in board.dict:
            return sign(board.dict[cell])
        else:
            return 0


# used in indicator.legal
def first_in_direction(board:"Board", cell:int, direction:int, max_distance:int) -> int:
    
    '''
    Returns the first piece in a given direction from a given cell.
    '''
    
    for _ in range(max_distance):
        cell = cell + direction
        piece = index(board, cell)
        if piece != 0:
            return piece
    return 0


# used in indicator.legal
def between(board:"Board", start_cell:int, final_cell:int, direction:int) -> List[int]:

    '''
    Returns an ordered list of all the pieces in between 2 cells.
    Direction is required to simplify calculations.
    '''
    
    pieces_in_between = []
    cell = start_cell
    for _ in range((final_cell-start_cell) // direction - 1):
        cell += direction
        pieces_in_between.append(index(board, cell))
    return pieces_in_between


def game_state(board) -> List[bool]:

    '''
    Returns the game state for the given board.
    Game state information concerns the checkmate status for both sides and the stalemate status.

    Output: List[black_checkmated, white_checkmated, stalemate]
        - black_checkmated : bool  -- white wins
        - white_checkmated : bool  -- black wins
        - stalemate : bool
    '''

    gamestate = [False, False, False]

    # black checkmated
    black_legal = len(set(legal.board(board, -1)))

    if board.check[-1] and black_legal != 0:
        gamestate[0] = True

    # white checkmated
    white_legal = len(set(legal.board(board, 1)))
    if board.check[1] and white_legal != 0:
        gamestate[1] = True

    # stalemate
    if (black_legal==0 and board.check[-1]) or (white_legal==0 and board.check[1]) or board.stalemate_counter==50:
        gamestate[2] = True

    return gamestate
