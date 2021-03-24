from Werewolf.environment.WerewolfEnvironment import WerewolfEnvironemnt;
from Werewolf.game.Game import Game;
from Werewolf.agents.DummyPlayer import DummyPlayer;

import gym;

def RunWerewolfEnvironment():
    game = Game("Training game");

    for i in range (10):
        DummyPlayer("bot-" + str(i), game);

    environment = WerewolfEnvironemnt(game);

    return;

if __name__ == "__main__":
    RunWerewolfEnvironment();
