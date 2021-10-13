'''
Prelegal move generation for the types of pieces (leaper & slider) and board.

Produces a generator. Does not immediately calculate prelegal moves when called.

leaper(), slider() and pawn() produce prelegal destinations (final cell number: int)
board() produces Move object
'''


# --------------------------------------------------------------------
'''
Imports
'''

from typing import Any, Iterator, List
from dtype import Move
import indicator
import get

# --------------------------------------------------------------------
'''
Function definitions
'''


def leaper(board:"Board", cell:int, side:int, directions:List[int]) -> Iterator[int]:

    '''
    Yields the leaper destinations in a given set of directions one at a time.

    Leapers are pieces that jump in a given direction once without passing through the cells in between
    '''
    
    for move_dir in directions:
        new_cell = cell + move_dir
        if indicator.traversible(board, new_cell, side):
            yield new_cell


def slider(board:"Board", cell:int, side:int, directions:List[int]) -> Iterator[int]:

    '''
    Yields the slider destinations in a given set of directions one at a time.

    Sliders are pieces that slide along one direction until it hits another object/goes off board
    '''

    for move_dir in directions:
        new_cell = cell
        for _ in range(8):
            new_cell += move_dir
            occupant = get.occupant(board, cell)
            if occupant == 0:
                yield new_cell
            elif occupant == -side:
                yield new_cell
                break
            else:
                break

def pawn(board:"Board", cell:int, side:int, dummy_var:Any = None) -> Iterator[int]:
    
    '''
    Yields the prelegal pawn destinations for a pawn in a given cell.
    '''
    
    # capture moves
    capture_directions = {-1:[-11, -9], 1:[11, 9]}[side]
    for direction in capture_directions:
        new_cell = cell + direction
        occupant_side = get.side(board, new_cell)
        if occupant_side == -side:
            yield new_cell
        
    # slider moves
    new_cell = cell + 10*-side
    if get.side(board, new_cell) == 0:
        jump_cell = new_cell + 10*-side
        jump_allowed = cell//10==8 if side == 1 else cell//10==3
        if get.side(board, jump_cell) == 0 and jump_allowed:
            yield jump_cell
        yield new_cell


def board(board:"Board", side:int) -> Iterator["Move"]:
    # get dict of all pieces on the relevent side with their cell numbers {piece_index:[cells]}
    pieces = {side:[], side*2:[], side*3:[], side*4:[], side*5:[], side*6: []}
    for index, cell in board.dict.items():
        if index >= side:
            pieces[index] += cell


    index_to_func = {1:pawn, -1:pawn, 2:leaper, -2:leaper, 3:slider, -3:slider, 4:slider, -4:slider, 
                     5:slider, -5:slider, 6:leaper, -6:leaper}
    for index, cells in pieces.items():
        func = index_to_func[index]
        for cell in cells:
            for direction in board.piece_dirs[index]:
                prelegal_dest_gen = func(board, cell, side, direction)
                for dest in prelegal_dest_gen:
                    # promotion is available
                    if (index == 1 and dest//10==9) or (index==-1 and dest//10==2):
                        for promo_value in [2, 3, 4, 5]:
                            yield Move(side, cell, dest, 0, promo_value)
                    else:
                        yield Move(side, cell, dest)
    
    # castling
    if not board.check[side] and # add more castling requirements