from Shared.utility.Helpers import nameof;
from Shared.exceptions.GameException import GameException;

from enum import Enum;

class PacketTypeEnum(Enum):
    # Can't escape keywords in Python :(
    _None = 0;

    # Server calls
    # this needs a "Disconnect" call as well if we have time
    # Disconnects are still handled, but it's not very explicit, rather it just
    # cuts off the connection and we rely on the server detecting that there
    # has been a cut off from some specific client. Arguably a bit more reliable
    # than awaiting a disconnect call which may or may not fail. Still unsure.
    Connect = 100;

    # Server game list calls
    GetGamesList = 200;
    CreateGame = 201;
    JoinGame = 202;
    LeaveGame = 203;

    # Game Instance call, this just asks for the game state
    GameLobby = 300;
    AddAgent = 301;
    RemoveAgent = 302;
    VoteStart = 303;

    # Game Instance Actions
    Talk = 400;
    VotePlayer = 401;

    Whisper = 410;
    AttackPlayer = 411;

    DivinePlayer = 420;

    GuardPlayer = 430;

    def __str__(self):
        if self.value == self._None.value:
            return str();

        elif self.value == self.Connect.value:
            return nameof(self.Connect);

        elif self.value == self.GetGamesList.value:
            return nameof(self.GetGamesList);
        elif self.value == self.CreateGame.value:
            return nameof(self.CreateGame);
        elif self.value == self.JoinGame.value:
            return nameof(self.JoinGame);
        elif self.value == self.LeaveGame.value:
            return nameof(self.LeaveGame);

        elif self.value == self.GameLobby.value:
            return nameof(self.GameLobby);
        elif self.value == self.AddAgent.value:
            return nameof(self.AddAgent);
        elif self.value == self.RemoveAgent.value:
            return nameof(self.RemoveAgent);

        elif self.value == self.VoteStart.value:
            return nameof(self.VoteStart);
        elif self.value == self.VotePlayer.value:
            return nameof(self.VotePlayer);
        elif self.value == self.Talk.value:
            return nameof(self.Talk);
        elif self.value == self.Whisper.value:
            return nameof(self.Whisper);
        elif self.value == self.AttackPlayer.value:
            return nameof(self.AttackPlayer);
        elif self.value == self.DivinePlayer.value:
            return nameof(self.DivinePlayer);
        elif self.value == self.GuardPlayer.value:
            return nameof(self.GuardPlayer);
        else:
            raise GameException("Unknown packet type used.");

    @staticmethod
    def Values():
        return [\
            PacketTypeEnum.Connect,\

            PacketTypeEnum.GetGamesList,\
            PacketTypeEnum.CreateGame,\
            PacketTypeEnum.JoinGame,\
            PacketTypeEnum.LeaveGame,\

            PacketTypeEnum.GameLobby,\
            PacketTypeEnum.AddAgent,\
            PacketTypeEnum.RemoveAgent,\
            PacketTypeEnum.VoteStart,\

            PacketTypeEnum.VotePlayer,\
            PacketTypeEnum.Talk,\
            PacketTypeEnum.Whisper,\
            PacketTypeEnum.AttackPlayer,\
            PacketTypeEnum.DivinePlayer,\
            PacketTypeEnum.GuardPlayer];
