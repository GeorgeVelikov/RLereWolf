from Werewolf.game.Game import Game;
from Werewolf.environment.MultiAgentActionSpace import MultiAgentActionSpace;
from Werewolf.environment.MultiAgentObservationSpace import MultiAgentObservationSpace;

import gym;
import numpy;
import random;

class WerewolfEnvironemnt(gym.Wrapper):
    def __init__(self, game):
        super().__init__(gym.make("Werewolf Environment - " + game.Name));

        # the environment itself will host a game
        self.game = game;

        self.__numberOfAgents = int();
        self.__stepCount = int();
        self.__totalEpisodeReward = None;
        self.reset();

        self.action_space = MultiAgentActionSpace([self.env.action_space]);
        self.observation_space = MultiAgentObservationSpace([self.env.observation_space]);

    def render(self):
        # probably not worth doing
        pass;

    def step(self, agentActions):
        self.__stepCount += 1;

        action = agentActions[0];
        observation, reward, done, info = self.env.step(action);

        done = self.game.CheckWinCondition();

        self.__totalEpisodeReward[0] += reward;

        return [observation], [reward], [done], info;

        pass;

    def reset(self):
        self.game.Restart();

        self.__numberOfAgents = len(game.AgentPlayers);
        self.__totalEpisodeReward = [0 for _ in range(self.__numberOfAgents)]
        self.__stepCount = int();

        observations = self.env.reset();

        return [observations];
