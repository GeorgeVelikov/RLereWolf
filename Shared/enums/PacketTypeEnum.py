from Shared.utility.Helpers import nameof;
from Shared.exceptions.GameException import GameException;

from enum import Enum;

class PacketTypeEnum(Enum):
    # Can't escape keywords in Python :(
    _None = 0;
    GetGamesList = 1;
    JoinGame = 2;
    LeaveGame = 3;
    GameLobby = 4;

    def __str__(self):
        if self.value == self._None.value:
            return str();
        elif self.value == self.GetGamesList.value:
            return nameof(self.GetGamesList);
        elif self.value == self.JoinGame.value:
            return nameof(self.JoinGame);
        elif self.value == self.LeaveGame.value:
            return nameof(self.LeaveGame);
        elif self.value == self.GameLobby.value:
            return nameof(self.GameLobby);
        else:
            raise GameException("Unknown packet type used.");

    @staticmethod
    def Values():
        return [\
            PacketTypeEnum.GetGamesList,\
            PacketTypeEnum.JoinGame,\
            PacketTypeEnum.LeaveGame,\
            PacketTypeEnum.GameLobby];
