from enums.WereworlfTurnCycleTypeEnum import WereworlfTurnCycleTypeEnum;

class Game():
    def __init__(self):
        self.Players = list();
        self.Turn = 0;
        self.TurnCycle = WerewolfTurnCycleTypeEnum._None;
