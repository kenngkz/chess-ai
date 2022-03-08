'''
Manages and runs the chess game.
'''

from chess_objects import Board, Move, Pawn, EmptyCell

class GameSave:
    pass  # TODO

class Game:
    stalemate_steps = 50

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

    # GET functions

    def game_over(self):
        '''
        Checks if game is over. 
        Returns None if not over, 0 if stalemate, 1 if White wins and -1 if Black wins
        '''
        pass  # TODO

    def all_prelegal_moves(self):
        prelegal_moves = {1:[], -1:[]}
        for piece in self.board.position.values():
            prelegal_moves[piece.side] += piece.prelegal_moves(self.board)
        return prelegal_moves

    def check(self, side, board:"Board"):
        ''' Returns True if the given side is under check, False otherwise '''
        for piece in board.position.values():
            if piece.side == -side:
                for cell in piece.threat_map_contribution(board):
                    if board.king_position[side] == cell:
                        return True
        return False

    def all_legal_moves(self, side):
        ''' Generate all legal moves. Gets check status as well '''
        legal_moves = []
        for piece in self.board.position.values():
            if piece.side == side:
                if piece is Pawn:
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
                            if self.check_move_legality:
                                promo_allowed = self.cell//10==3 if self.side == 1 else self.cell//10==8
                                if promo_allowed: # handle promotion -> limit to queen and knight promotions
                                    legal_moves += [Move(side, piece.cell, cell, 0, 2), Move(side, piece.cell, cell, 0, 5)]
                                else:
                                    legal_moves.append(move)

                else:  # if not Pawn
                    for cell in piece.threat_map_contribution(self.board):
                        # update current check_status
                        if self.board.occupant(cell).side != side:   # then it is prelegal move
                            move = Move(side, piece.cell, cell)
                            # pseudomove and run check()
                            if self.check_move_legality(move):
                                legal_moves.append(move)

        # TODO: castling

        return legal_moves

    # PUT functions (change some attribute of Game object)

    def make_move(self, board, move:"Move"):
        pass

    def check_move_legality(self):  # pseudomove? move that will be undone when function ends
        pass

    # Miscellaneous functions

    def pseudomove(self, move):
        pass

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