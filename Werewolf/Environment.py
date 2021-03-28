from Werewolf.environment.WerewolfEnvironment import WerewolfEnvironemnt;
from Werewolf.game.Game import Game;
from Werewolf.agents.DummyPlayer import DummyPlayer;

import multiprocessing;
import logging;
import gym;
import ray;

def RunWerewolfEnvironment():
    game = Game("Training game", False);

    for i in range (10):
        DummyPlayer("bot-" + str(i), game);

    environment = WerewolfEnvironemnt(game);

    return;

if __name__ == "__main__":
    numberOfCpuCores = multiprocessing.cpu_count();

    ray.init(local_mode=True,\
        logging_level = logging.WARN,\
        num_cpus = numberOfCpuCores);

    RunWerewolfEnvironment();
