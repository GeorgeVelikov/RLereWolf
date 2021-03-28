from Shared.utility.Helpers import nameof;
from Shared.exceptions.GameException import GameException;

from enum import Enum;

class VoteResultTypeEnum(Enum):
   # Can't escape keywords in Python :(
    _None = 0;

    WaitAction = 100;
    SuccessfulAction = 101;

    CannotActDuringTimeOfDay = 200;
    InvalidAction = 201;
    DeadPlayerTargeted = 202;
    WerewolfCannibalism = 203;

    def __str__(self):
        if self.value == self._None.value:
            return str();

        elif self.value == self.WaitAction.value:
            return nameof(self.WaitAction);
        elif self.value == self.SuccessfulAction.value:
            return nameof(self.SuccessfulAction);

        elif self.value == self.CannotActDuringTimeOfDay.value:
            return nameof(self.CannotActDuringTimeOfDay);
        elif self.value == self.InvalidAction.value:
            return nameof(self.InvalidAction);
        elif self.value == self.DeadPlayerTargeted.value:
            return nameof(self.DeadPlayerTargeted);
        elif self.value == self.WerewolfCannibalism.value:
            return nameof(self.WerewolfCannibalism);

        else:
            raise GameException("Unknown vote result type used.");

    @staticmethod
    def Values():
        return [\
            VoteResultTypeEnum.WaitAction,\
            VoteResultTypeEnum.SuccessfulAction,\

            VoteResultTypeEnum.CannotActDuringTimeOfDay,\
            VoteResultTypeEnum.InvalidAction,\
            VoteResultTypeEnum.DeadPlayerTargeted,\
            VoteResultTypeEnum.WerewolfCannibalism];
