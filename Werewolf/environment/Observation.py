class Observation():
    def __init__(self, role, players, time, votes, messages):
        self.__role = role;
        self.__players = players;
        self.__time = time;
        self.__votes = votes;
        self.__messages = messages;

    @property
    def Role(self):
        return self.__role;

    @property
    def Players(self):
        return self.__players;

    @property
    def Time(self):
        return self.__time;

    @property
    def Votes(self):
        return self.__votes;

    @property
    def Messages(self):
        return self.__messages;
