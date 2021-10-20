# --------------------------------------------------------------------
'''
Imports
'''
# --------------------------------------------------------------------

from typing import Union, Tuple, List
from convert import sign

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


# dont think i need this
def pieces_in_direction(board:"Board", cell:int, direction:int, max_distance:int, n_pieces:int=2) -> Tuple[int]:
    
    '''
    Returns the first 2 pieces in a given direction from a given cell.
    '''
    output_pieces = (None, None)
    n_pieces_found = 0
    for _ in range(max_distance):
        cell = cell + direction
        piece = index(board, cell)
        if piece != 0:
            output_pieces[n_pieces_found] = piece
            n_pieces_found += 1
        if n_pieces_found == n_pieces:
            return output_pieces