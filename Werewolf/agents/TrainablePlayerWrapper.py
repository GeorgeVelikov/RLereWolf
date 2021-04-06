import csv;
import itertools;
import random;
import sys;

from multiprocessing.pool import ThreadPool

class TrainablePlayerWrapper():
    def __init__(self, game):
        self.__game = game;
        self.__metrics = {};

    @property
    def Game(self):
        return self.__game;

    def Experiment(self, episodes, environment, isRandom):
        observations = environment.reset();

        episode = 0;
        actionSpace = environment.action_space;

        orderedTargets = [];
        metrics = [];

        while episode < episodes:

            actions = [];

            allAgents = self.Game.AgentPlayers;
            allAliveAgents = [a for a in allAgents if a.IsAlive];
            allAliveAgentIds = [a.Identifier for a in allAliveAgents];

            if isRandom:
                # just a random action
                actions = [agent.Act() for agent in allAliveAgents];
            else:
                # get list of people to target
                actions, orderedTargets = None;

            for index, identifier in enumerate(observations.keys()):
                pass;

            observations, rewards, dones, info = environment.step(actions);

            # all players are "done"
            if all(dones.values()):
                observations = environment.reset();
                episode += 1;

        return [environment.NumberOfAgents, isRandom], metrics;

    def SaveMetrics(self):
        headers = ["header 1", "header 2"];
        rows = [headers]

        # add a csv row
        for k, v in self.__metrics.items():
            pass;

        with open("metrics - " + str(self.Game), "w") as file:
            wr = csv.writer(file, dialect='excel')
            wr.writerows(rows)

        return;

    def TuneMetrics(self, combinations):

        for combination in combinations:
            pass;

        results = {};
        metrics = {};

        # merge metrics coming from the same settings
        for k, v in results:

            if k not in metrics.keys():
                metrics[k] = []

            metrics[k] += v

        # reformat
        metrics = {tuple[0]: tuple[1] for tuple in res}

        return metrics;
