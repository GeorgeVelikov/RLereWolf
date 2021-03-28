from Shared.utility.Helpers import nameof;
from Shared.exceptions.GameException import GameException;

from enum import Enum;

class MessageTypeEnum(Enum):
    # Can't escape keywords in Python :(
    _None = 0;
    AgreeWith = 100;
    DisagreeWith = 101;
    AccusePlayerOfRole = 102;
    SuggestPlayerOfRole = 103;
    DeclareSelfAsRole = 104;

    WerewolfAttack = 200;

    SeerDivine = 300;

    def __str__(self):
        if self.value == self._None.value:
            return str();

        elif self.value == self.AgreeWith.value:
            return nameof(self.AgreeWith);
        elif self.value == self.DisagreeWith.value:
            return nameof(self.DisagreeWith);
        elif self.value == self.AccusePlayerOfRole.value:
            return nameof(self.AccusePlayerOfRole);
        elif self.value == self.SuggestPlayerOfRole.value:
            return nameof(self.SuggestPlayerOfRole);
        elif self.value == self.DeclareSelfAsRole.value:
            return nameof(self.DeclareSelfAsRole);

        elif self.value == self.WerewolfAttack.value:
            return nameof(self.WerewolfAttack);

        elif self.value == self.SeerDivine.value:
            return nameof(self.SeerDivine);

        else:
            raise GameException("Unknown message type used.");

    @staticmethod
    def Values():
        return [\
            MessageTypeEnum.AgreeWith,\
            MessageTypeEnum.DisagreeWith,\
            MessageTypeEnum.AccusePlayerOfRole,\
            MessageTypeEnum.SuggestPlayerOfRole,\
            MessageTypeEnum.DeclareSelfAsRole,\

            MessageTypeEnum.WerewolfAttack,\

            MessageTypeEnum.SeerDivine];
