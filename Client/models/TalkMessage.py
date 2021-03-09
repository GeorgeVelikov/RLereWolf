class TalkMessage():
    def __init__(self, messageTemplate, playerType):
        self.__messageTemplate = messageTemplate;
        self.__playerType = playerType;

    @property
    def MessageTemplate(self):
        return self.__messageTemplate;

    @property
    def PlayerType(self):
        return self.__playerType;
