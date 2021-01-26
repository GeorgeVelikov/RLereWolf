from enums.WerewolfPlayerTypeEnum import WerewolfPlayerTypeEnum;
from models.roles.RoleBase import RoleBase;

class Seer(RoleBase):
    def __init__(self):
        super().__init__(WerewolfPlayerTypeEnum.Seer)
