'''
Manages and runs the chess game.
'''

from chess_objects import Board, Move, Pawn, EmptyCell

class GameState:
    pass  # TODO

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
        self.check_status = {-1:None, 1:None}

    @classmethod
    def load(cls):
        pass # TODO

    # Game state functions

    def game_over(self):
        '''
        Checks if game is over. 
        Returns None if not over, 0 if stalemate, 1 if White wins and -1 if Black wins
        '''
        pass  # TODO

    def is_check(self, side):  # used by Game object user
        ''' Gets the check status for the given side for the current board position '''
        if self.check_status[side] == None:
            self.check_status[side] = self.run_check(side, self.board)
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
        pass   # TODO

    # Legal moves functions

    def all_legal_moves(self, side):
        ''' Generate all legal moves for a side. Gets check status for both sides as well as well '''
        legal_moves = []
        opponent_threat_map = []
        for piece in self.board.position.values():
            if piece.side == side:
                if isinstance(piece, Pawn):
                    for cell, is_threat in piece.candidate_move_cell(self.board):
                        move = None
                        if is_threat:  # then it is a capture move cell
                            # update current check_status
                            if self.board.king_position[-side] == cell:
                                self.check_status[-side] = True
                            if self.board.occupant(cell).side == -side:  # then it is prelegal move
                                move = Move(side, piece.cell, cell)
                        else:  # then it is a forward move cell
                            if self.board.occupant(cell) == EmptyCell:  # then it is prelegal move
                                move = Move(side, piece.cell, cell)

                        if move:  # if prelegal move, pseudomove and check_move_legality
                            if self._check_move_legality(move):
                                promo_allowed = piece.cell//10==3 if piece.side == 1 else piece.cell//10==8
                                if promo_allowed: # handle promotion -> limit to queen and knight promotions
                                    legal_moves += [Move(side, piece.cell, cell, 0, 2), Move(side, piece.cell, cell, 0, 5)]
                                else:
                                    legal_moves.append(move)

                else:  # if not Pawn
                    for cell in piece.threat_map_contribution(self.board):
                        # TODO update current check_status
                        if self.board.occupant(cell).side != side:   # then it is prelegal move
                            move = Move(side, piece.cell, cell)
                            # pseudomove and run check()
                            if self._check_move_legality(move):
                                legal_moves.append(move)
            else:  # if enemy piece
                opponent_threat_map += piece.threat_map_contribution(self.board)

        # set check_status for ally side
        self.check_status[side] = self.board.king_position[side] in opponent_threat_map
        # castling moves
        if not self.check_status[side]:
            for castle_type in self.castling_occupant_free[side]:
                # check threat free cells -> cells must not be threatened to perform castling
                if sum(cell in opponent_threat_map for cell in self.castling_threat_free[side][castle_type]) == 0:
                    # check occupant free cells -> cells must not be occupied to perform castling
                    if sum(not self.board.occupant(cell) is EmptyCell for cell in self.castling_occupant_free[side][castle_type]) == 0:
                        legal_moves.append(Move(side, 0, 0, castle_type, 0))
        return legal_moves

    def _check_move_legality(self, move:"Move"):
        ''' Checks whether a move is legal by making a move on a Board copy and checking if it places the King under check '''
        new_board = self.make_move(move, permanent=False)
        return not self._run_check(move.side, new_board)

    # Make Move functions (change some attribute of Game object)

    def make_move(self, move:"Move", permanent=True):
        ''' Executes a move on current board. permanent=False to return new_board instead of updating current board '''
        new_board = self.board.copy()
        if move.castle_type:
            king_cells, rook_cells = move.castle_move_cells
            new_board.move_piece(*king_cells)
            new_board.move_piece(*rook_cells)
        else:
            new_board.move_piece(move.start, move.final)
        
        if permanent:
            self.board = new_board
            # TODO: other move related attr -> stalemate counter, castle_status, reset check_status, legal_moves?
        else:
            return new_board

'''
What do i need prelegal moves for?
V1:
 - is_check: check if king cell is in opposing side's prelegal moves final_cell
 - legal_moves: spawn copy of board, execute candidate move and see if ally king is under check
V2:
 - is_check not using prelegal: see if threat cells have the right threat type
 - legal_moves: spawn copy of board, execute candidate move and see if ally king is under check
V3: 
 - set is_check when prelegal moves are being generated


is there another way to run legal_moves?
- bunch of ifelse?
- threat maps: map of cells that are 
'''