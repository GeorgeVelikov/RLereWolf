from Werewolf.environment.WerewolfEnvironment import WerewolfEnvironemnt;
from Werewolf.game.Game import Game;
from Werewolf.agents.DummyPlayer import DummyPlayer;
from Werewolf.agents.RuleBasedPlayer import RuleBasedPlayer;
from Werewolf.agents.TrainablePlayer import TrainablePlayer;
from Werewolf.TrainableEnvironmentWrapper import TrainableEnvironmentWrapper;

import multiprocessing;
import logging;
import gym;
import ray;
import pprint;

def RunWerewolfEnvironment():
    game = Game("Training game", False);

    for i in range(5):
        TrainablePlayer("TBot-" + str(i), game);

    environment = WerewolfEnvironemnt(game);

    # wrapper over everything
    trainablePlayer = TrainableEnvironmentWrapper(game);

    generalInfo, metrics = trainablePlayer.Experiment(1000, environment, True);
    print("\n" + str(environment.Statistics));

    print("\n");
    pprint.pprint(metrics, width = 1);

    return;

if __name__ == "__main__":
    numberOfCpuCores = multiprocessing.cpu_count();

    ray.init(local_mode=True,\
        logging_level = logging.WARN,\
        num_cpus = numberOfCpuCores);

    RunWerewolfEnvironment();
