from Shared.utility.Helpers import nameof;
from Shared.exceptions.GameException import GameException;

from enum import Enum;

class PlayerTypeEnum(Enum):
    # Can't escape keywords in Python :(
    _None = 0;
    Villager = 1;
    Werewolf = 2;
    Seer = 3;
    Guard = 4;

    def __str__(self):
        if self.value == self._None.value:
            return str();
        elif self.value == self.Villager.value:
            return nameof(self.Villager);
        elif self.value == self.Werewolf.value:
            return nameof(self.Werewolf);
        elif self.value == self.Seer.value:
            return nameof(self.Seer);
        elif self.value == self.Guard.value:
            return nameof(self.Guard);
        else:
            raise GameException("Unknown player type used.");

    @staticmethod
    def Values():
        return [\
            PlayerTypeEnum.Villager,\
            PlayerTypeEnum.Werewolf,\
            PlayerTypeEnum.Seer,\
            PlayerTypeEnum.Doctor];

    @staticmethod
    def RolesWithPrivateMessages():
        return [\
            PlayerTypeEnum.Seer];
