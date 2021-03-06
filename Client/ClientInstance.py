from Client.context.ViewModelContext import ViewModelContext;

import uuid;

class ClientInstance():
    def __init__(self):
        self.__context = ViewModelContext(self);

        self.__name = str();
        self.__identifier = uuid.uuid4().hex;

        self.__player = None;
        self.__game = None;

        self.__context.UIContext.StartMainWindow();

    @property
    def Context(self):
        return self.__context;

    @property
    def Name(self):
        return self.__name;

    @property
    def Identifier(self):
        return self.__identifier;

    @property
    def Player(self):
        return self.__player;

    @property
    def Game(self):
        return self.__game;

    @property
    def GameIdentifier(self):
        if not self.__game:
            return None;

        return self.__game.Identifier;

    #region Client

    def SetName(self, name):
        if (not isinstance(name, str)):
            print("[ERROR] Name must be a string in order to create a player.")
            return;

        self.__name = name.strip();
        return;

    def SetPlayer(self, player):
        self.__player = player;
        return;

    def SetGame(self, game):
        self.__game = game;
        return;

    #endregion

if __name__ == "__main__":
    ClientInstance();
