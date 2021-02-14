from enum import Enum;
from utility.Helpers import nameof;

class PacketTypeEnum(Enum):
    # Can't escape keywords in Python :(
    _None = 0;
    GetGamesList = 1;
    JoinGame = 2;
    LeaveGame = 3;

    def __str__(self):
        if self.value == self._None.value:
            return str();
        elif self.value == self.GetGamesList.value:
            return nameof(self.GetGamesList);
        elif self.value == self.JoinGame.value:
            return nameof(self.JoinGame);
        elif self.value == self.LeaveGame.value:
            return nameof(self.LeaveGame);
        else:
            raise Exception("Unknown packet type used.");

    def Values():
        return [\
            PacketTypeEnum.GetGamesList,\
            PacketTypeEnum.JoinGame,\
            PacketTypeEnum.LeaveGame];
