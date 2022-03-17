'''
Manages and runs the chess game.
'''

from chess_objects import Board, Move, piece_threat_map
import utils
import constants

from copy import copy

class GameState:

    def __init__(self, game_obj:"Game", include_history=False):
        self.hashboard = game_obj.board.enhash()
        self.player_to_move = game_obj.player_to_move
        self.move_counter = game_obj.move_counter
        self.stalemate_counter = game_obj.stalemate_counter
        self.castle_status = game_obj.castle_status_tuple()  # tuple with bools
        if include_history:
            self.move_history = tuple(game_obj.move_history)  # list is mutable

    @classmethod
    def load(cls, state_source):
        '''
        Load from json file or dict. 
        Note: Can call Game.load in the Game class to generate Game obj directly from file.
        '''
        blank_state = cls(Game())
        if isinstance(state_source, str):
            with open(state_source, "r") as f:
                data = eval(f.read())
            for name, val in data.items():
                blank_state.__dict__[name] = val
        elif isinstance(state_source, dict):
            for name, val in state_source.items():
                blank_state.__dict__[name] = val
        return blank_state

    def save(self, filename, folder=None):
        ''' Save as a json file '''
        data = {name:val for name, val in self.__dict__.items()}
        filename += ".json"
        filepath = utils.path_join(folder, filename)
        with open(filepath, "w") as f:
            f.write(str(data))

class Game:
    stalemate_steps = 50
    castling_threat_free = {-1:{-5:[23, 24], -6:[26, 27]}, 1:{5:[93, 94], 6:[96, 97]}}
    castling_occupant_free = {-1:{-5:[22, 23, 24], -6:[26, 27]}, 1:{5:[92, 93, 94], 6:[96, 97]}}

    def __init__(self):
        self.board = Board(constants.initial_hashboard)
        self.player_to_move = 1
        self.move_counter = 0
        self.move_history = []
        self.stalemate_counter = 0
        self.castle_status = [-5, -6, 5, 6]  # tracks whether castling is allowed: if present in list then allowed
        self.check_status = {-1:None, 1:None}  # specifies whether the side is under check
        self.legal_moves = {-1:None, 1:None}

    @classmethod
    def load(cls, state_source):
        ''' Load Game object from GameState save file or GameState obj'''
        blank_game = Game()
        if isinstance(state_source, GameState):
            for name, val in state_source.__dict__.items():
                if name == "hashboard":
                    blank_game.board = Board(val)
                elif name == "move_history":
                    blank_game.move_history = list(val)
                else:
                    blank_game.__dict__[name] = val
                blank_game.castle_status = [castle_type for castle_type, castle_status in zip([-5, -6, 5, 6], blank_game.castle_status) if castle_status]
        elif isinstance(state_source, str):
            with open(state_source, "r") as f:
                data = eval(f.read())
            for name, val in data.items():
                blank_game.__dict__[name] = val
        blank_game.castle_status = list(blank_game.castle_status)
        return blank_game

    # Game state functions

    def game_over(self):
        '''
        Checks if game is over. 
        Returns None if not over, 0 if stalemate, 1 if White wins and -1 if Black wins
        '''
        if self.stalemate_counter >= self.stalemate_steps:
            return 0
        for side in [-1, 1]:
            if self.check_status[side]:
                if len(self.legal_moves[side]) == 0:
                    return -side
            else:
                if len(self.legal_moves[side]) == 0:
                    return 0
        return None

    def is_check(self, side):  # used by Game object user
        ''' Gets the check status for the given side for the current board position '''
        if self.check_status[side] == None:
            self.check_status[side] = self._run_check(side, self.board)
        return self.check_status[side]

    def _run_check(self, side, board:"Board"):  # used for checking move legality
        ''' 
        Runs through threat_map for the opposing side. 
        Returns True if the given side is under check, False otherwise. 
        Requires board to be passed
        '''
        for piece in board.position.values():
            if piece[0] == -side:
                for cell in piece_threat_map(piece, self.board):
                    if board.king_position[side] == cell:
                        return True
        return False

    def get_state(self):
        return GameState(self)

    def castle_status_tuple(self) -> "tuple[bool]":
        return tuple((key in self.castle_status for key in [-5, -6, 5, 6]))

    # Legal moves functions

    def all_legal_moves(self):
        ''' Generate all legal moves for both sides and saves as .legal_moves attribute. Gets check status for both sides as well as well '''
        self.legal_moves = {-1:[], 1:[]}
        threat_map = {-1:[], 1:[]}
        for piece in self.board.position.values():
            piece_side, piece_index, piece_cell, _ = piece
            if piece_index == 0:
                continue
            elif piece_index == 1:
                for cell, is_threat in piece_threat_map(piece, self.board):
                    move = None
                    if is_threat:  # then it is a capture move cell
                        threat_map[-piece_side].append(cell)
                        if self.board.king_position[-piece_side] == cell:  # update current check_status
                            self.check_status[-piece_side] = True
                        if self.board.occupant(cell)[0] == -piece_side:  # if occupant is enemy, then it is prelegal move
                            move = Move(piece_side, piece_cell, cell)
                    else:  # then it is a forward move cell
                        if self.board.occupant(cell)[0] == 0:  # if occupant is empty, then it is prelegal move
                            move = Move(piece_side, piece_cell, cell)

                    if move:  # if prelegal move, check move legality
                        if self._check_move_legality(move):
                            promo_allowed = piece_cell//10==3 if piece_side == 1 else piece_cell//10==8
                            if promo_allowed: # handle promotion -> limit to queen and knight promotions
                                self.legal_moves[piece_side] += [Move(piece_side, piece_cell, cell, 0, 2), Move(piece_side, piece_cell, cell, 0, 5)]
                            else:
                                self.legal_moves[piece_side].append(move)

            else:  # if not Pawn
                for cell, _ in piece_threat_map(piece, self.board):
                    threat_map[-piece_side].append(cell)
                    # update current check_status
                    if self.board.king_position[-piece_side] == cell:
                        self.check_status[-piece_side] = True
                    if self.board.occupant(cell)[0] != piece_side:   # if occupant not ally, then it is prelegal move
                        move = Move(piece_side, piece_cell, cell)
                        # check move legality
                        if self._check_move_legality(move):
                            self.legal_moves[piece_side].append(move)

        # castling moves
        for side in [-1, 1]:
            if self.check_status[side] == None:
                self.check_status[side] = False
        for castle_type in self.castle_status:
            side = utils.sign(castle_type)
            if sum(self.board.occupant(cell)[0]!=0 for cell in self.castling_occupant_free[side][castle_type]) == 0:
                if sum(cell in threat_map[side] for cell in self.castling_threat_free[side][castle_type]) == 0:
                    self.legal_moves[side].append(Move(side, self.board.king_position[side], 0, castle_type, 0))

        # for side in [-1, 1]:
        #     if self.check_status[side] == None:
        #         self.check_status[side] = False
        #     if not self.check_status[side]:
        #         for castle_type in self.castling_occupant_free[side]:
        #             if self.castle_status[castle_type]:
        #                 # check occupant free cells -> cells must not be occupied to perform castling
        #                 if sum(self.board.occupant(cell)[0]!=0 for cell in self.castling_occupant_free[side][castle_type]) == 0:
        #                     # check threat free cells -> cells must not be threatened to perform castling
        #                     if sum(cell in threat_map[side] for cell in self.castling_threat_free[side][castle_type]) == 0:
        #                         self.legal_moves[side].append(Move(side, self.board.king_position[side], 0, castle_type, 0))

    def _check_move_legality(self, move:"Move"):
        ''' Checks whether a move is legal by making a move on a Board copy and checking if it places the King under check '''
        new_board = self.make_move(move, permanent=False)
        return not self._run_check(move.side, new_board)

    # Make Move functions (change some attribute of Game object)

    def make_move(self, move:"Move", permanent=True):
        ''' Executes a move on current board. permanent=False to return new_board instead of updating current board '''
        new_board = self.board.copy()
        piece = new_board.occupant(move.start)
        n_pieces = len(new_board.position)
        if move.castle_type:
            king_cells, rook_cells = move.castle_move_cells
            new_board.move_piece(*king_cells)
            new_board.move_piece(*rook_cells)
        else:
            new_board.move_piece(move.start, move.end, move.promo)

        if permanent:
            piece_side, piece_index, piece_cell,  *_ = piece
            self.board = new_board
            self.player_to_move *= -1
            if piece_index == 1 or n_pieces > len(new_board.position):
                self.stalemate_counter = 0
            else:
                self.stalemate_counter += 1
            self.move_counter += 1
            self.move_history.append(move.to_tuple())
            for castle_type in self.castle_status:
                castle_type_side = utils.sign(castle_type)
                if castle_type_side == piece_side:
                    if piece_index == 6:
                        self.castle_status.remove(castle_type)
                    elif piece_index == castle_type:
                        self.castle_status.remove(castle_type)
            self.check_status = {-1:None, 1:None}
        else:
            return new_board