'''
Utility functions
'''

from constants import index_to_name

def add(v1, v2):
    ''' Element-wise vector addition '''
    return [a+b for a, b in zip(v1, v2)]

def print_move(move:"Move", board:"Board"):
    init_params = move.__repr__()
    if move.start == 0:
        movement = f'{move.castle_names[move.castle_type]}'
    else:
        movement = f'{index_to_name[board.occupant(move.start)]} -> ' \
            + f'{index_to_name[board.occupant(move.final)]}'
    print(init_params, movement)