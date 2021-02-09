from enums.TimeOfDayEnum import TimeOfDayEnum;
from enums.TurnPhaseTypeEnum import TurnPhaseTypeEnum;

import hashlib;

import constants.GameConstants as GameConstant;

class Player():
    def __init__(self, name):
        self.__identifier = str(hash(self));
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

    def JoinGame(self, game):
        self.__game = game;