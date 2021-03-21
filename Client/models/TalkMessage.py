class TalkMessage():
    def __init__(self, messageName, messageTemplate, playerType, isRoleBased, messageType):
        self.__messageName = messageName;
        self.__messageTemplate = messageTemplate;
        self.__playerType = playerType;
        self.__isRoleBased = isRoleBased;
        self.__messageType = messageType;

    @property
    def MessageName(self):
        return self.__messageName;

    @property
    def MessageTemplate(self):
        return self.__messageTemplate;

    @property
    def PlayerType(self):
        return self.__playerType;

    @property
    def IsRoleBased(self):
        return self.__isRoleBased;

    @property
    def MessageType(self):
        return self.__messageType;
