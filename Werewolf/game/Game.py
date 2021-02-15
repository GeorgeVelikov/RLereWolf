from Shared.enums.TimeOfDayEnum import TimeOfDayEnum;
from Shared.enums.TurnPhaseTypeEnum import TurnPhaseTypeEnum;

import Shared.constants.GameConstants as GameConstant;

from Werewolf.roles.Peasant import Peasant;
from Werewolf.roles.Seer import Seer;
from Werewolf.roles.Doctor import Doctor;
from Werewolf.roles.Werewolf import Werewolf;

import hashlib;
import uuid;

class Game():
    def __init__(self, name):
        self.__identifier = uuid.uuid4().hex;
        self.__name = name;
        self.__messages = set();
        self.__turn = int();
        self.__players = set();
        self.__timeOfDay = TimeOfDayEnum._None;
        self.__turnPhase = TurnPhaseTypeEnum._None;

    def __str__(self):
        return self.__name + " - " + self.Identifier;

    def __repr__(self):
        return self.__name + " - " + self.Identifier;

    @property
    def Name(self):
        return self.__name;

    @property
    def Players(self):
        return sorted(self.__players,\
            key = lambda p: p.Name, \
            reverse = False);

    @property
    def Identifier(self):
        return self.__identifier;

    def Join(self, player):
        self.__players.add(player);
        return;

    def Leave(self, player):
        if (player.Identifier not in [p.Identifier for p in self.__players]):
            # TODO: raise some silent exception
            return;

        # no need to sort, already alphabetical
        self.__players\
            .remove(next(p for p in self.__players if p.Identifier == player.Identifier));

    def Start(self):
        if (len(self.__players) < GameConstant.MINIMAL_PLAYER_COUNT):
            # TODO: add some warning
            return;

        for player in self.__players:
            player.SetRole(Peasant(), self);
            continue;

        self.__turn = 1;
        self.__timeOfDay == TimeOfDayEnum.Day;
        self.__turnPhase = TurnPhaseTypeEnum.Introduction;
        return;

    def NextPhase(self):
        self.__turnPhase.Next();
        return;
