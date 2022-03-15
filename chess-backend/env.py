from game import Game, GameState
from agent import RandomAgent
import utils

import time
import os
import random

clear_console = lambda: os.system("cls")

class ChessEnv:
    '''
    Chess-v0

    observation structure: list of len 71
        - 1 entry specifying the player to move: 1 for white and -1 for black
        - 64 entries specifying the piece index in each cell (order: row1col1, row1col2, ...)
        - 4 entries specifying the castle status (whether castling is allowed for each castle type)
            - order: black queenside, black queenside, white queenside, white kingside
        - 2 entries specifying whether each side is under check (order: white, black)

    Note: initialization arg white and black not used.
    '''

    def __init__(self, white=None, black=None):
        ''' Initialization. player=1 if human player is white, -1 if black. player not required if opponent=None '''
        self.game = None
        self.done = True
        self.last_reward = None
        # built-in opponents
        built_in_opp = {"random":RandomAgent}
        self.players = {}
        players = {-1:black, 1:white}
        for side, agent in players.items():
            if isinstance(agent, str):
                if not agent in built_in_opp:
                    print(f"Warning: Agent {agent} with side {side} not in built-in opponents. Default to None")
                    agent = None
                else:
                    agent = built_in_opp.get(agent)()  # initialize the built-in opponent
            self.players[side] = agent


    @classmethod
    def load(cls, filepath, white=None, black=None):
        ''' Load env from gamestate save file. Players must be specified if not None '''
        gamestate = GameState.load(filepath)
        env = cls(white, black)
        env.set_state(gamestate)
        return env

    def reset(self):
        ''' Resets the env and returns the starting obs'''
        self.game = Game()
        self.game.all_legal_moves()
        self.action_space = self.game.legal_moves[self.game.player_to_move]
        self.done = False
        self.last_reward = None
        return tuple([self.game.player_to_move, *self.game.board.to_arr().flatten(), *list(self.game.castle_status.values()), *self.game.check_status.values()])

    def step(self, action):
        ''' Take a single action in the environment '''
        assert action in self.action_space, f"Action {action} not in action_space"
        assert not self.done, "Environment is completed. Run .reset() to reset the environment"
        self.game.make_move(action, permanent=True)
        self.game.all_legal_moves()
        self.action_space = self.game.legal_moves[self.game.player_to_move]
        obs = tuple([self.game.player_to_move, *self.game.board.to_arr().flatten(), *list(self.game.castle_status.values()), *self.game.check_status.values()])
        game_over = self.game.game_over()
        self.done = game_over != None
        reward = 0 if game_over==None else 0.5*(self.game.player_to_move*game_over+1)
        self.last_reward = reward
        return obs, reward, self.done, None

    def set_state(self, gamestate:"GameState"):
        ''' Set the game to a specified gamestate '''
        self.game = Game.load(gamestate)
        self.game.all_legal_moves()
        self.action_space = self.game.legal_moves[self.game.player_to_move]
        self.done = self.game.game_over() != None

    def get_state(self):
        ''' Gets the gamestate '''
        return self.game.get_state()

    def render(self, delay=0, clear=False):
        ''' Prints the board position in console '''
        if clear:
            clear_console()  # execute system call to clear console
        print(f"Turn {self.game.move_counter}")
        print(self.game.board)
        time.sleep(delay)

    def render_actions(self):
        ''' Prints the legal moves in console '''
        for i, move in enumerate(self.action_space):
            print(f"{i} - {move}")

    def save(self, filename, folder=None):
        ''' Saves a GameState file at filepath. Returns GameState if filepath is not provided. '''
        gamestate = GameState(self.game)
        gamestate.save(filename, folder)

    def sample_action(self):
        return random.choice(self.action_space)

    def copy(self):
        gamestate = self.get_state()
        new_env = ChessEnv(self.players[1], self.players[-1])
        new_env.set_state(gamestate)
        return new_env