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
        raise NotImplementedError("Act Day has not been implemented for this agent type.");
        return;

    def ActNight(self):
        raise NotImplementedError("Act Night has not been implemented for this agent type.");
        return;

    def PreGameSetup(self):
        raise NotImplementedError("Pre Game Setup has not been implemented for this agent type.");
        return;

    def PostGameSetup(self):
        raise NotImplementedError("Post Game Setup has not been implemented for this agent type.");
        return;

    def Talk(self):
        raise NotImplementedError("Talk has not been implemented for this agent type.");
        return;

    def Sway(self):
        raise NotImplementedError("Sway has not been implemented for this agent type.");
        return;
