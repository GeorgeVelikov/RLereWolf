from Shared.enums.PlayerTypeEnum import PlayerTypeEnum;
from Werewolf.roles.RoleBase import RoleBase;

class Guard(RoleBase):
    def __init__(self, name):
        super().__init__(name);
        self.__canGuard = True;

    @property
    def Role(self):
        return PlayerTypeEnum.Guard;

    @property
    def CanGuard(self):
        return self.__canGuard;

    def Guard(self, player):
        if (not self.__canGuard):
            return;

        if (not isinstance(player, RoleBase)):
            # TODO: not a very good "friendly" message
            raise TypeError("Player must be inherited from RoleBase in order to Guard them.");
            return;

        if (self == player):
            # TODO: not a very good "friendly" message, this probably needs to be handled elsewhere?
            raise ValueError("Player cannot guard themselves.");
            return;

        # TODO: call server to guard
        print(self.Name + " guards " + player.Name);
        return;