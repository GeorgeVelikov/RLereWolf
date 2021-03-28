from Shared.utility.Helpers import nameof;
from Shared.exceptions.GameException import GameException;

from enum import Enum;

class FactionTypeEnum(Enum):
    # Can't escape keywords in Python :(
    _None = 0;
    Villagers = 100;
    Werewolves = 200;

    def __str__(self):
        if self.value == self._None.value:
            return str();

        elif self.value == self.Villagers.value:
            return nameof(self.Villagers);

        elif self.value == self.Werewolves.value:
            return nameof(self.Werewolves);
        else:
            raise GameException("Unknown faction type used.");

    @staticmethod
    def Values():
        return [\
            FactionTypeEnum.Villagers,\
            FactionTypeEnum.Werewolves];
