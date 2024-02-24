from typing import List, TypedDict

import chess

from src.schema.player import Player


class GameStep(TypedDict):
    board: str
    outcome: float  # 1 for white win, 0 for black win, 0.5 for stalemate


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
