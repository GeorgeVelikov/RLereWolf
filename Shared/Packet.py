from Shared.enums.PacketTypeEnum import PacketTypeEnum;

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