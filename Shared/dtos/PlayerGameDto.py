class PlayerGameDto():
    def __init__(self, player, gameIdentifier, lastUpdatedUtc):
        self.__player = player;
        self.__gameIdentifier = gameIdentifier;
        self.__lastUpdatedUtc = lastUpdatedUtc;

    @property
    def Player(self):
        return self.__player;

    @property
    def GameIdentifier(self):
        return self.__gameIdentifier;

    @property
    def LastUpdatedUtc(self):
        return self.__lastUpdatedUtc;
