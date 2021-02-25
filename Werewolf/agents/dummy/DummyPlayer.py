from Werewolf.game.Player import Player;

class DummyPlayer(Player):
    def __init__(self, name, game):
        super().__init__(name);
        self.__game = game;

    @property
    def Game(self):
        return self.__game;

    def ActDay(self):
        raise NotImplementedError("Act Day has not been implemented for this dummy agent type.");
        return;

    def ActNight(self):
        raise NotImplementedError("Act Night has not been implemented for this dummy agent type.");
        return;