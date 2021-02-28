class GameActionDto():
    def __init__(self, player, targetPlayer, actionType, additionalData = None):
        self.__player = player;
        self.__targetPlayer = targetPlayer;
        self.__actionType = actionType;
        self.__additionalData = additionalData;

    @property
    def Player(self):
        return self.__player;

    @property
    def TargetPlayer(self):
        return self.__targetPlayer;

    @property
    def ActionType(self):
        return self.__actionType;

    @property
    def AdditionalData(self):
        return self.__additionalData;
