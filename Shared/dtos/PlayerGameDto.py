class PlayerGameDto():
    def __init__(self, player, game):
        self.__player = player;
        self.__game = game;

    @property
    def Player(self):
        return self.__player;

    @property
    def Game(self):
        return self.__game;