from Werewolf.game.roles.Role import Role;
from Shared.enums.PlayerTypeEnum import PlayerTypeEnum;

class Werewolf(Role):
    def __init__(self):
        pass;

    @property
    def Type(self):
        return PlayerTypeEnum.Werewolf;

    @property
    def CanTargetDeadPlayers(self):
        return False;

    @property
    def HasDayAction(self):
        return True;

    @property
    def HasNightAction(self):
        return True;
