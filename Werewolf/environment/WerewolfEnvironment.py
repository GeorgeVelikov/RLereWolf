from Werewolf.game.Game import Game;

import gym;
import numpy;
import random;

class WerewolfEnvironemnt(gym.Env):
    def __init__(self):
        self.action_space = gym.spaces.Discrete(6);

        # the environment itself will host a game
        self.game = Game("Werewolf Environment");

        return self.game, reward, self.game.CheckWinCondition(), info;

    def render(self):
        pass;

    def step(self):
        # probably not worth doing, should be able to reuse the client
        pass;

    def reset(self):
        self.game.Restart();

        return self.game;
