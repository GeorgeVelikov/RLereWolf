from Werewolf.environment.WerewolfEnvironment import WerewolfEnvironemnt;
from Werewolf.game.Game import Game;
from Werewolf.agents.DummyPlayer import DummyPlayer;
from Werewolf.agents.TrainablePlayer import TrainablePlayer;
from Werewolf.agents.TrainablePlayerWrapper import TrainablePlayerWrapper;

import multiprocessing;
import logging;
import gym;
import ray;

def RunWerewolfEnvironment():
    game = Game("Training game", False);

    for i in range(70):
        TrainablePlayer("TBot-" + str(i), game);

    environment = WerewolfEnvironemnt(game);

    # wrapper over everything
    trainablePlayer = TrainablePlayerWrapper(game);

    trainablePlayer.Experiment(10, environment, True);
    print("\n" + str(environment.Statistics));

    return;

if __name__ == "__main__":
    numberOfCpuCores = multiprocessing.cpu_count();

    ray.init(local_mode=True,\
        logging_level = logging.WARN,\
        num_cpus = numberOfCpuCores);

    RunWerewolfEnvironment();
