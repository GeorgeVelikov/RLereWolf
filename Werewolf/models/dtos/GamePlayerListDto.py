class GamePlayerListDto():
    def __init__(self, gameIdentifier, players = dict()):
        self.__gameIdentifier = gameIdentifier;
        self.__players = players;

    @property
    def GameIdentifier(self):
        return self.__gameIdentifier;

    @property
    def Players(self):
        return self.__players;
