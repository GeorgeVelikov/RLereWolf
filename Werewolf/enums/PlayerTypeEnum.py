from Shared.utility.Helpers import nameof;

from enum import Enum;


class PlayerTypeEnum(Enum):
    # Can't escape keywords in Python :(
    _None = 0;
    Peasant = 1;
    Werewolf = 2;
    Seer = 3;
    Guard = 4;

    def __str__(self):
        if self.value == self._None.value:
            return str();
        elif self.value == self.Peasant.value:
            return nameof(self.Peasant);
        elif self.value == self.Werewolf.value:
            return nameof(self.Werewolf);
        elif self.value == self.Seer.value:
            return nameof(self.Seer);
        elif self.value == self.Guard.value:
            return nameof(self.Guard);
        else:
            raise Exception("Unknown player type used.");

    def Values():
        return [\
            PlayerTypeEnum.Peasant,\
            PlayerTypeEnum.Werewolf,\
            PlayerTypeEnum.Seer,\
            PlayerTypeEnum.Guard];
