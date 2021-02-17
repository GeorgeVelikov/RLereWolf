from Shared.enums.PlayerTypeEnum import PlayerTypeEnum;
from Werewolf.roles.RoleBase import RoleBase;

class Villager(RoleBase):
    def __init__(self, name):
        super().__init__(name);

    @property
    def Role(self):
        return PlayerTypeEnum.Villager;