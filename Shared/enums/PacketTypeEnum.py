from Shared.utility.Helpers import nameof;

from enum import Enum;

class PacketTypeEnum(Enum):
    # Can't escape keywords in Python :(
    _None = 0;
    GetGamesList = 1;
    JoinGame = 2;
    LeaveGame = 3;
    GetPlayers = 4;
    GameLobby = 5;

    def __str__(self):
        if self.value == self._None.value:
            return str();
        elif self.value == self.GetGamesList.value:
            return nameof(self.GetGamesList);
        elif self.value == self.JoinGame.value:
            return nameof(self.JoinGame);
        elif self.value == self.LeaveGame.value:
            return nameof(self.LeaveGame);
        elif self.value == self.GetPlayers.value:
            return nameof(self.GetPlayers);
        elif self.value == self.GameLobby.value:
            return nameof(self.GameLobby);
        else:
            raise Exception("Unknown packet type used.");

    def Values():
        return [\
            PacketTypeEnum.GetGamesList,\
            PacketTypeEnum.JoinGame,\
            PacketTypeEnum.LeaveGame,\
            PacketTypeEnum.GetPlayers,\
            PacketTypeEnum.GameLobby];
