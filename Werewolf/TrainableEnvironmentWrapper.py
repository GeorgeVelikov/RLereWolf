import csv;
import itertools;
import random;
import sys;
from tqdm import tqdm;

from multiprocessing.pool import ThreadPool

class TrainableEnvironmentWrapper():
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

        allAgents = self.Game.AgentPlayers;
        allAgentIds = [a.Identifier for a in allAgents];

        self.__metrics = {k: 0 for k in allAgentIds};
        episodeMetrics = {k: 0 for k in allAgentIds};

        orderedTargets = [];

        loadingBar = tqdm(total = episodes);
        while episode < episodes:

            actions = [];

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

            # Sanity checks since we do work with "low-level" data in here, and may or may
            # not get nulls, depending on our agent type. "Logically safer" agents will put
            # Nones as their action, i.e. they cannot do anything, whereas a "Wait" action
            # is a vote directed to no one, this is a bit of a bad design choice and would
            # ideally be replaced by some class Action which can then be inherited by
            # Wait/Vote/Divine etc. However, time for the project didn't allow gold plating
            actions = [a for a in actions if a != None];

            observations, rewards, dones, info = environment.step(actions);

            for agentId in allAliveAgentIds:
                self.__metrics[agentId] += rewards[agentId];
                episodeMetrics[agentId] += rewards[agentId];

            # all players are "done"
            if all(dones.values()):
                observations = environment.reset();
                episode += 1;
                loadingBar.update(1);

                episodeMetrics = {k: 0 for k in allAgentIds};

        loadingBar.close();
        return [environment.NumberOfAgents, isRandom], self.__metrics;

    def SaveMetrics(self, metrics):
        headers = ["header 1", "header 2"];
        rows = [headers]

        # add a csv row
        for k, v in self.metrics.items():
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
