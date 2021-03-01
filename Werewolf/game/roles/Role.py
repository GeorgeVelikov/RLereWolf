from Shared.enums.PlayerTypeEnum import PlayerTypeEnum;

class Role():
    def __init__(self):
        pass;

    @property
    def Type(self):
        return PlayerTypeEnum._None;

    @property
    def HasDayAction(self):
        return False;

    @property
    def HasNightAction(self):
        return False;
