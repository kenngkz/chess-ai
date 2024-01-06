from typing import List

import chess

from .base.state import BaseState


class ChessState(BaseState):

    def __init__(self, fen:str):
        self.fen = fen
        self.board = chess.Board(self.fen)

    def getCurrentPlayer(self):
        return 1 if self.fen.split(" ")[1] == "w" else -1

    def getPossibleActions(self) -> List[chess.Move]:
        return list(self.board.legal_moves)

    def takeAction(self, action: chess.Move) -> "ChessState":
        self.board.push(action)
        new_state = ChessState(self.board.fen())
        self.board.pop()
        return new_state

    def isTerminal(self):
        return self.board.is_game_over()

    def getReward(self):
        outcome = self.board.outcome()
        if outcome:
            return int(outcome.winner) if outcome.winner != None else 0
        check_penalty = 2
        piece_values = {
            "p": -1,
            "n": -3,
            "b": -3,
            "r": -5,
            "q": -9,
            "k": 0,
            "P": 1,
            "N": 3,
            "B": 3,
            "R": 5,
            "Q": 9,
            "K": 0,
        }
        # scales the reward to control the sensitivity of reward to piece values + check
        reward_scaling_factor = 50

        # calculate reward from pieces
        board_pieces = self.fen.split(" ")[0]
        # eliminate empty spots
        board_pieces = "".join(char for char in board_pieces if not char.isdigit())
        board_pieces = board_pieces.replace("/", "")
        # convert to piece values
        board_piece_values = [piece_values[piece] for piece in board_pieces]
        reward = sum(board_piece_values)

        # rewards for check
        if self.board.turn == chess.WHITE:
            reward -= check_penalty * self.board.is_check()
        else:
            reward += check_penalty * self.board.is_check()

        return 0.5 + (reward / reward_scaling_factor)