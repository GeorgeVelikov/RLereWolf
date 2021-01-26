from enums.PlayerTypeEnum import PlayerTypeEnum;
from models.roles.RoleBase import RoleBase;

class Peasant(RoleBase):
    def __init__(self):
        super().__init__(PlayerTypeEnum.Peasant);
