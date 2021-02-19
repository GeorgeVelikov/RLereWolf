import Shared.constants.GameConstants as GameConstants;

class GameListDto():
    def __init__(self, identifier, name, players):
        self.__identifier = identifier;
        self.__name = name;
        self.__players = players;

    @property
    def Identifier(self):
        return self.__identifier;

    @property
    def Name(self):
        return self.__name;

    @property
    def Players(self):
        return str(self.__players) + "/" + str(GameConstants.MAXIMUM_PLAYER_COUNT);
