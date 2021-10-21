'''
Application endpoints

Functions:Endpoints >>
    - move: '/move'
    - get_board: '/get/board'
    - get_legal: '/get/legal'
    - get_gamestate: '/get/gamestate'
    - reset: '/reset'
    - set: '/set'
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
from app_functions import move_app, save_app, get_app, paracheck

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
def move(move:Dict[str:int]) -> Tuple[int]: 

    '''
    Make a move on the given board and return the new board after the move is made.
    Also returns the castle status as the last 4 integers in the 2D list.

    Inputs (Request parameters):
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
    parameters = ["move"]
    for name in parameters:
        locals()[name] = request.args.get(name)

    # Check that all parameters are passed
    required_parameters = parameters
    paracheck.required(required_parameters)

    new_board, castle_status = move_app.main(move)

    return new_board, castle_status


@app.route('/get/board', method=["GET"])
def get_board():

    '''
    Gets the board position and castle status from the save file and returns both inside of a tuple.

    Output: 
        - Tuple(board, castle_status)
            - board : Array[int] with shape (8, 8) representing chessboard position
            - castle_status : Dict[int:bool] representing castle status
    '''
    
    return get_app.board()


@app.route('/get/legal', method=["GET"])
def get_legal(side:int):
    
    '''
    Gets all legal moves for a given side and returns the moves as a list of tuples. The board position and castle status is taken from save file.

    Input:
        - side: int -- ChooseOne[-1, 1]

    Output: 
        - List of moves in tuple representation
            - Tuple(side, start_cell, final_cell, castle_type, promo) -- all items in tuple are of type int
    '''

    # Parameters
    parameters = ["side"]
    for name in parameters:
        locals()[name] = request.args.get(name)

    # Parameter Checking
    required_parameters = parameters
    paracheck.required(required_parameters)

    # Return all legal moves for the given side
    return get_app.legal(side)

@app.route('/get/gamestate', method=["GET"])
def get_gamestate():

    '''
    Gets the check, checkmate and stalemate status for both sides for the board in the save file.

    Output: List[black_check, white_check, black_checkmated, white_checkmated, stalemate]
        - black_check : bool -- True if black if under check
        - white_check : bool -- True if white is under check
        - black_checkmated : bool -- True if white has won the game
        - white_checkmated : bool -- True if black has won the game
        - stalemate : bool -- True if a stalemate/tie has been achieved
    '''

    return get_app.game_state()


@app.route('/reset', method=["POST"])
def reset():

    '''
    Resets the board position and castle status in the save file.
    '''

    return save_app.reset()


@app.route('/set', method=["POST"])
def set(arr:"np.ndarray", castle:Dict[str:bool], filename:str = None):

    '''
    Sets the board position and castle status in the save file to the provided values in the parameters

    Parameters:
        - arr : 2D array with shape (8, 8) representing the board position
        - castle : dict with format {-5:bool, -6:bool, 5:bool, 6:bool}
        - filename (optional) : str as the filename to save the position and castle_status
    '''

    # Parameters
    parameters = set(["arr", "castle", "filename"])
    for name in parameters:
        locals()[name] = request.args.get(name)

    # Parameter Checking
    required_parameters = set(["arr", "castle"])
    paracheck.required(required_parameters)

    # set the save file to the given values
    return save_app.set(arr, castle, filename)




# --------------------------------------------------------------------
'''
Notes
'''

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
