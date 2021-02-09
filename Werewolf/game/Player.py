from enums.TimeOfDayEnum import TimeOfDayEnum;
from enums.TurnPhaseTypeEnum import TurnPhaseTypeEnum;

import hashlib;

import constants.GameConstants as GameConstant;

class Player():
    def __init__(self, name):
        if (not isinstance(name, str)):
            raise TypeError("Name must be a string in order to create a player.");
            return;

        self.__identifier = str(hash(self));
        self.__name = name.strip();
        self.__name = name;
        self.__role = None;
        self.__game = None;

    def __str__(self):
        return self.__name;

    def __repr__(self):
        return self.__name + "(" + self.Identifier + ")";

    @property
    def Name(self):
        return self.__name;

    @property
    def Identifier(self):
        return self.__identifier;

    def SetRole(self, role, gameIdentifier):
        # verify the game is changing our role and not something else
        if not gameIdentifier == self.__game.Identifier:
            return;

        self.__role = role;
        return;

    def JoinGame(self, game):
        if self.__game:
            # can't join a game when already in one
            return;

        self.__game = game;
        return;