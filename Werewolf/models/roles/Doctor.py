from models.roles.RoleBase import RoleBase;

class Doctor(RoleBase):
    def __init__(self, role):
        super().__init__(role)