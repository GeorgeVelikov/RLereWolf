class PlayerGameDto():
    def __init__(self, player, gameIdentifier):
        self.__player = player;
        self.__gameIdentifier = gameIdentifier;

    @property
    def Player(self):
        return self.__player;

    @property
    def GameIdentifier(self):
        return self.__gameIdentifier;
