'''
Legal move generation for the entire board

Produces a generator. Does not immediately calculate legal moves when called.
'''


# --------------------------------------------------------------------
'''
Imports
'''

from dtype import Board, Move
import indicator
import prelegal

# --------------------------------------------------------------------
'''
Function definitions
'''

def board(board:Board, side:int):
    '''
    Yields the legal moves available for a given side in a given board position

    To improve alpha-beta pruning tree search, the order of pieces is pawn, knight, bishop, rook, queen, king
    '''
    
    # loop through prelegal moves and run indicator.legal(move), yield if True
    for move_data in prelegal.board(board, side):
        move = Move(*move_data)
        if indicator.legal(board, move):
            yield move