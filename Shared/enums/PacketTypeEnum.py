from Shared.utility.Helpers import nameof;
from Shared.exceptions.GameException import GameException;

from enum import Enum;

class PacketTypeEnum(Enum):
    # Can't escape keywords in Python :(
    _None = 0;
    Connect = 1;
    GetGamesList = 2;
    JoinGame = 3;
    LeaveGame = 4;
    GameLobby = 5;
    VoteStart = 6;

    def __str__(self):
        if self.value == self._None.value:
            return str();
        elif self.value == self.Connect.value:
            return nameof(self.Connect);
        elif self.value == self.GetGamesList.value:
            return nameof(self.GetGamesList);
        elif self.value == self.JoinGame.value:
            return nameof(self.JoinGame);
        elif self.value == self.LeaveGame.value:
            return nameof(self.LeaveGame);
        elif self.value == self.GameLobby.value:
            return nameof(self.GameLobby);
        elif self.value == self.VoteStart.value:
            return nameof(self.VoteStart);
        else:
            raise GameException("Unknown packet type used.");

    @staticmethod
    def Values():
        return [\
            PacketTypeEnum.Connect,\
            PacketTypeEnum.GetGamesList,\
            PacketTypeEnum.JoinGame,\
            PacketTypeEnum.LeaveGame,\
            PacketTypeEnum.GameLobby,\
            PacketTypeEnum.VoteStart];
