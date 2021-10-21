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

import itertools
from typing import Any, Iterator, List, Tuple
import indicator
import get

# --------------------------------------------------------------------
'''
Function definitions
'''


def leaper(board:"Board", cell:int, side:int, directions:List[int]) -> Iterator[int]:

    '''
    Yields the leaper side, cell and destinations in a given set of directions one at a time.

    Leapers are pieces that jump in a given direction once without passing through the cells in between
    '''
    
    for move_dir in directions:
        new_cell = cell + move_dir
        if indicator.traversible(board, new_cell, side):
            yield side, cell, new_cell


def slider(board:"Board", cell:int, side:int, directions:List[int]) -> Iterator[int]:

    '''
    Yields the slider side, cell and destinations in a given set of directions one at a time.

    Sliders are pieces that slide along one direction until it hits another object/goes off board
    '''

    # create a vector of displacements from givven cell to all other cells in the movement range of the piece.
        # each direction is repeated 8 times (in total) and multiplied to generate the movement range
    distances = [0, 1, 2, 3, 4, 5, 6, 7]
    direction_chain = itertools.chain.from_iterable(itertools.repeat(direction, 8) for direction in directions)
    drct_vector = (dist*drct for dist, drct in zip(distances*len(directions), direction_chain))
    
    # skip is the variable that controls whether the considered cell is previously blocked by ally/enemy piece
    skip = False
    for drct in drct_vector:
        if skip:
            continue
        elif drct in directions:
            skip = False
        
        new_cell = cell + drct
        occupant_side = get.side(board, new_cell)

        if occupant_side*side != 0:
            skip = True
        if occupant_side*side <= 0:
            yield side, cell, new_cell


def pawn(board:"Board", cell:int, side:int, dummy_var:Any = None) -> Iterator[int]:
    
    '''
    Yields the prelegal pawn side, cell, destinations and promotion value for a pawn in a given cell.
    '''
    
    # capture moves
    capture_directions = {-1:[11, 9], 1:[-11, -9]}[side]
    for direction in capture_directions:
        new_cell = cell + direction
        occupant_side = get.side(board, new_cell)
        if occupant_side == -side:
            yield side, cell, new_cell, 0, 0
        
    # slider moves
    new_cell = cell + 10*-side
    if get.side(board, new_cell) == 0:
        jump_cell = new_cell + 10*-side
        jump_allowed = cell//10==8 if side == 1 else cell//10==3
        promo_allowed = cell//10==3 if side == 1 else cell//8
        
        
        if promo_allowed:
            for promo_val in [2, 3, 4, 5]:
                yield side, cell, new_cell, 0, promo_val
        else:
            yield side, cell, new_cell, 0, 0
        
        if get.side(board, jump_cell) == 0 and jump_allowed:
            yield side, cell, jump_cell, 0, 0



def board(board:"Board", side:int) -> Iterator[Tuple[int]]:

    '''
    Yields the prelegal moves (as Move objects) for all pieces of a particular side

    Order of Moves (reversed for black):
        - pawn (promo, capture, slider_moves)
        - knight
        - bishop
        - rook
        - queen
        - king
        - castling

    To do: implement piece sorting for black
    '''
    
    # define what function to be used for all pieces
    index_to_func = {1:pawn, -1:pawn, 2:leaper, -2:leaper, 3:slider, -3:slider, 4:slider, -4:slider, 
                     5:slider, -5:slider, 6:leaper, -6:leaper}

    prelegal_gens = []
    for cell, index in board.dict.items():
        if indicator.same_side(index, side):
            gen = index_to_func[index](board, cell, side, board.piece_dirs[index])
            prelegal_gens.append(gen)
    
    prelegal_destinations = itertools.chain.from_iterable(prelegal_gens)

    for args in prelegal_destinations:
        yield args

    # castling
    if not board.check[side]:
        # lists the cells to check for a particular side and castle type
            # the first list is the cells to check for threats
            # the second list is the cells to check for occupants
        castling_cells = {-1:{-5:[[23, 24], [22, 23, 24]], -6:[[26, 27], [26, 27]]}, 1:{5:[[93, 94], [92, 93, 94]], 6:[[96, 97], [96, 97]]}}[side]
        for castle_type, check_cells in castling_cells.items():
            # board castling status must be True for castling to be allowed
            if board.castle_status[castle_type] and sum([get.index(board, check_cell)==0 for check_cell in check_cells[1]]) == 2 and sum([indicator.threatened(board, side, check_cell) for check_cell in check_cells[0]]) == 0:
                yield side, 0, 0, castle_type