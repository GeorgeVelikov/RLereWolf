from Werewolf.game.roles.Role import Role;
from Shared.enums.PlayerTypeEnum import PlayerTypeEnum;

class Guard(Role):
    def __init__(self):
        self.__canGuardTimes = 1;

    @property
    def Type(self):
        return PlayerTypeEnum.Guard;

    @property
    def HasDayAction(self):
        return True;

    @property
    def HasNightAction(self):
        return self.CanGuard;

    @property
    def CanGuard(self):
        return self.__canGuardTimes > 0;