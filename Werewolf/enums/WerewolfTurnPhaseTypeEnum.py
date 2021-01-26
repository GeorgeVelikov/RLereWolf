from enum import Enum;
from utility.Helpers import nameof;

class WerewolfTurnPhaseTypeEnum(Enum):
    # Can't escape keywords in Python :(
    _None = 0;
    Introduction = 1;
    Discussion = 2;
    Event = 3;
    Accusation = 4;
    Voting = 5;

    def __str__(self):
        if self.value == self._None.value:
            return str();
        elif self.value == self.Introduction.value:
            return nameof(self.Introduction);
        elif self.value == self.Discussion.value:
            return nameof(self.Discussion);
        elif self.value == self.Event.value:
            return nameof(self.Event);
        elif self.value == self.Accusation.value:
            return nameof(self.Accusation);
        elif self.value == self.Voting.value:
            return nameof(self.Voting);
        else:
            raise Exception("Unknown turn phase type used.");

    def Values():
        return [\
            WerewolfTurnPhaseTypeEnum.Introduction,\
            WerewolfTurnPhaseTypeEnum.Discussion,\
            WerewolfTurnPhaseTypeEnum.Event,\
            WerewolfTurnPhaseTypeEnum.Accusation,\
            WerewolfTurnPhaseTypeEnum.Voting];



