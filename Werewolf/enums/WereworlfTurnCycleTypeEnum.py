from enum import Enum;

class WereworlfTurnCycleTypeEnum(Enum):
    # Can't escape keywords in Python :(
    _None = 0;
    Day = 1;
    Night = 2;

    def __str__(self):
        if self.value == self._None.value:
            return str();
        elif self.value == self.Day.value:
            return name(self.Day);
        elif self.value == self.Night.value:
            return name(self.Night);
        else:
            raise Exception("Unknown turn cycle type used.");

    def Values():
        return [\
            WereworlfTurnCycleTypeEnum.Day,\
            WereworlfTurnCycleTypeEnum.Night];


