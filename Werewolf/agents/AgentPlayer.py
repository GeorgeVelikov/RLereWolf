from Werewolf.game.Player import Player;

class AgentPlayer(Player):
    def __init__(self, name, game):
        super().__init__("[AI] " + name);
        self.__game = game;

        self.__game.Join(self);
        self._Player__isReady = True;

    @property
    def Game(self):
        return self.__game;

    def ActDay(self):
        raise NotImplementedError("Act Day has not been implemented for this dummy agent type.");
        return;

    def ActNight(self):
        raise NotImplementedError("Act Night has not been implemented for this dummy agent type.");
        return;
