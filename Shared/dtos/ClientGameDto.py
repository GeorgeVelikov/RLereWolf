class ClientGameDto():
    def __init__(self, client, gameIdentifier):
        self.__client = client;
        self.__gameIdentifier = gameIdentifier;

    @property
    def Client(self):
        return self.__client;

    @property
    def GameIdentifier(self):
        return self.__gameIdentifier;
