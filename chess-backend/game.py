'''
Manages and runs the chess game.
'''

from chess_objects import Board, Move, Pawn, EmptyCell, King, Rook
import utils

class GameState:

    def __init__(self, game_obj:"Game"):
        self.position = game_obj.board.position
        self.player_to_move = game_obj.player_to_move
        self.move_counter = game_obj.move_counter
        self.move_history = game_obj.move_history
        self.stalemate_counter = game_obj.stalemate_counter
        self.castle_status = game_obj.castle_status

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
            for name, val in data.values():
                blank_state.__dict__[name] = val
        elif isinstance(state_source, dict):
            for name, val in state_source.values():
                blank_state.__dict__[name] = val
        return blank_state

    def save(self, filename, folder=None):
        ''' Save as a json file '''
        data = {name:val for name, val in self.__dict__.values()}
        filename += ".json"
        filepath = utils.path_join(folder, filename)
        with open(filepath, "w") as f:
            f.write(data)

class Game:
    stalemate_steps = 50
    castling_threat_free = {-1:{-5:[23, 24], -6:[26, 27]}, 1:{5:[93, 94], 6:[96, 97]}}
    castling_occupant_free = {-1:{-5:[22, 23, 24], -6:[26, 27]}, 1:{5:[92, 93, 94], 6:[96, 97]}}

    def __init__(self):
        self.board = Board()
        self.player_to_move = 1
        self.move_counter = 0
        self.move_history = []
        self.stalemate_counter = 0
        self.castle_status = {-5:True, -6:True, 5:True, 6:True}  # tracks whether castling is allowed
        self.check_status = {-1:None, 1:None}  # specifies whether the side is under check
        self.legal_moves = {-1:None, 1:None}

    @classmethod
    def load(cls, state_source):
        ''' Load Game object from GameState save file or GameState obj'''
        blank_game = Game()
        if isinstance(state_source, GameState):
            for name, val in GameState.__dict__.values():
                blank_game.__dict__[name] = val
        elif isinstance(state_source, str):
            with open(state_source, "r") as f:
                data = eval(f.read())
            for name, val in data.values():
                blank_game.__dict__[name] = val
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
            if piece.side == -side:
                for cell in piece.threat_map_contribution(board):
                    if board.king_position[side] == cell:
                        return True
        return False

    def get_state(self):
        return GameState(self)

    # Legal moves functions

    def all_legal_moves(self):
        ''' Generate all legal moves for both sides and saves as .legal_moves attribute. Gets check status for both sides as well as well '''
        legal_moves = {-1:[], 1:[]}
        threat_map = {-1:[], 1:[]}
        for piece in self.board.position.values():
            if isinstance(piece, Pawn):
                for cell, is_threat in piece.candidate_move_cell(self.board):
                    move = None
                    if is_threat:  # then it is a capture move cell
                        threat_map[-piece.side].append(cell)
                        if self.board.king_position[-piece.side] == cell:  # update current check_status
                            self.check_status[-piece.side] = True
                        if self.board.occupant(cell).side == -piece.side:  # then it is prelegal move
                            move = Move(piece.side, piece.cell, cell)
                    else:  # then it is a forward move cell
                        if self.board.occupant(cell) == EmptyCell:  # then it is prelegal move
                            move = Move(piece.side, piece.cell, cell)

                    if move:  # if prelegal move, check move legality
                        if self._check_move_legality(move):
                            promo_allowed = piece.cell//10==3 if piece.side == 1 else piece.cell//10==8
                            if promo_allowed: # handle promotion -> limit to queen and knight promotions
                                legal_moves += [Move(piece.side, piece.cell, cell, 0, 2), Move(piece.side, piece.cell, cell, 0, 5)]
                            else:
                                legal_moves[piece.side].append(move)

            else:  # if not Pawn
                for cell in piece.threat_map_contribution(self.board):
                    threat_map[-piece.side].append(cell)
                    # update current check_status
                    if self.board.king_position[-piece.side] == cell:
                        self.check_status[-piece.side] = True
                    if self.board.occupant(cell).side != piece.side:   # then it is prelegal move
                        move = Move(piece.side, piece.cell, cell)
                        # check move legality
                        if self._check_move_legality(move):
                            legal_moves[piece.side].append(move)

        # castling moves
        for side in [-1, 1]:
            if self.check_status[side] == None:
                self.check_status[side] = False
            if not self.check_status[side]:
                for castle_type in self.castling_occupant_free[side]:
                    if self.castle_status[castle_type]:
                        # check occupant free cells -> cells must not be occupied to perform castling
                        if sum(not self.board.occupant(cell) is EmptyCell for cell in self.castling_occupant_free[side][castle_type]) == 0:
                            # check threat free cells -> cells must not be threatened to perform castling
                            if sum(cell in threat_map[side] for cell in self.castling_threat_free[side][castle_type]) == 0:
                                legal_moves[side].append(Move(side, self.board.king_position[side], 0, castle_type, 0))
        self.legal_moves = legal_moves

    def _check_move_legality(self, move:"Move"):
        ''' Checks whether a move is legal by making a move on a Board copy and checking if it places the King under check '''
        new_board = self.make_move(move, permanent=False)
        return not self._run_check(move.side, new_board)

    # Make Move functions (change some attribute of Game object)

    def make_move(self, move:"Move", permanent=True):
        ''' Executes a move on current board. permanent=False to return new_board instead of updating current board '''
        new_board = self.board.copy()
        piece = new_board.occupant(move.start)
        if move.castle_type:
            king_cells, rook_cells = move.castle_move_cells
            new_board.move_piece(*king_cells)
            new_board.move_piece(*rook_cells)
        else:
            new_board.move_piece(move.start, move.final)
        
        if permanent:
            self.board = new_board
            self.player_to_move *= -1
            self.stalemate_counter += 1
            self.move_counter += 1
            if isinstance(piece, King):
                self.castle_status[piece.side*5] = False
                self.castle_status[piece.side*6] = False
            elif isinstance(piece, Rook):
                if piece.cell%10 == 1:
                    self.castle_status[piece.side*5] = False
                elif piece.cell%10 == 8:
                    self.castle_status[piece.side*6] = False
            self.check_status = {-1:None, 1:None}
        else:
            return new_board