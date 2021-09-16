##### PRELEGAL_FUCTIONS #####

# IMPORTS
from done.get import get_occupant
from done.indicator import is_traversible

### FUNCTION DEFINITIONS ###

def pre_pawn(board, pawn_cell, side):
    move_dirs = [-10*side, -20*side, -11*side, -9*side]
    new_cell = [pawn_cell+move for move in move_dirs]
    # calculate if first move jump is allowed for this pawn_cell and side
    jump_allowed = pawn_cell//10==8 if side == 1 else pawn_cell//10==3

    # go through each condition iteratively and append to final output list
    prelegal_dest = []
    if get_occupant(board, new_cell[0]) == 0:
        prelegal_dest.append(new_cell[0])
    if get_occupant(board, new_cell[1]) == 0 and jump_allowed:
        prelegal_dest.append(new_cell[1])
    if get_occupant(board, new_cell[2]) == -side:
        prelegal_dest.append(new_cell[2])
    if get_occupant(board, new_cell[3]) == -side:
        prelegal_dest.append(new_cell[3])
    return prelegal_dest


def pre_leaper(board, leaper_cell, move_dirs, side):

    prelegal_dest = []
    for move_dir in move_dirs:
        new_cell = leaper_cell + move_dir
        if is_traversible(board, new_cell, side):
            prelegal_dest.append(new_cell)
    return prelegal_dest

def pre_slider(board, slider_cell, move_dirs, side):

    prelegal_dest = []
    for move_dir in move_dirs:
        for _ in range(8):
            slider_cell += move_dir
            occupant = get_occupant(board, slider_cell)
            if occupant == 0:
                prelegal_dest.append(slider_cell)
            elif occupant == -side:
                prelegal_dest.append(slider_cell)
                break
            else:
                break
    return prelegal_dest