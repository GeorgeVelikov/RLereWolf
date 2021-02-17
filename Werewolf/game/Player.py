from Shared.enums.TimeOfDayEnum import TimeOfDayEnum;
from Shared.enums.TurnPhaseTypeEnum import TurnPhaseTypeEnum;

import hashlib;
import uuid;

class Player():
    def __init__(self, name = "", role = None):
        self.__identifier = uuid.uuid4().hex;
        self.__name = name;
        self.__role = role;

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

    @property
    def IsAlive(self):
        if not self.__role:
            return None;

        return self.__role.IsAlive;

