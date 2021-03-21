class MessageMetaDataDto():
    def __init__(self, authorIdentifier, targetIdentifier, targetRole, messageType):
        self.__authorIdentifier = authorIdentifier;
        self.__targetIdentifier = targetIdentifier;
        self.__targetRole = targetRole;
        self.__messageType = messageType;

    @property
    def AuthorIdentifier(self):
        return self.__authorIdentifier;

    @property
    def TargetIdentifier(self):
        return self.__targetIdentifier;

    @property
    def TargetRole(self):
        return self.__targetRole;

    @property
    def MessageType(self):
        return self.__messageType;
