'''
Utility functions
'''

import numpy as np
from typing import Union
import chess

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

############################
### Conversion Functions ###
############################

def arr_to_dict(arr) -> dict:
    ''' Converts a board position represented by an array into a dictionary representation '''
    output = {}
    for row in range(8):
        for col in range(8):
            if arr[row, col] != 0:
                output[21 + row*10 + col] = arr[row, col]
    return output

def dict_to_arr(dict) -> np.array:
    ''' Converts a board position represented by a dictionary into an array representation '''
    output = np.zeros((8, 8), dtype=int)
    for cell, index in dict.items():
        output[(cell-21)//10, (cell-21)%10] = index
    return output

#########################
### Display Functions ###
#########################

def print_move(move:"Move", board:"Board"):
    init_params = move.__repr__()
    if move.start == 0:
        movement = f'{constants.castle_names[move.castle_type]} Castle'
    else:
        movement = f'{board.occupant(move.start).name} -> {board.occupant_name(move.final).name}'
    print(init_params, movement)

##########################
###    Optimization    ###
##########################

def dict_to_tuple(dic) -> tuple:
    ''' Converts dict board position to tuple representation '''
    tup = (0 for _ in len(64))
    for cell, val in dic.items():
        tup[constants.cell_mapping[cell]] = val
    return tup

def enhash_cell(padCell:int) -> int:
    ''' Converts padCell number (21-98) to hashCell (0-63) '''
    return constants.padCell_hashCell_mapping[padCell]

def dehash_cell(hashCell:int) -> int:
    ''' Converts hashCell (0-63) to padCell (21-98) '''
    return constants.hashCell_padCell_mapping[hashCell]

def pad_to_usercell(padCell:int) -> str:
    return constants.padCell_userCell_mapping[padCell]

##############################
###    Notation Parsing    ###
##############################

def parse_fen(fen:str):
    '''
    Parses fen notation and return a obs tuple.

    Obs tuple indices: 
        - 0 - 63: index of pieces in each cell on the board
        - 64 - 67: whether castling is allowed (1 if allowed else 0). order: white kingside, white queenside, black kingside, black queenside
        - 65: player to move. 1 if white 0 if black
        - 66: whether white under check (1 if under check else 0)
        - 67: whether black under check (1 if under check else 0)
    '''
    tup = tuple(0 for _ in range(66))
    sections = fen.split(" ")

    # board section of fen
    index = 0
    for char in sections[0]:
        if char == "/":
            index += 1
        elif char.isnumeric():
            index += int(char)
        elif char in constants.symbol_piece_index_mapping:
            tup[index] = constants.symbol_piece_index_mapping[char]
            index += 1
        else:
            raise KeyError(f"Char {char} in board section of fen not recognized")
        
    # player to move
    if sections[1] == "w":
        tup[65] = 1

    # castling status
    if sections[2] == "-":
        pass
    else:
        if "K" in sections[2]:
            tup[64] = 1
        if "Q" in sections[2]:
            tup[65] = 1
        if "k" in sections[2]:
            tup[66] = 1
        if "q" in sections[2]:
            tup[67] = 1

    # check status
    board = chess.Board(fen)
    check_status_combinations = {
        (True, True, False):(1, 0),
        (True, False, True):(0, 1),
        (True, False, False):(0, 0),
        (False, True, False):(0, 1),
        (False, False, True):(1, 0),
        (False, False, False):(0, 0)
    }
    check_status = (board.turn, board.is_check(), None)
    board.turn = not board.turn
    check_status[-1] = board.is_check()
    check_status = check_status_combinations[check_status]
    tup[-2], tup[-1] = check_status[0], check_status[1]
        
    return tup