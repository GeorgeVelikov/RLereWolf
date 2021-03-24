from Werewolf.game.Game import Game;
from Werewolf.environment.Observation import Observation;
from Werewolf.environment.Statistics import Statistics;
from Werewolf.environment.TrainingRewards import TrainingRewards;

from Shared.enums.PlayerTypeEnum import PlayerTypeEnum;

import gym;
import numpy;
import random;

from ray.rllib import MultiAgentEnv;
from ray.rllib.env import EnvContext;

class WerewolfEnvironemnt(gym.Wrapper):
    def __init__(self, game):
        # the environment itself will host a game
        self.game = game;

        self.__numberOfAgents = len(self.game.AgentPlayers);
        self.__totalEpisodeReward = [0 for _ in range(self.__numberOfAgents)]
        self.__stepCount = int();

        self.staitistics = Statistics();

        self.__roles = PlayerTypeEnum.Values();
        roleCount = len(self.__roles);

        self.observation_space = gym.spaces.Dict(
            dict(
                AgentRole = gym.spaces.Discrete(roleCount),
                Day = gym.spaces.Discrete(100),
                StatusMap = gym.spaces.MultiBinary(self.__numberOfAgents),
                Votes = gym.spaces.Box(
                    low = -1,
                    high = self.__numberOfAgents,
                    shape = (self.__numberOfAgents, ))
            )
        );

        self.action_space = gym.spaces.Discrete(self.__numberOfAgents);

        x = 1;


    def render(self):
        # probably not worth doing
        pass;

    def step(self, agentActions):
        self.__stepCount += 1;

        action = agentActions[0];
        observation, reward, done, info = self.env.step(action);

        done = False;

        if self.env._elapsed_steps == (self.env._max_episode_steps - 1)\
            or self.game.CheckWinCondition():

            done = True;

        self.__totalEpisodeReward[0] += reward;

        return [observation], [reward], [done], info;

        pass;

    def observe(self):

        observations = {};

        agents = self.game.AgentPlayers;
        aliveAgents = [a for a in agents if a.IsAlive];

        for agent in aliveAgents:
            observations[agent.Identifier] = Observation(\
                agent.Role.Type,\
                self.game.Players,\
                self.game.TimeOfDay,\
                self.game.Votes,\
                self.game.Messages);

        return observations;

    def reset(self):
        self.game.Restart();
        return self.observe();
