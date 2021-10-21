'''
Conversion of board information to vector representation.

The vector used will be one-hot: can only take values of 0 or 1.

Information Indexes:
    0 - 4031 : Regular Moves
    4032 - 4035 : Castling Moves
    4036 - 4099 : Promotion Moves
    4100 - 4931 : Position
    4932 - 4935 : Castle Status
'''

# --------------------------------------------------------------------
'''
Imports
'''

import numpy as np
import legal

# --------------------------------------------------------------------
'''
Function definitions
'''


def move_encode(move:"Move") -> int:
    
    '''
    Returns the index of a given move in the vector encoding.

    Regular moves: 0 - 4031
    Castling: 4032 - 4035
    Promotion: 4036 - 4099

    Output vector length: 4100
    '''
    # intercepts for different types of moves
    castle_bias = 4032
    promo_bias = 4036
    regular_bias = -1

    # castle moves
    if move.castle_type != 0:
        castle_type_to_raw_index = {-5:0, -6:1, 5:2, 6:3}
        return castle_bias +castle_type_to_raw_index[move.castle_type]

    # promotion moves
    elif move.promo != 0:
        side = 0 if move.final//10 == 2 else 1  # 0 if white pawn promotion, 1 if black pawn promotion
        col = move.final%10 - 1  # 0 - 8
        promo_index = move.promo - 2  # 0 - 3
        return promo_bias + promo_index + col*4 + side*32

    # regular moves
    else:
        # raw_index is calculated based on all combinations of 2 cells that can be repeated (eg. 21->21, 22->22 included)
            # the raw_index is then shifted as the repeating combinations are removed (shifted by //65+1 steps)
        raw_index = move.final%10 - 1 + (move.final//10 - 2)*8 + (move.start%10 - 1) * 64 + (move.start//10 - 2) * 512
        return regular_bias + raw_index - raw_index//65


def position_to_vec(board:"Board") -> np.ndarray:

    '''
    Returns the board position and castle status information as a tuple (one-hot).

    Position: 0 - 831
    Castle: 832 - 835

    Output vector length: 836
    '''
    
    vec = np.zeros(836)
    castle_bias = 832
    possible_pieces = [0, 1, 2, 3, 4, 5, 6, -1, -2, -3, -4, -5, -6]

    # position encoding
    for cell_num in range(64):
        # get the piece index of the cell
        cell = board.valid_cells[cell_num]
        if cell in board.dict:
            index = possible_pieces.index(board.dict[cell])
        else:
            index = 0
        # convert the piece index to the corresponding index in the vector
        vec_index = cell_num*13 + index
        vec[vec_index] = 1

    # castle_status encoding
    for castle_type, castle_status in board.castle_status.items():
        type_to_index = {-5:0, -6:1, 5:2, 6:3}
        vec[castle_bias+type_to_index[castle_type]] = int(castle_status)

    return vec


def board_to_vec(board:"Board") -> np.ndarray:

    '''
    Converts a given board object to an array. Encoded information will be legal moves, position and castle status.
    '''

    legal_moves = legal.board(board, board.side_to_move)

    set_to_one = set()
    for move in legal_moves:
        board.add_legal(move)
        set_to_one.add(move_encode(move))

    move_vec = np.zeros(4100)

    for index in set_to_one:
        move_vec[index] = 1

    position_vec = position_to_vec(board)

    return np.r_[move_vec, position_vec]
    
    