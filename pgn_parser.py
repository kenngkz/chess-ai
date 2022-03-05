'''
Function to parse .pgn files and return them as a list of tuples.

Data is collected from https://www.ficsgames.org/download.html
'''

# --------------------------------------------------------------------
'''
Imports
'''

from typing import List
from chess.dtype import Board
import chess.legal

# --------------------------------------------------------------------
'''
Folder and File Names
'''

data_folder = 'data/'
file_prefix = 'chessgames'
file_suffix = '.pgn'

# --------------------------------------------------------------------
'''
Function Definitions
'''

def read(filepath):

    ## Intermediate functions to be used later below.
    def get_games(raw_file):
        '''
        Gets a list of games as a list of strings. Each string represents the sequence of moves in one game.
        '''
        raw_games = []
        game_start = False
        game_str = ''
        nextline = False

        # retrieve each game as a str append to list
        for char in raw_file:
            # detect when the move notation for a game begins
            if nextline and char == '1':
                game_start = True
            # detect when the move notation for a game ends
            elif game_start and char == '\n':
                game_start = False
                raw_games.append(game_str)
                game_str = ''
            # if the char is inside move notation for a game, add to game_str
            if game_start:
                game_str += char

            # detect if char is a newline, if it is then pass the information to the next iteration of the loop 
                # to detect if move notation starts/ends
            if char == '\n':
                nextline = True
            else:
                nextline = False

        return raw_games

    def get_moves(raw_games):
        '''
        From a list of strings, each representing a sequence of moves in a game (as a string), extract each move.
        In the output, each game is represented as a list of strings, each string being the algebraic notation of a single move.
        '''
        games = []
        # split each game into moves
        for game in raw_games:
            is_move = False
            moves = [] # list of moves
            move = ''
            space = False

            for char in game:
                # if the first char after a space is a letter, this word represents a move
                if space == True and char.isalpha():
                    is_move = True

                # if current char is a space
                if char == ' ':
                    space = True  # pass the information to the next iteration
                    # if the previous char was part of a move, this char is no longer part of the same move
                    if is_move:
                        is_move = False
                        moves.append(move)  # add the completed move to the list moves and reset the variable move
                        move = ''
                else:
                    space = False
                
                # if this char is part of a move, add it to the variable move
                if is_move == True:
                    move += char

            # remove all non-move words (some words that pass the stage above is not an algebraic notation for a move)
            non_moves = []
            for move in moves:
                if not move[-1].isnumeric() or not move[-1] in {'N', 'B', 'R', 'Q'}:  # some moves are promotion moves: end with these characters
                    non_moves.append(move)
            [moves.remove(item) for item in non_moves]

            # add the list of moves to the games list: this list of moves represents a full game.
            games.append(moves)

        return games

    def alg_to_cell(alg_cell:str) -> int:
        '''
        Parse the algebraic notation for a cell and return the equivalent cell number.
        '''
        file_conversion = {'a':1, 'b':2, 'c':3, 'd':4, 'e':5, 'f':6, 'g':7, 'h':8}
        rank_conversion = {'1':8, '2':7, '3':6, '4':5, '5':4, '6':3, '7':2, '8':1}

        col = file_conversion[alg_cell[0]]
        row = rank_conversion[alg_cell[1]]

        return 10 + row*10 + col

    def get_origin(board:"Board", side:int, dest_cell:int) -> int:
        '''
        Find the start cell of the move from the given position and destination cell.
        '''

        legal_moves = chess.legal.board(board, side)

        potential_moves = []
        for move in legal_moves:
            move.add_board(board)
            move_info = move.info(show=False)
            if move_info[2] == dest_cell:
                potential_moves.append(move_info)
        
        return potential_moves

    def parse_move(board:"Board", alg_move:str, index:int) -> tuple:
        '''
        Parse the algebraic notation for a single move and returns a tuple as representation for the move.
        '''
        piece_notation = {'N':2, 'B':3, 'R':4, 'Q':5, 'K':6}

        promotion = False

        # drop capture notation 'x'
        alg_move.replace('x', '', 1)

        # get the side from the index of the move within the game
        if index%2 == 0:
            side = 1
        else:
            side = -1
        
        # castling
        castle_notation = {'O-O-O':5, 'O-O':6}
        if alg_move in castle_notation:
            return (side, 0, 0, castle_notation[alg_move]*side, 0)

        # get destination cell
        if alg_move[-1].isnumeric: # regular move
            dest_alg = alg_move[-2:]
            dest_cell = alg_to_cell(dest_alg)
        elif alg_move[-1] in piece_notation: # promotion move
            promotion = True
            dest_alg = alg_move[-4:-2]
            dest_cell = alg_to_cell(dest_alg)
        else: # move that results in check/checkmate
            if alg_move[-2] in piece_notation: # promotion + check
                promotion = True
                dest_alg = alg_move[-5:-3]
                dest_cell = alg_to_cell(dest_alg)
            else:
                dest_alg = alg_move[-3:-1]
                dest_cell = alg_to_cell(dest_alg)

        # get origin_cell
        origin_cells = get_origin(board, side, dest_cell)
        if len(origin_cells) == 1:
            origin_cell = origin_cells[0][1]
        else:
            # get the piece from alg_move
            for i in range(3):
                if alg_move[i].isupper():
                    skip = i
                    piece = piece_notation[alg_move[i]] * side
                    break
            else:
                # if the first 3 char are not uppercase, piece is a pawn
                piece = side
                for i in range(3):
                    if alg_move[i:i+2] == dest_alg:
                        skip = i

            # if skip == 0, the no file or rank need to identify the origin cell
            if skip == 0:
                moving_pieces = [move[5] for move in origin_cells]
                indexes = [i for i, moving_piece in enumerate(moving_pieces) if piece == moving_piece]
                origin_cell = origin_cells[indexes[0]][1]
            # if skip == 1, either rank or file is needed to identify the origin cell
            elif skip == 1:
                pass
            # if skip == 2, the origin cell is specified directly
            else:
                origin_cell = alg_to_cell(alg_move[:2])
        

    def parse_game(move_list:list) -> List[tuple]:
        '''
        Parses and converts the list of str moves (alg notation) to list of tuples.
        '''
        board = Board()
        for index, alg_move in enumerate(move_list):
            parse_move(board, alg_move, index)


    ## Run conversion to list
    # Open the .pgn data file
    with open(filepath, 'r') as f:
        raw_file = f.read()

    # Get each game from the pgn file, with each game as a string
    raw_games = get_games(raw_file)
    # Get the moves for each game, with each move as a string: one game will be a list of strings(moves).
    games = get_moves(raw_games)

    output_games = []
    for game in games:
        output_games.append(parse_game(game))

    return output_games

def build_path(year):

    '''
    Returns the path to the pgn file given a year.
    Depends on the global variables data_folder, file_prefix and file_suffix defined in the section above.
    '''

    return data_folder + file_prefix + str(year) + file_suffix