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
            return name(Day);
        elif self.value == self.Night.value:
            return name(Night);
        else:
            raise Exception("Unknown turn cycle type used.");

    def Values():
        return [\
            LogicalConnectiveEnum.Day,\
            LogicalConnectiveEnum.Night];


