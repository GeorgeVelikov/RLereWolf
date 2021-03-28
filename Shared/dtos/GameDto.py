import Shared.constants.GameConstants as GameConstants;

class GameDto():
    def __init__(self, identifier, hasStarted, name, messages, votes, players, turn, timeOfDay):
        self.__identifier = identifier
        self.__hasStarted = hasStarted;
        self.__name = name;
        self.__messages = messages;
        self.__votes = votes;
        self.__players = players;
        self.__turn = turn;
        self.__timeOfDay = timeOfDay;

    @property
    def Identifier(self):
        return self.__identifier;

    @property
    def HasStarted(self):
        return self.__hasStarted;

    @property
    def Name(self):
        return self.__name;

    @property
    def Messages(self):
        return self.__messages;

    @property
    def Votes(self):
        self.__votes;

    @property
    def Players(self):
        return self.__players;

    @property
    def Turn(self):
        return self.__turn;

    @property
    def TimeOfDay(self):
        return self.__timeOfDay;

    @property
    def PlayersCount(self):
        return str(len(self.__players)) + "/" + str(GameConstants.MAXIMUM_PLAYER_COUNT);

