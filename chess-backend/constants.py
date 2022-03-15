'''
Constants to be exported to other scripts.
'''

initial_board_position = {21:-4, 22:-2, 23:-3, 24:-5, 25:-6, 26:-3, 27:-2, 28:-4, 31:-1, 32:-1, 33:-1, 34:-1, 35:-1, 36:-1, 37:-1, 38:-1, 81:1, 82:1, 83:1, 84:1, 85:1, 86:1, 87:1, 88:1, 91:4, 92:2, 93:3, 94:5, 95:6, 96:3, 97:2, 98:4}

# movement range for pawns (without considering other pieces or cell validity)
pawn_move_range = {1:[-10, -20, -11, -9], -1:[10, 20, 11, 9]}

# cell coordinates that are valid: exist on the board
valid_cells = {21, 22, 23, 24, 25, 26, 27, 28, 31, 32, 33, 34, 35, 36, 37, 38, 41, 42, 43, 44, 45, 46, 47, 48, 51, 52, 53, 54, 55, 56, 57, 58, 61, 62, 63, 64, 65, 66, 67, 68, 71, 72, 73, 74, 75, 76, 77, 78, 81, 82, 83, 84, 85, 86, 87, 88, 91, 92, 93, 94, 95, 96, 97, 98}

# mapping of castle type index to name
castle_names = {-5:'Black Queenside', -6:'Black Kingside', 5: 'White Queenside', 6:'White Kingside'}