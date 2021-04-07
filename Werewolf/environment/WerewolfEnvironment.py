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
import csv;
import os;

from ray.rllib import MultiAgentEnv;
from ray.rllib.env import EnvContext;

class WerewolfEnvironemnt(gym.Wrapper):
    def __init__(self, game):
        # the environment itself will host a game
        self.game = game;

        self.__numberOfAgents = len(self.game.AgentPlayers);
        self.__totalEpisodeReward = [0 for _ in range(self.__numberOfAgents)]
        self.__stepCount = int();

        self.__instanceStatistics = Statistics();
        self.__statistics = Statistics();

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

    @property
    def Game(self):
        return self.game;

    @property
    def InstanceStatistics(self):
        return self.__instanceStatistics;

    @property
    def Statistics(self):
        return self.__statistics;

    @property
    def NumberOfAgents(self):
        return self.__numberOfAgents;

    def render(self):
        # probably not worth doing
        pass;

    def step(self, agentActions):

        agents = self.game.AgentPlayers;
        agentPlayerIdentifiers = [ap.Identifier for ap in agents];
        rewards = {id: 0 for id in agentPlayerIdentifiers};

        if self.game.TimeOfDay == TimeOfDayEnum.Day:
            shouldForceGameStep = False;

            for action in agentActions:
                actionResult = self.game.VoteDay(action);

                if actionResult == VoteResultTypeEnum.InvalidAction:
                    # player cannot vote, likely attempted to vote more than once
                    shouldForceGameStep = True;
                    rewards[action.Player.Identifier] += TrainingRewards.IncorrectAction;
                    self.InstanceStatistics.IncorrectAction += 1;
                elif actionResult == VoteResultTypeEnum.DeadPlayerTargeted:
                    # dead player target
                    shouldForceGameStep = True;
                    rewards[action.Player.Identifier] += TrainingRewards.DeadPlayerTargeted;
                    self.InstanceStatistics.DeadAgentVoted += 1;
                elif actionResult == VoteResultTypeEnum.WaitAction:
                    # waited
                    rewards[action.Player.Identifier] += TrainingRewards.Wait;
                elif actionResult == VoteResultTypeEnum.SuccessfulAction:
                    # voted
                    rewards[action.Player.Identifier] += TrainingRewards.Vote;

            if shouldForceGameStep:
                self.game.CountVotesExecute();

        elif self.game.TimeOfDay == TimeOfDayEnum.Night:
            shouldForceGameStep = False;

            for action in agentActions:
                actionResult = self.game.VoteNight(action);

                if actionResult == VoteResultTypeEnum.CannotActDuringTimeOfDay:
                    # role cannot act during the night
                    shouldForceGameStep = True;
                    rewards[action.Player.Identifier] += TrainingRewards.IncorrectAction;
                    self.InstanceStatistics.IncorrectAction += 1;
                elif actionResult == VoteResultTypeEnum.InvalidAction:
                    # player cannot vote, likely attempted to vote more than once
                    shouldForceGameStep = True;
                    rewards[action.Player.Identifier] += TrainingRewards.IncorrectAction;
                    self.InstanceStatistics.IncorrectAction += 1;
                elif actionResult == VoteResultTypeEnum.DeadPlayerTargeted:
                    # dead player target
                    shouldForceGameStep = True;
                    rewards[action.Player.Identifier] += TrainingRewards.DeadPlayerTargeted;
                    self.InstanceStatistics.DeadAgentAttacked += 1;
                elif actionResult == VoteResultTypeEnum.WerewolfCannibalism:
                    # werewolf attacking werewolf
                    rewards[action.Player.Identifier] += TrainingRewards.WerewolfCannibalism;
                    self.InstanceStatistics.TeammateAttacked += 1;

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

            self.InstanceStatistics.TotalDays += 1;

        # done if you're dead

        gameIsOver, winningFaction = self.game.CheckWinCondition();

        dones = {};

        if gameIsOver:
            dones = {a.Identifier: True for a in agents};
            self.InstanceStatistics.TotalGames += 1;

            villagers = [a for a in agents\
                if a.Role == PlayerTypeEnum.Villager\
                    or a.Role == PlayerTypeEnum.Guard\
                    or a.Role == PlayerTypeEnum.Seer];

            werewolves = [a for a in agents\
                if a.Role == PlayerTypeEnum.Werewolf];

            if winningFaction == FactionTypeEnum.Villagers:
                for villager in villagers:
                    rewards[villager.Identifier] += TrainingRewards.Victory;

                for werewolf in werewolves:
                    rewards[werewolf.Identifier] += TrainingRewards.Lost;

                self.InstanceStatistics.VillagerWins += 1;
                pass;

            if winningFaction == FactionTypeEnum.Werewolves:
                for villager in villagers:
                    rewards[villager.Identifier] += TrainingRewards.Lost;

                for werewolf in werewolves:
                    rewards[werewolf.Identifier] += TrainingRewards.Victory;

                self.InstanceStatistics.WerewolfWins += 1;
                pass;

            pass;
        else:
            dones = {a.Identifier: not a.IsAlive for a in agents};

        observations = self.observe();
        info = None;

        return observations, rewards, dones, info;

    def observe(self):

        observations = {};

        agents = self.game.AgentPlayers;
        aliveAgents = [a for a in agents if a.IsAlive];

        for agent in aliveAgents:
            observations[agent.Identifier] = Observation(\
                agent.Role.Type if agent.Role else None,\
                self.game.Players,\
                self.game.TimeOfDay,\
                self.game.Votes,\
                self.game.Messages);

        return observations;

    def reset(self):
        self.game.Restart();
        self.game.Start();
        self.saveStatistics();

        self.Statistics.DeadAgentVoted += self.InstanceStatistics.DeadAgentVoted;
        self.Statistics.DeadAgentAttacked += self.InstanceStatistics.DeadAgentAttacked;
        self.Statistics.TeammateAttacked += self.InstanceStatistics.TeammateAttacked;
        self.Statistics.IncorrectAction += self.InstanceStatistics.IncorrectAction;
        self.Statistics.WerewolfWins += self.InstanceStatistics.WerewolfWins;
        self.Statistics.VillagerWins += self.InstanceStatistics.VillagerWins;
        self.Statistics.TotalDays += self.InstanceStatistics.TotalDays;
        self.Statistics.TotalGames += self.InstanceStatistics.TotalGames;

        self.__instanceStatistics = Statistics();
        return self.observe();

    def saveStatistics(self):
        if self.InstanceStatistics.TotalGames == 0:
            return;

        statisticsDict = {attr: getattr(self.InstanceStatistics, attr)\
           for attr in self.InstanceStatistics.__dict__};

        headers = [propertyName for propertyName, propertyValue in statisticsDict.items()];

        fileName = "Statistics.csv";
        with open(fileName, "a+", newline = str()) as file:
            writer = csv.DictWriter(file,\
               fieldnames = headers,\
               delimiter=",",\
               lineterminator="\n");

            file.seek(0, 2);

            if file.tell() == 0:
                writer.writeheader();

            writer.writerow(statisticsDict);

        return;
