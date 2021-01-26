from enums.TimeOfDayEnum import TimeOfDayEnum;
from enums.TurnPhaseTypeEnum import TurnPhaseTypeEnum;

import game.Constants as Constant;

class Game():
    def __init__(self):
        self.__turn = int();
        self.__players = list();
        self.__timeOfDay = TimeOfDayEnum._None;
        self.__turnPhase = TurnPhaseTypeEnum._None

    def Join(self, player):
        self.__players\
            .append(player)\
            .sort();
        return;

    def Leave(self, player):
        if (player not in self.__players):
            # TODO: raise some silent exception
            return;

        # no need to sort, already alphabetical
        self.__players\
            .remove(player);

    def Start(self):
        if (len(self.__players) < Constant.MINIMAL_PLAYER_COUNT):
            # TODO: add some warning
            return;

        return;

    def NextPhase(self):
        self.__turnPhase.Next();
        return;
