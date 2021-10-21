'''
Conversion functions between different data types.

Functions:
    - position representation: np.ndarray to dict
    - position representation: dict to np.ndarray
    - integers: returns the sign of the integer. Returns 0 if input is None.
'''


# --------------------------------------------------------------------
'''
Imports
'''

import numpy as np
from typing import Union

# --------------------------------------------------------------------
'''
Function definitions
'''


def arr_to_dict(arr) -> dict:

    '''
    Converts a board position represented by an array into a dictionary representation
    '''

    output = {}
    for row in range(8):
        for col in range(8):
            if arr[row, col] != 0:
                output[21 + row*10 + col] = arr[row, col]
    return output

def dict_to_arr(dict) -> np.ndarray:

    '''
    Converts a board position represented by a dictionary into an array representation
    '''
    
    output = np.zeros((8, 8), dtype=int)
    for cell, index in dict.items():
        cell = cell-21
        row = cell//10
        col = cell%10
        output[row, col] = index
    return output

def sign(num:Union[int, None]) -> int:

    '''
    Returns the sign of the input. Input can be an integer or None.

    Returns 1 if num > 0
    Returns -1 if num < 0
    Returns 0 if num == 0 or num == None
    '''

    if num != None:
        if num > 0:
            return 1
        elif num < 0:
            return -1
    return 0