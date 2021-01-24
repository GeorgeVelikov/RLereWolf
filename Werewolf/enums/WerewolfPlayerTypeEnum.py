from enum import Enum

class WerewolfPlayerTypeEnum(Enum):
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
            return name(Peasant);
        elif self.value == self.Werewolf.value:
            return name(Werewolf);
        elif self.value == self.Seer.value:
            return name(Seer);
        elif self.value == self.Guard.value:
            return name(Guard);
        else:
            raise Exception("Unknown player type used.");

    def Values():
        return [\
            LogicalConnectiveEnum.Peasant,\
            LogicalConnectiveEnum.Werewolf,\
            LogicalConnectiveEnum.Seer,\
            LogicalConnectiveEnum.Guard];