import Shared.constants.GameConstants as GameConstants;
import Shared.constants.NetConstants as NetConstants;

from Shared.dtos.PlayerGameDto import PlayerGameDto;
from Shared.dtos.GamePlayerListDto import GamePlayerListDto;

from Shared.Packet import Packet;
import Shared.utility.PacketUtility as PacketUtility;

from Shared.utility.Helpers import nameof;

from Werewolf.game.Player import Player;

import Client.utility.UIContext as UIContext;
from Client.MainWindow import MainWindow;

from datetime import datetime;

import socket;
import pickle;
import threading;
import time;

class ClientInstance():
    def __init__(self):
        super().__init__();
        self.__name = str();
        self.__connection = None;
        self.__lastUpdatedUtc = None;
        self.__player = None;
        self.__game = None;
        self.__mainWindow = MainWindow(self);

    def __getstate__(self):
        state = self.__dict__.copy();
        state["_" + type(self).__name__ + nameof(self.__connection)] = None;
        return state;

    # TODO: Do we need to do __setstate__ as well? Will I ever override Client/Player?

    @property
    def Name(self):
        return self.__name;

    @property
    def GameIdentifier(self):
        if not self.__game:
            return None;

        return self.__game.Identifier;

    #region Connection

    def Send(self, data):
        try:
            # We send some data
            self.__connection.sendall(pickle.dumps(data));

            # We get some reply
            serializedReply = self.__connection.recv(4 * NetConstants.KILOBYTE);

            # this is some serialized object
            reply = pickle.loads(serializedReply);

            return reply;

            print(reply);
        except socket.error as error:
            print("[ERROR] " + str(error));

        return;

    def Connect(self):
        try:
            self.__connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
            self.__connection.connect(NetConstants.ADDRESS);

            data = self.__connection.recv(4 * NetConstants.KILOBYTE).decode();

            self.__player = Player(self.__name);
            return data;
        except Exception as error:
            print("[ERROR] " + str(error));

        return;

    def Disconnect(self):
        if not self.__connection:
            return;

        try:
            self.LeaveGame();
            self.__connection.close();
        except Exception as error:
            print("[ERROR] " + str(error));

        return;

    #endregion

    #region Calls

    def GetGamesList(self):
        packet = PacketUtility.GetGamesPacket();

        reply = self.Send(packet);

        return reply;

    def LeaveGame(self):
        if not self.GameIdentifier:
            return;

        dto = PlayerGameDto(self.__player, self.GameIdentifier, self.__lastUpdatedUtc);
        packet = PacketUtility.GetLeaveGamePacket(dto)

        reply = self.Send(packet);

        if reply:
            self.__game = None;

        return reply;

    def JoinGame(self, gameIdentifier):
        dto = PlayerGameDto(self.__player, gameIdentifier, self.__lastUpdatedUtc)
        packet = PacketUtility.GetJoinGamePacket(dto);

        reply = self.Send(packet);

        self.__game = reply;

        return reply;

    def GetGameLobby(self):
        if not self.GameIdentifier:
            return None;

        dto = PlayerGameDto(self.__player, self.GameIdentifier, self.__lastUpdatedUtc);
        packet = PacketUtility.GetGameLobbyPacket(dto);

        reply = self.Send(packet);

        return reply;

    #endregion

    #region Client

    def SetName(self, name):
        if (not isinstance(name, str)):
            print("[ERROR] Name must be a string in order to create a player.")
            return;

        self.__name = name.strip();
        return;

    #endregion

if __name__ == "__main__":
    ClientInstance();
