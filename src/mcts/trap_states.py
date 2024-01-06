from . import MCTS
from .chess_state import ChessState

trap_states = [
        ("rnbqkbnr/pp2pp1p/8/2pp2P1/8/2P2P2/PP1PPKP1/RNBQ1BNR w kq - 1 6", "g1g7"),
        ("rnbqkbr1/pppppppp/5n2/4N3/8/8/PPPPPPPP/RNBQKB1R w KQq - 4 3", "e5f7"),
        ("rnbqk1nr/pp3ppp/2p5/3pp3/8/P1N4P/2PPPPP1/R1BQKBNR w KQkq - 0 5", "c3d5"),
        ("rnbqkbnr/pp1pp1p1/2p5/5p1p/8/BP5N/P1PPPPPP/RN1QKB1R w KQkq - 0 4", "a3e7"),
        ("r1bqk2r/p1pp4/8/3R3p/1b6/5PK1/P2PN2P/RNBQ1B2 w kq - 0 15", "d5h5"),
    ]

def eval_trap_states(mcts:MCTS):
    
    results = []
    for state, bad_move in trap_states:
        prediction = mcts.search(ChessState(state), True)
        if prediction["action"].uci() == bad_move:
            results.append(0)
        else:
            results.append(1)
    return sum(results)/len(results)