from Shared.enums.PacketTypeEnum import PacketTypeEnum;
from Shared.Packet import Packet;

def GetConnectPacket(data):
    return Packet(PacketTypeEnum.Connect, data);

# game list
def GetGamesPacket(data = None):
    return Packet(PacketTypeEnum.GetGamesList, data);

def GetJoinGamePacket(data):
    return Packet(PacketTypeEnum.JoinGame, data);

def GetLeaveGamePacket(data):
    return Packet(PacketTypeEnum.LeaveGame, data);

# lobby calls
def GetPlayersListPacket(data):
    return Packet(PacketTypeEnum.GetPlayers, data);

def GetGameLobbyPacket(data):
    return Packet(PacketTypeEnum.GameLobby, data);

def GetVoteGameStartPacket(data):
    return Packet(PacketTypeEnum.VoteStart, data);

def GetVotePlayerPacket(data):
    return Packet(PacketTypeEnum.VotePlayer, data);