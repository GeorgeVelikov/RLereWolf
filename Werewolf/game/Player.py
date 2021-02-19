import uuid;

class Player():
    def __init__(self, name, identifier = None):
        self.__identifier = (uuid.uuid4().hex if not identifier else identifier);
        self.__name = name;
        self.__isReady = False;
        self.__role = None;

    def __str__(self):
        return self.__name;

    def __repr__(self):
        return self.__name + "(" + self.Identifier + ")";

    @property
    def Identifier(self):
        return self.__identifier;

    @property
    def Name(self):
        return self.__name;

    @property
    def IsReady(self):
        return self.__isReady;

    @property
    def Role(self):
        return self.__role;

    @property
    def IsAlive(self):
        if not self.__role:
            return None;

        return self.__role.IsAlive;
