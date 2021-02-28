from Shared.utility.Helpers import nameof;
from Shared.exceptions.GameException import GameException;

from enum import Enum;

class PacketTypeEnum(Enum):
    # Can't escape keywords in Python :(
    _None = 0;

    # Server call, this needs a "Disconnect" call as well
    Connect = 1;

    # Server game list calls
    GetGamesList = 2;
    JoinGame = 3;
    LeaveGame = 4;

    # Game instance call, this just asks for the game state
    GameLobby = 5;

    # Game Instance Actions
    VoteStart = 6;
    Talk = 7;
    VotePlayer = 8;
    Whisper = 9;
    AttackPlayer = 10;
    DivinePlayer = 11;
    GuardPlayer = 12;


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
        elif self.value == self.VotePlayer.value:
            return nameof(self.VotePlayer);
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

            PacketTypeEnum.VoteStart,\
            PacketTypeEnum.VotePlayer];
