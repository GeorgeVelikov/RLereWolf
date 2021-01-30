from http.client import HTTPConnection;

import constants.NetConstants as NetConstants;

class Client():
    def __init__(self):
        self.__connection = HTTPConnection(NetConstants.IP, NetConstants.PORT);
        self.__identifier = str(hash(self));
        self.__player = None;

        self.__connection.request("GET", NetConstants.ROUTE_INDEX);

    @property
    def Identifier(self):
        return self.__identifier;

    @property
    def Role(self):
        return self.__player;

    def SetPlayer(self, role):
        self.__player = role;
