import pickle

def add(coor1, coor2) -> list:
    return [coor1[0]+coor2[0], coor1[1]+coor2[1]]

move_range = {}  # move_range[coor][piece_type] for pawn/knight/king, move_range[coor][piece_type][direc] for bishop/rook/queen
for row in range(8):
    for col in range(8):
        print(f'({row}, {col})')
        coor_dict = {}
        # pawns
        if row == 1:
            black_coors = [(col, row+1), (col, row+2)]
        elif row >= 2 and row <= 6:
            black_coors = [(col, row+1)]
        if row == 6:
            white_coors = [(col, row-1), (col, row-2)]
        elif row >= 1 and row <= 5:
            white_coors = [(col, row-1)]
        if row == 0 or row == 7:
            white_coors = []
            black_coors = []
        else:
            if col-1 >= 0:
                black_coors.append((col-1, row+1))
                white_coors.append((col-1, row-1))
            if col+1 <= 7:
                black_coors.append((col+1, row+1))
                white_coors.append((col+1, row-1))
        coor_dict[-1] = black_coors
        coor_dict[1] = white_coors
        
        # knights
        kn_direcs = [(-2, -1), (-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2)]
        coors = []
        for direc in kn_direcs:
            new_coor = tuple(add((row, col), direc))
            if min(new_coor) >= 0 and max(new_coor) <= 7:
                coors.append(new_coor)
        coor_dict[-2] = coors
        coor_dict[2] = coors

        # bishops
            # direction:[coors] instead of [coors]
        b_direcs = [(-1, -1), (-1, 1), (1, 1), (1, -1)]
        coors = {}
        for direc in b_direcs:
            coors_in_direc = []
            for i in range(1, 8):
                next_coor = tuple(add((row, col), (i*direc[0], i*direc[1])))
                if max(next_coor) <= 7 and min(next_coor) >= 0:
                    coors_in_direc.append(next_coor)
                else:
                    break
            coors[direc] = coors_in_direc
        coor_dict[-3] = coors
        coor_dict[3] = coors

        # rooks
            # direction:[coors] instead of [coors]
        r_direcs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        coors = {}
        for direc in r_direcs:
            coors_in_direc = []
            for i in range(1, 8):
                next_coor = tuple(add((row, col), (i*direc[0], i*direc[1])))
                if max(next_coor) <= 7 and min(next_coor) >= 0:
                    coors_in_direc.append(next_coor)
                else:
                    break
            coors[direc] = coors_in_direc
        coor_dict[-4] = coors
        coor_dict[4] = coors

        # queens
            # direction:[coors] instead of [coors]
        q_direcs = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
        coors = {}
        for direc in q_direcs:
            coors_in_direc = []
            for i in range(1, 8):
                next_coor = tuple(add((row, col), (i*direc[0], i*direc[1])))
                if max(next_coor) <= 7 and min(next_coor) >= 0:
                    coors_in_direc.append(next_coor)
                else:
                    break
            coors[direc] = coors_in_direc
        coor_dict[-5] = coors
        coor_dict[5] = coors

        # king
        k_direcs = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
        coors = []
        for direc in k_direcs:
            next_coor = tuple(add((row, col), (i*direc[0], i*direc[1])))
            if max(next_coor) <= 7 and min(next_coor) >= 0:
                coors.append(next_coor)
        coors.append('queen')
        coors.append('king')
        coor_dict[-6] = coors
        coor_dict[6] = coors

        move_range[(row, col)] = coor_dict

# save move_range as pkl file
with open('move_range.pkl', 'wb') as f:
    pickle.dump(move_range, f)