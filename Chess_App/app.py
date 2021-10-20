'''
Application endpoints

Functions:Endpoints >>
    - move: '/move'
    - legal_moves: '/legalmoves'
    - is_check/is_game_end:
    - ai_move: 
    - (?) probability of ai winning <- can be added to ai_move
    - (?) logging
'''

# --------------------------------------------------------------------
'''
Imports
'''

from flask import Flask, request
from typing import Tuple, Dict
from app_functions import move_app

# --------------------------------------------------------------------
'''
Application
'''

app = Flask(__name__)

# --------------------------------------------------------------------
'''
Endpoints
'''

@app.route('/move', method=["GET", "POST"])
def move(board:list, castle:Dict[int:bool], move:Dict[str:int]) -> Tuple[int]: 

    '''
    Make a move on the given board and return the new board after the move is made.
    Also returns the castle status as the last 4 integers in the 2D list.

    Inputs (Request parameters):
        - board: 2D list of the positions of all pieces on the board
        - castle: Dict{-5:Boolean, -6:Boolean, 5:Boolean, 6:Boolean}. All keys are required
        - move: Dict{'side':ChooseOne[-1, 1], 'start_cell':int, 'final_cell':int, \
            'castle' (optional):ChooseOne[0, -5, -6, 5, 6], 'promo' (optional):ChooseOne[0, 2, 3, 4, 5]}

    Output:
        If move is legal:
            Tuple(board, castle_status)
            - board: 2D list of the new positions of all pieces on the board
            - castle_status: Dict{-5:Boolean, -6:Boolean, 5:Boolean, 6:Boolean}
        If move is not legal:
            Error message returned
    '''

    # Parameters
    parameters = ["board", "castle", "move"]

    for name in parameters:
        locals()[name] = request.args.get(name)

    # Check that all parameters are passed
    for name in parameters:

        val = locals()[name]

        if val == None:
            return f"Input Parameter Error: {name}. Parameter Not Found.\nThe parameter was not found in the submitted request."

    new_board, castle_status = move_app.main(board, castle, move)

    return new_board, castle_status
    

# # Get the position of all pieces on the chessboard
# @app.route('/get_board')
# def get_board():
#     return chessboard.board

# # Reset the game
# @app.route('/reset')
# def reset():
#     chessboard.reset()
#     return 'Reset complete'



# Required API endpoints
# -- ai_move <ai_side, board>  (return new_board)
# -- which moves are legal <piece, board>  (return legal end_coor)
# -- is_check + is_game_end <board> (return some kind of vector/list/dict)
# -?- probability of winning

# errors? request failed error code 401
# logging?