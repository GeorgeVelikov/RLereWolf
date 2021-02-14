from enums.TimeOfDayEnum import TimeOfDayEnum;
from enums.TurnPhaseTypeEnum import TurnPhaseTypeEnum;

import hashlib;
import uuid;

import constants.GameConstants as GameConstant;

class Player():
    def __init__(self):
        self.__identifier = uuid.uuid4().hex;
        self.__name = str();
        self.__role = None;
        self.__gameIdentifier = None;

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

    def SetName(self, name):
        if (not isinstance(name, str)):
            print("[ERROR] Name must be a string in order to create a player.")
            return;

        self.__name = name.strip();
        return;

    def SetRole(self, role, gameIdentifier):
        # verify the game is changing our role and not something else
        if not gameIdentifier == self.__game.Identifier:
            return;

        self.__role = role;
        return;

    def JoinGame(self, gameIdentifier):
        if self.__gameIdentifier:
            # can't join a game when already in one
            return;

        self.__gameIdentifier = gameIdentifier;
        return;