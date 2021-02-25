class Vote():
    def __init__(self, player, votedPlayer):
        self.__player = player;
        self.__votedPlayer = votedPlayer;

    @property
    def Player(self):
        return self.__player;

    @property
    def VotedPlayer(self):
        return self.__votedPlayer;
