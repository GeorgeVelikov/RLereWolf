from enum import Enum;
from utility.Helpers import nameof;

class TimeOfDayEnum(Enum):
    # Can't escape keywords in Python :(
    _None = 0;
    Day = 1;
    Night = 2;

    def __str__(self):
        if self.value == self._None.value:
            return str();
        elif self.value == self.Day.value:
            return nameof(self.Day);
        elif self.value == self.Night.value:
            return nameof(self.Night);
        else:
            raise Exception("Unknown turn cycle type used.");

    def Values():
        return [\
            TimeOfDayEnum.Day,\
            TimeOfDayEnum.Night];
