from abc import abstractmethod;

from enums.PlayerTypeEnum import PlayerTypeEnum;

class RoleBase():
    def __init__(self, role):
        self.__role = role;

    @property
    def Role(self):
        return self.__role;
