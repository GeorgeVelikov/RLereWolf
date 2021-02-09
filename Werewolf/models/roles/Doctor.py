from enums.PlayerTypeEnum import PlayerTypeEnum;
from models.roles.RoleBase import RoleBase;

class Doctor(RoleBase):
    def __init__(self):
        super().__init__();

    @property
    def Role(self):
        return PlayerTypeEnum.Doctor;

    def Heal(self, player):
        if (not isinstance(player, RoleBase)):
            # TODO: not a very good "friendly" message
            raise TypeError("Player must be inherited from RoleBase in order to Heal them.");
            return;

        if (self == player):
            # TODO: not a very good "friendly" message, this probably needs to be handled elsewhere?
            raise ValueError("Player cannot heal themselves.");
            return;

        # TODO: call server to heal
        print(self.Name + " heals " + player.Name);
        return;