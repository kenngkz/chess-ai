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
Main function
'''

def main(move:Dict[str:int]) -> Tuple[int]: 

    '''
    Main function to be used in the move() function in the chess application. 
    '''
    
    # Parameter checking
    # move_coor
    if sum([item in move for item in ['side', 'start_cell', 'final_cell']]) != 3:
        return "Input Parameter Error: move. Required keys not provided.\nmove_coor is a dictionary that expects keys 'side', \
            'start_cell' and 'final_cell'.\nOptional keys in move_coor are 'castle' or 'promo'"

    # Initilize Board object
    board = Board.from_file()
            
    # Initialize Move object
    move = Move(**move)  # move (from input) is overwritten here to change from dict to Move object

    legal_moves = list(chess.legal.board(board, move.side))
    if move not in legal_moves:
        move.add_board(board)
        return f"Move {move.info(show=False)} is not legal."

    board.move(move)

    return board.to_arr(), board.castle_status