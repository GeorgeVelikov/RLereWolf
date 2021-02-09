from enums.PlayerTypeEnum import PlayerTypeEnum;
from models.roles.RoleBase import RoleBase;

class Seer(RoleBase):
    def __init__(self):
        super().__init__();

    @property
    def Role(self):
        return PlayerTypeEnum.Seer;