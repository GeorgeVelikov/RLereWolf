class ConnectDto():
    def __init__(self, name, identifier):
        self.__clientIdentifier = identifier;
        self.__clientName = name;

    @property
    def ClientIdentifier(self):
        return self.__clientIdentifier;

    @property
    def ClientName(self):
        return self.__clientName;
