from enums.TimeOfDayEnum import TimeOfDayEnum;
from enums.TurnPhaseTypeEnum import TurnPhaseTypeEnum;

from models.roles.Peasant import Peasant;
from models.roles.Seer import Seer;
from models.roles.Doctor import Doctor;
from models.roles.Werewolf import Werewolf;

import hashlib;

import constants.GameConstants as GameConstant;

class Game():
    def __init__(self, name):
        self.__identifier = str(hash(self));
        self.__name = name;
        self.__messages = list();
        self.__turn = int();
        self.__players = set();
        self.__timeOfDay = TimeOfDayEnum._None;
        self.__turnPhase = TurnPhaseTypeEnum._None;

    def __str__(self):
        return self.__name;

    def __repr__(self):
        return self.__name + " - " + self.Identifier;

    @property
    def Name(self):
        return self.__name + " - " + self.Identifier;

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

        player.JoinGame(self);
        return;

    def Leave(self, player):
        if (player not in self.__players):
            # TODO: raise some silent exception
            return;

        # no need to sort, already alphabetical
        self.__players\
            .remove(player);

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
