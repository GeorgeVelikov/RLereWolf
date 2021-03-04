from Shared.enums.PacketTypeEnum import PacketTypeEnum;
from Shared.Packet import Packet;

def GetConnectPacket(data):
    return Packet(PacketTypeEnum.Connect, data);

#region Game list calls

def GetGamesPacket(data = None):
    return Packet(PacketTypeEnum.GetGamesList, data);

def GetJoinGamePacket(data):
    return Packet(PacketTypeEnum.JoinGame, data);

def GetLeaveGamePacket(data):
    return Packet(PacketTypeEnum.LeaveGame, data);

#endregion

#region Game lobby calls

def GetGameLobbyPacket(data):
    return Packet(PacketTypeEnum.GameLobby, data);

def GetAddAgentToGamePacket(data):
    return Packet(PacketTypeEnum.AddAgent, data);

def GetRemoveAgentFromGamePacket(data):
    return Packet(PacketTypeEnum.RemoveAgent, data);

def GetVoteGameStartPacket(data):
    return Packet(PacketTypeEnum.VoteStart, data);

#endregion

#region Game lobby action calls

def GetVotePlayerPacket(data):
    return Packet(PacketTypeEnum.VotePlayer, data);

def GetAttackPlayerPacket(data):
    return Packet(PacketTypeEnum.AttackPlayer, data);

def GetDivinePlayerPacket(data):
    return Packet(PacketTypeEnum.DivinePlayer, data);

def GetGuardPlayerPacket(data):
    return Packet(PacketTypeEnum.GuardPlayer, data);

#endregion