from enums.TimeOfDayEnum import TimeOfDayEnum;
from enums.TurnPhaseTypeEnum import TurnPhaseTypeEnum;

import game.Constants as Constant;

class Game():
    def __init__(self):
        self.Turn = 0;
        self.Players = list();
        self.TimeOfDay = TimeOfDayEnum._None;
        self.TurnPhase = TurnPhaseTypeEnum._None

    def Join(self, player):
        self.Players\
            .append(player)\
            .sort();
        return;

    def Leave(self, player):
        if (player not in self.Players):
            # TODO: raise some silent exception
            return;

        # no need to sort, already alphabetical
        self.Players\
            .remove(player);

    def Start(self):
        if (len(self.Players) < Constant.MINIMAL_PLAYER_COUNT):
            # TODO: add some warning
            return;

        return;

    def NextPhase(self):
        self.TurnPhase.Next();
        return;
