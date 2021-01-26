from enums.TimeOfDayEnum import TimeOfDayEnum;
from enums.TurnPhaseTypeEnum import TurnPhaseTypeEnum;

import game.Constants as Constant;

class Game():
    def __init__(self):
        self.Players = list();
        self.Turn = 0;
        self.TimeOfDay = TimeOfDayEnum._None;
        self.TurnPhase = TurnPhaseTypeEnum._None

    def Start(self):
        if (len(self.Players) < Constant.MINIMAL_PLAYER_COUNT):
            # TODO: add some warning
            return;

        return;

    def NextPhase(self):
        self.TurnPhase.Next();
        return;
