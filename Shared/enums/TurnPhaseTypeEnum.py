from Shared.utility.Helpers import nameof;

from enum import Enum;

class TurnPhaseTypeEnum(Enum):
    # Can't escape keywords in Python :(
    _None = 0;
    Introduction = 1;
    Discussion = 2;
    Event = 3;
    Accusation = 4;
    Voting = 5;

    def __str__(self):
        if self.value == self._None.value:
            return str()
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

    def Next(self):
        if self.value == self.Introduction or self.value == self.Discussion:
            self.value = self.Event;
        elif self.value == self.Event:
            self.value = self.Accusation;
        elif self.value == self.Accusation:
            self.value = self.Voting;
        elif self.value == self.Voting:
            self.value = self.Discussion;
        else:
            raise Exception("Turn phase " + str(self.value) + " has no next phase.");

    @staticmethod
    def Values():
        return [\
            TurnPhaseTypeEnum.Introduction,\
            TurnPhaseTypeEnum.Discussion,\
            TurnPhaseTypeEnum.Event,\
            TurnPhaseTypeEnum.Accusation,\
            TurnPhaseTypeEnum.Voting];
