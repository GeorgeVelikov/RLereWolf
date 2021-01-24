from models.roles.RoleBase import RoleBase;

from enums.WerewolfPlayerTypeEnum import WerewolfPlayerTypeEnum;

class Peasant(RoleBase):
    def __init__(self, role):
        super().__init__(role)
