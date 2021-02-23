class GameDto():
    def __init__(self, identifier, hasStarted, name, messages, players, timeOfDay):
        self.__identifier = identifier
        self.__hasStarted = hasStarted;
        self.__name = name;
        self.__messages = messages;
        self.__players = players;
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
    def Players(self):
        return self.__players;

    @property
    def TimeOfDay(self):
        return self.__timeOfDay;
