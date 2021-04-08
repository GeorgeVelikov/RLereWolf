class AddAgentGameDto():
    def __init__(self, player, gameIdentifier, agentType):
        self.__player = player;
        self.__gameIdentifier = gameIdentifier;
        self.__agentType = agentType;

    @property
    def Player(self):
        return self.__player;

    @property
    def GameIdentifier(self):
        return self.__gameIdentifier;

    @property
    def AgentType(self):
        return self.__agentType;
