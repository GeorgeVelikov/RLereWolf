class CreateGameDto():
    def __init__(self, player, gameName):
        self.__player = player;
        self.__name = gameName;

    @property
    def Player(self):
        return self.__player;

    @property
    def Name(self):
        return self.__name;
