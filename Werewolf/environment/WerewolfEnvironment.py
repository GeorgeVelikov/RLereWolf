from Werewolf.game.Game import Game;
from Werewolf.environment.Observation import Observation;
from Werewolf.environment.Statistics import Statistics;
from Werewolf.environment.TrainingRewards import TrainingRewards;

from Shared.enums.PlayerTypeEnum import PlayerTypeEnum;
from Shared.enums.TimeOfDayEnum import TimeOfDayEnum;
from Shared.enums.FactionTypeEnum import FactionTypeEnum;
from Shared.enums.VoteResultTypeEnum import VoteResultTypeEnum;

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

    def render(self):
        # probably not worth doing
        pass;

    def step(self, agentActions):

        agentPlayerIdentifiers = [ap.Identifier for ap in self.game.AgentPlayers];
        rewards = {id: 0 for id in agentPlayerIdentifiers};

        if self.game.TimeOfDay == TimeOfDayEnum.Day:
            shouldForceGameStep = False;

            for action in agentActions:
                actionResult = self.game.VoteDay(action);

                if actionResult == VoteResultTypeEnum.InvalidAction:
                    # player cannot vote, likely attempted to vote more than once
                    shouldForceGameStep = True;
                    rewards[action.Player.Identifier] += TrainingRewards.IncorrectAction;
                elif actionResult == VoteResultTypeEnum.DeadPlayerTargeted:
                    # dead player target
                    shouldForceGameStep = True;
                    rewards[action.Player.Identifier] += TrainingRewards.DeadPlayerTargeted;
                elif actionResult == VoteResultTypeEnum.WaitAction:
                    # waited
                    rewards[action.Player.Identifier] += TrainingRewards.Wait;
                elif actionResult == VoteResultTypeEnum.SuccessfulAction:
                    # voted
                    rewards[action.Player.Identifier] += TrainingRewards.Vote;

            if shouldForceGameStep:
                self.game.CountVotesExecute();

        if self.game.TimeOfDay == TimeOfDay.Night:
            shouldForceGameStep = False;

            for action in agentActions:
                actionResult = self.game.VoteNight(action);

                if actionResult == VoteResultTypeEnum.CannotActDuringTimeOfDay:
                    # role cannot act during the night
                    shouldForceGameStep = True;
                    rewards[action.Player.Identifier] += TrainingRewards.CannotActDuringTimeOfDay;
                elif actionResult == VoteResultTypeEnum.InvalidAction:
                    # player cannot vote, likely attempted to vote more than once
                    shouldForceGameStep = True;
                    rewards[action.Player.Identifier] += TrainingRewards.IncorrectAction;
                elif actionResult == VoteResultTypeEnum.DeadPlayerTargeted:
                    # dead player target
                    shouldForceGameStep = True;
                    rewards[action.Player.Identifier] += TrainingRewards.DeadPlayerTargeted;
                elif actionResult == VoteResultTypeEnum.WerewolfCannibalism:
                    # werewolf attacking werewolf
                    rewards[action.Player.Identifier] += TrainingRewards.WerewolfCannibalism;

                elif actionResult == VoteResultTypeEnum.WaitAction:
                    # waited
                    rewards[action.Player.Identifier] += TrainingRewards.Wait;
                elif actionResult == VoteResultTypeEnum.SuccessfulAction:
                    # voted
                    rewards[action.Player.Identifier] += TrainingRewards.Vote;

            if shouldForceGameStep:
                self.game.CountNightVotesAndEvents();

            # bump everyone's rewards for surviving the day
            rewards = {id: value + TrainingRewards.DayPassed\
                for id, value in rewards.items()};

        dones, rewards = self.check_done(rewards);
        observations = self.observe();
        info = None;

        gameIsOver, winningFaction = self.CheckWinCondition();

        if gameIsOver:

            if winningFaction == FactionTypeEnum.Villagers:
                pass;

            if winningFaction == FactionTypeEnum.Werewolves:
                pass;

            pass;

        return observations, rewards, dones, info;

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
