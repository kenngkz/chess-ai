from abc import ABC, abstractmethod
import random

class Agent(ABC):
    ''' Abstract class to define a template for agents '''
    
    @abstractmethod
    def pred(self, obs):
        pass

class RandomAgent(Agent):

    def pred(self, obs):
        return random.choice(obs)