from enums.PacketTypeEnum import PacketTypeEnum;

class Packet():
    def __init__(self, type, data):
        self.__packetType = type;
        self.__data = data;

    @property
    def PacketType(self):
        return self.__packetType;

    @property
    def Data(self):
        return self.__data;

    @staticmethod
    def GetGamesPacket(data = None):
        return Packet(PacketTypeEnum.GetGamesList, data);

    @staticmethod
    def GetJoinGamePacket(data):
        return Packet(PacketTypeEnum.JoinGame, data);

    @staticmethod
    def GetLeaveGamePacket(data):
        return Packet(PacketTypeEnum.LeaveGame, data);

    @staticmethod
    def GetPlayersListPacket(data):
        return Packet(PacketTypeEnum.GetPlayers, data);