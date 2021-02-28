class GameActionDto():
    def __init__(self, gameIdentifier, player, targetPlayerIdentifier, additionalData = None):
        self.__gameIdentifier = gameIdentifier;
        self.__player = player;
        self.__targetPlayerIdentifier = targetPlayerIdentifier;
        self.__additionalData = additionalData;

    @property
    def GameIdentifier(self):
        return self.__gameIdentifier;

    @property
    def Player(self):
        return self.__player;

    @property
    def TargetPlayerIdentifier(self):
        return self.__targetPlayerIdentifier;

    @property
    def AdditionalData(self):
        return self.__additionalData;
