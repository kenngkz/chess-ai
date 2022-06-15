'''
Utility functions
'''

from typing import Union
import chess as pychess
import numpy as np

import constants

###################
### Basic Utils ###
###################

def add(v1, v2):
    ''' Element-wise vector addition '''
    return [a+b for a, b in zip(v1, v2)]

def sign(num:Union[int, None]) -> int:
    ''' Returns the sign of the input. Input can be an integer or None. '''
    # Returns 1 if num > 0
    # Returns -1 if num < 0
    # Returns 0 if num == 0 or num == None
    if num != None:
        if num > 0:
            return 1
        elif num < 0:
            return -1
    return 0

def path_join(*args):
    path = ""
    for arg in args:
        if arg[-1] == '\\':
            arg = arg[:-1]
        if arg[-1] != '/':
            arg += '/'
        path += arg
    return path[:-1]

##############################
###    Notation Parsing    ###
##############################

def parse_fen(fen:str):
    '''
    Parses fen notation and return a obs numpy array.
    Obs tuple indices: 
        - 0: player to move. 1 if white 0 if black
        - 1 - 64: index of pieces in each cell on the board
        - 65 - 68: whether castling is allowed (1 if allowed else 0). order: white kingside, white queenside, black kingside, black queenside
        - 69: whether player_to_move is under check (1 if under check else 0)
    '''
    obs = np.zeros(70, dtype=np.int16)
    sections = fen.split(" ")

    # player to move
    if sections[1] == "w":
        obs[0] = 1
    else:
        obs[0] = -1

    # board section of fen
    index = 1
    for char in sections[0]:
        if char == "/":
            pass
        elif char.isnumeric():
            index += int(char)
        elif char in constants.symbol_piece_index_mapping:
            obs[index] = constants.symbol_piece_index_mapping[char]
            index += 1
        else:
            raise KeyError(f"Char {char} in board section of fen not recognized")

    # castling status
    if sections[2] == "-":
        pass
    else:
        if "K" in sections[2]:
            obs[65] = 1
        if "Q" in sections[2]:
            obs[66] = 1
        if "k" in sections[2]:
            obs[67] = 1
        if "q" in sections[2]:
            obs[68] = 1

    # under_check status
    board = pychess.Board(fen)
    obs[69] = int(board.is_check())
    
    return obs