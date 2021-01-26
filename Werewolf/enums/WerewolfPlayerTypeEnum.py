from enum import Enum;

class WerewolfPlayerTypeEnum(Enum):
    # Can't escape keywords in Python :(
    _None = 0;
    Peasant = 1;
    Werewolf = 2;
    Seer = 3;
    Doctor = 4;

    def __str__(self):
        if self.value == self._None.value:
            return str();
        elif self.value == self.Peasant.value:
            return name(self.Peasant);
        elif self.value == self.Werewolf.value:
            return name(self.Werewolf);
        elif self.value == self.Seer.value:
            return name(self.Seer);
        elif self.value == self.Doctor.value:
            return name(self.Doctor);
        else:
            raise Exception("Unknown player type used.");

    def Values():
        return [\
            WerewolfPlayerTypeEnum.Peasant,\
            WerewolfPlayerTypeEnum.Werewolf,\
            WerewolfPlayerTypeEnum.Seer,\
            WerewolfPlayerTypeEnum.Doctor];