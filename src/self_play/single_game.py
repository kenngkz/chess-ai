from typing import List

import chess

from src.schema.game import GameStep
from src.schema.player import Player


def generate_game(white: Player, black: Player) -> List[GameStep]:
    board = chess.Board()
    game_history = []
    current_player = white
    for _ in range(1000):
        fen = board.fen()
        move = current_player.select_move(fen)
        game_history.append({"board": fen, "outcome": None})
        board.push(move)
        outcome = board.outcome()
        if outcome:
            for step in game_history:
                step["outcome"] = int(outcome.winner == chess.WHITE)
            break
        current_player = black if current_player == white else white
    else:
        raise Exception(f"Max turns reached!")

    return game_history
