class TalkMessage():
    def __init__(self, messageName, messageTemplate, playerType, isRoleBased):
        self.__messageName = messageName;
        self.__messageTemplate = messageTemplate;
        self.__playerType = playerType;
        self.__isRoleBased = isRoleBased;

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
