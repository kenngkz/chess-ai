import chess as pychess
import random
from typing import Union

import utils

#######################
###   Environment   ###
#######################

class ChessEnv:

    def __init__(self):
        ''' Initialization '''
        self.board = None
        self.last_reward = None
        self.done = True

    @classmethod
    def load(cls, state):
        ''' Load env from EnvState file or EnvState dict '''
        env = cls()
        env.set_state(state)
        return env

    def get_state(self):
        ''' Returns a EnvState dict '''
        envstate = {
            "fen": self.board.fen(),
            "last_reward": self.last_reward,
            # add statistics?
        }
        return envstate

    def set_state(self, state:Union[str, dict]):
        ''' Set Env to given EnvState '''
        if isinstance(state, str):  # then filepath
            with open(state, "r") as f:
                state = eval(f.read())
        if isinstance(state, dict):
            self.board = pychess.Board(state["fen"])
            self.action_space = [move for move in self.board.legal_moves]
            self.done = self.board.outcome() != None
            self.last_reward = state["last_reward"]
            self.player_to_move = self.board.turn
            return utils.parse_fen(self.board.fen())
        else: print(f"Invalid state arg type: {type(state)}")

    def copy(self):
        env = ChessEnv()
        env.set_state(self.get_state())
        return env

    def reset(self):
        ''' Resets the env and returns the starting obs'''
        self.board = pychess.Board()
        self.action_space = [move for move in self.board.legal_moves]
        self.done = False
        self.last_reward = None
        self.player_to_move = self.board.turn
        return utils.parse_fen(self.board.fen())

    def step(self, action):
        ''' Take a single action in the environment. Returns obs, reward, done, info '''
        assert action in self.action_space, f"Action {action} not in action_space"
        assert not self.done, "Environment is completed. Run .reset() to reset the environment"
        self.board.push(action)
        self.player_to_move = self.board.turn
        self.action_space = [move for move in self.board.legal_moves]
        obs = utils.parse_fen(self.board.fen())
        outcome = self.board.outcome()
        if outcome:
            self.done = True
            if outcome.winner == (not self.board.turn): 
                self.last_reward = 1
            elif outcome.winner == None:
                self.last_reward = 0.5
            else:
                self.last_reward = 0
        return obs, self.last_reward, self.done, None

    def sample_action(self):
        ''' Return a random action from action space '''
        return random.choice(self.action_space)

    def render(self):
        ''' Renders the board position on console '''
        print("-"*20)
        print(self.board)
        print("-"*20)
'''
EnvState dict format (file is saved in json format)
{
    fen: "${fen-string}",
    last_reward: int,
}
'''

if __name__ == "__main__":
    from archive.agent import MCTSAgent, RandomAgent

    env = ChessEnv()
    obs = env.reset()
    done = False

    for i in range(40):
        action = env.sample_action()
        obs, reward, done, info = env.step(action)
    
    white = MCTSAgent(env, show=1, time_limit=20, explore_param=0.5, max_depth=250)
    black = RandomAgent(env)
    env.render()

    for i in range(10):
        # set player
        player = white if env.player_to_move else black

        # get action and step
        action = player.pred(obs)
        print(action)
        obs, reward, done, info = env.step(action)
        env.render()

        if done:
            break