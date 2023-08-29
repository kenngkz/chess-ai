import chess
import time
import random
import itertools
import os
import numpy as np
import pandas as pd
import math
from typing import Iterable, Any, List, Tuple, Dict
from enum import Enum
from scipy.special import expit

from src.logger import get_logger

logger = get_logger("MCTS")


class MCTSNode:
    def __init__(
        self,
        side: bool,
        action: chess.Move = None,
        parent: "MCTSNode" = None,
        explore_param: float = None,
        ucb_base: float = None,
    ):
        self.side = side
        self.action = action
        self.parent = parent
        self.explore_param = explore_param
        self.ucb_base = ucb_base if ucb_base else math.e
        self.score = {"reward": 0, "visits": 0}
        self.children: List[MCTSNode] = []

    def add_children(self, action_space: Iterable[Any]):
        for action in action_space:
            child = MCTSNode(
                not self.side, action, self, self.explore_param, self.ucb_base
            )
            self.children.append(child)

    def update_score(self, reward: float):
        self.score["reward"] += reward
        self.score["visits"] += 1

    def ucb(self) -> float:
        if self.score["visits"] == 0:
            return np.inf
        avg_score = self.score["reward"] / self.score["visits"]
        # exploration_term = self.explore_param * np.sqrt(
        #     math.log(max(self.parent.score["visits"], 1), self.ucb_base)
        #     / 1.1 ** self.score["visits"]
        # )
        exploration_term = self.explore_param * np.sqrt(
            math.log(max(self.parent.score["visits"], 1), self.ucb_base)
            / self.score["visits"]
        )
        return avg_score + exploration_term


class MCTSAgent:
    class ShowLevel(Enum):
        NONE = 0
        MOVE = 1
        ROLLOUT = 2
        DISTRIBUTION = 3
        TREE = 4
        PATHS = 5

    def __init__(
        self,
        side_is_white: bool,
        time_limit: float = 10,
        show: ShowLevel = ShowLevel.NONE,
        max_depth: int = np.inf,
        explore_param: float = 2,
        found_threshold_multiplier: float = 1.5,
        found_threshold: int = 50,
        ucb_base: float = None,
    ):
        """
        Intialization args:
            expore_param: hyperparameter controlling incentive to explore unvisited nodes
            time_limit: search will quit after the specified number of seconds
            show: show results breakdown if 1, also show the search progress if 2
            max_depth: max number of steps to run rollout, if max_depth is hit during rollout, the agent will estimate the value of the state
        """
        self.side = side_is_white
        self.time_limit = time_limit
        self.max_depth = max_depth
        self.explore_param = explore_param
        self.found_threshold_multiplier = found_threshold_multiplier
        self.found_threshold = found_threshold
        self.ucb_base = ucb_base
        self.turn = 0
        self._setup_logging(self.ShowLevel(show))
        self.tree: Dict[str, MCTSNode] = {}

    def _setup_logging(self, show_level: ShowLevel):
        # show one log per move
        self._move_logging = self.__disabled_logging
        if show_level.value >= self.ShowLevel.MOVE.value:
            self._move_logging = self.__move_logging
        # show one log per rollout
        self._rollout_logging = self.__disabled_logging
        if show_level.value >= self.ShowLevel.ROLLOUT.value:
            self._rollout_logging = self.__rollout_logging
        # save move options distribution to file (once per action taken)
        self._distibution_logging = self.__disabled_logging
        if show_level.value >= self.ShowLevel.DISTRIBUTION.value:
            self._distibution_logging = self.__distribution_logging
        # save final node tree to file (once per action taken)
        self._tree_logging = self.__disabled_logging
        if show_level.value >= self.ShowLevel.TREE.value:
            self._tree_logging = self.__tree_logging
        # save selection + rollout paths
        self._path_logging_to_mem = self.__disabled_logging
        self._paths_logging_to_file = self.__disabled_logging
        if show_level.value >= self.ShowLevel.PATHS.value:
            self._paths = []
            # save a single rollout path to memory (once per rollout)
            self._path_logging_to_mem = self.__save_selected_path_to_mem
            # save all rollout paths to file (once per action taken)
            self._paths_logging_to_file = self.__save_paths_to_file

    def pred(self, fen: str):
        if (fen.split(" ")[1] == "w") != self.side:
            raise Exception(
                f"Current turn is {'black' if self.side else 'white'}. This player is {'white' if self.side else 'black'}."
            )

        root = self._root_node(fen)
        start_time = time.time()
        total_time = total_depth = start = end = depth = reward = 0
        initial_board = chess.Board(fen)
        root.add_children(list(initial_board.legal_moves))
        highest_children = []
        for i in itertools.count():
            # self._rollout_logging(
            #     count=i, duration=end - start, depth=depth, reward=reward
            # )
            node = self._selection(root)
            node, board = self._expansion(fen, node)
            start = time.perf_counter()
            reward, depth, rollout_moves = self._rollout(board)
            end = time.perf_counter()
            # self._path_logging_to_mem(
            #     node=node,
            #     rollout_moves=rollout_moves,
            #     fen_final_state=board.fen(),
            #     reward=reward,
            # )
            total_time += end - start
            total_depth += depth
            node = self._backpropogation(reward, node)
            if len(highest_children) < 2:
                highest_children.append(node)
            else:
                if node.score["visits"] > highest_children[0].score["visits"]:
                    highest_children = [node, highest_children[0]]
                elif (
                    node.score["visits"] > highest_children[1].score["visits"]
                    and node != highest_children[0]
                ):
                    highest_children[1] = node
                # if (
                #     highest_children[0].score["visits"]
                #     > self.found_threshold_multiplier
                #     * highest_children[1].score["visits"]
                #     + self.found_threshold
                # ):
                #     why = "found"
                #     break
            if time.time() - start_time > self.time_limit:
                why = "time"
                break
        max_visit = max([child.score["visits"] for child in root.children])
        most_visited_children = [
            child for child in root.children if child.score["visits"] == max_visit
        ]
        max_reward = max([child.score["reward"] for child in most_visited_children])
        best_children = [
            child
            for child in most_visited_children
            if child.score["reward"] == max_reward
        ]
        chosen_node = random.choice(best_children)
        chosen_action = chosen_node.action
        initial_board.push(chosen_action)
        self._save_chosen_node_children_to_tree(chosen_node, initial_board.fen())
        self._move_logging(
            reason=why,
            result=chosen_action,
            iterations=i,
            max_visit=max_visit,
            total_time=total_time,
            total_depth=total_depth,
            fen_state_after_move=initial_board.fen(),
        )
        self._distibution_logging(root=root, fen_state=fen)
        self._tree_logging(root=root, fen_initial_state=fen)
        self._paths_logging_to_file(fen_initial_state=fen)
        self.turn += 1
        return chosen_action

    def _root_node(self, fen: str) -> MCTSNode:
        if fen not in self.tree:
            return MCTSNode(
                not self.side, explore_param=self.explore_param, ucb_base=self.ucb_base
            )
        existing_node = self.tree[fen]
        existing_node.action = None
        existing_node.parent = None
        self.tree = {}
        return existing_node

    def _selection(self, root_node: MCTSNode) -> MCTSNode:
        """Selects the leaf node by successively picking branches with the highest UCB score"""
        current_node = root_node
        for i in itertools.count():
            children = current_node.children
            if len(children) == 0:
                return current_node
            max_ucb = max([child.ucb() for child in children])
            current_node = random.choice(
                [child for child in children if child.ucb() == max_ucb]
            )

    def _expansion(self, fen: str, node: MCTSNode) -> Tuple[MCTSNode, chess.Board]:
        board = chess.Board(fen)
        actions = self._get_actions(node)
        for action in actions:
            board.push(action)
        if node.ucb() < np.inf:
            if not board.is_game_over():
                node.add_children([move for move in board.legal_moves])
                node = random.choice(node.children)
                board.push(node.action)
        return node, board

    def _rollout(self, board: chess.Board) -> Tuple[float, int]:
        outcome = board.outcome()
        if outcome:
            return int(outcome.winner) if outcome.winner != None else 0, 0, []
        moves = []
        for i in itertools.count():
            if i < self.max_depth:
                move = random.choice([move for move in board.legal_moves])
                board.push(move)
                moves.append(move.uci())
                outcome = board.outcome()
                if outcome:
                    value = int(outcome.winner) if outcome.winner != None else 0
                    break
            else:
                value = self._estimate_value(board.fen())
                break
        return value, i, moves

    def _backpropogation(self, state_value: float, node: MCTSNode) -> MCTSNode:
        reward = {True: state_value, False: 1 - state_value}
        while True:
            node.update_score(reward[node.side])
            # print(node.action, "W" if node.side else "B", scores[node.side])
            if node.parent.action == None:
                node.parent.update_score(reward[node.parent.side])
                # print(
                #     node.parent.action,
                #     "W" if node.parent.side else "B",
                #     scores[node.parent.side],
                # )
                return node
            node = node.parent

    def _get_actions(self, node: MCTSNode) -> List[chess.Move]:
        # get a list of actions to execute in order to get to the state of a node
        actions = []
        while True:
            if node.parent == None:
                actions.reverse()
                return actions
            actions.append(node.action)
            node = node.parent

    @staticmethod
    def _estimate_value(fen: str) -> float:
        """Estimates the value of a observation by summing relative piece values and check_status"""
        check_penalty = 5
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
        board_pieces = fen.split(" ")[0]
        # eliminate empty spots
        board_pieces = "".join(char for char in board_pieces if not char.isdigit())
        board_pieces = board_pieces.replace("/", "")
        # convert to piece values
        board_piece_values = [piece_values[piece] for piece in board_pieces]
        reward = sum(board_piece_values)

        # rewards for check
        board = chess.Board(fen)
        if board.turn == chess.WHITE:
            reward -= check_penalty * board.is_check()
        else:
            reward += check_penalty * board.is_check()

        return 0.5 + (reward / reward_scaling_factor)

    def _save_chosen_node_children_to_tree(
        self, chosen_node: MCTSNode, fen_state_at_node: str
    ):
        for node in chosen_node.children:
            board = chess.Board(fen_state_at_node)
            board.push(node.action)
            self.tree[board.fen()] = node

    def __disabled_logging(self, *args, **kwargs) -> None:
        pass

    def __rollout_logging(
        self, count: int, duration: float, depth: int, reward: float
    ) -> None:
        logger.debug(
            f"Iterations: {count}  -  Last rollout stats - time: {duration:.4f}, depth: {depth}, reward: {reward:.4f}        "
        )

    def __move_logging(
        self,
        reason: str,
        result: chess.Move,
        iterations: int,
        max_visit: int,
        total_time: float,
        total_depth: int,
        fen_state_after_move: str,
    ) -> None:
        logger.info(
            f"MOVE - turn:{self.turn} reason:{reason} action:{result.uci()} iters:{iterations+1} max_visit:{max_visit} avg_rollout_time:{total_time/iterations:.4f} avg_depth:{total_depth/iterations:.4f} state:{fen_state_after_move}"
        )

    def __distribution_logging(self, root: MCTSNode, fen_state: str) -> None:
        distribution = pd.DataFrame(
            {
                "action": [child.action.uci() for child in root.children],
                "visits": [child.score["visits"] for child in root.children],
                "reward": [child.score["reward"] for child in root.children],
                "ucb": [child.ucb() for child in root.children],
            },
            columns=["turn", "state", "action", "visits", "reward", "ucb"],
        )
        distribution["turn"] = self.turn
        distribution["state"] = fen_state
        distribution.to_csv(
            "distribution.csv",
            mode="a",
            header=not os.path.exists("distribution.csv"),
            index=False,
        )

    def __tree_logging(self, root: MCTSNode, fen_initial_state: str):
        nodes_to_log = [(node, fen_initial_state) for node in root.children]
        logged_nodes = [
            {
                "node_state": fen_initial_state,
                "parent_state": None,
                "node_action": None,
                "visits": root.score["visits"],
                "total_reward": root.score["reward"],
                "ucb": None,
            }
        ]
        while len(nodes_to_log) > 0:
            child_nodes = []
            for node, parent_state in nodes_to_log:
                board = chess.Board(parent_state)
                board.push(node.action)
                node_state = board.fen()
                logged_nodes.append(
                    {
                        "node_state": node_state,
                        "parent_state": parent_state,
                        "node_action": node.action.uci(),
                        "visits": node.score["visits"],
                        "total_reward": node.score["reward"],
                        "ucb": node.ucb(),
                    }
                )
                child_nodes.extend([(node, node_state) for node in node.children])
            nodes_to_log = child_nodes
        tree_df = pd.DataFrame(logged_nodes)
        tree_df.to_csv(
            "tree.csv",
            mode="a",
            header=not os.path.exists("tree.csv"),
            index=False,
        )

    def __save_selected_path_to_mem(
        self,
        node: MCTSNode,
        rollout_moves: List[str],
        fen_final_state: str,
        reward: float,
    ):
        node_moves = []
        while node.action != None:
            node_moves.append(node.action.uci())
            node = node.parent
        node_moves.reverse()
        self._paths.append(
            {
                "node_path": node_moves,
                "rollout_path": rollout_moves,
                "final_state": fen_final_state,
                "value": reward,
            }
        )

    def __save_paths_to_file(self, fen_initial_state):
        tree_paths_df = pd.DataFrame(
            [{"initial_state": fen_initial_state, **path} for path in self._paths]
        )
        tree_paths_df.to_csv(
            "paths.csv",
            mode="a",
            header=not os.path.exists("paths.csv"),
            index=False,
        )
        self._paths = []


def render(board: chess.Board):
    print("-" * 20)
    print(board)
    print("-" * 20)
