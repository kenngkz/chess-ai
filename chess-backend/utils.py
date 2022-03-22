'''
Utility functions
'''

import numpy as np
from typing import Union

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

def parse_fen(self, fen):
    ''' Parses fen notation and return a obs tuple '''
    pass