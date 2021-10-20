'''
move() function to be used in app.py
'''

# --------------------------------------------------------------------
'''
Imports
'''

from numpy import array
from typing import Tuple, Dict, List
import chess
from chess.dtype import Move, Board

# --------------------------------------------------------------------
'''
Imported Variables (?)
'''


# --------------------------------------------------------------------
'''
Main function
'''

def main(board:List[int], castle:Dict[int:bool], move:Dict[str:int]) -> Tuple[int]: 

    '''
    Main function to be used in the move() function in the chess application. Takes in a given board position and performs the given move. 
    '''
    
    # Parameter checking
    # move_coor
    if sum([item in move for item in ['side', 'start_cell', 'final_cell']]) != 3:
        return "Input Parameter Error: move. Required keys not provided.\nmove_coor is a dictionary that expects keys 'side', \
            'start_cell' and 'final_cell'.\nOptional keys in move_coor are 'castle' or 'promo'"

    # board
    arr = array(board) 
    if arr.shape != (8, 8):
        return f"Input Parameter Error: board. Wrong input shape.\nboard input expected shape (8, 8) but recieved shape {arr.shape}"

    # castle_status
    if sum([symbol in castle for symbol in [-5, -6, 5, 6]]) != 4:
        return "Input Parameter Error: castle. Required keys not provided.\ncastle_status is a dictionary that expects keys -5, -6, 5 and 6"

    # prepare Board parameters
    arr = array(board)
    move = Move(**move)  # move (from input) is overwritten here to change from dict to Move object

    legal_moves = list(chess.legal.board(board, move.side))
    if move not in legal_moves:
        move.add_board(board)
        return f"Move {move.info(show=False)} is not legal."

    chessboard = Board(arr, castle)
    chessboard.move(move)

    return chessboard.to_arr(), chessboard.castle_status