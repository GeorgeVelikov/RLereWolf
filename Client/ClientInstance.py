import Shared.constants.GameConstants as GameConstants;
import Shared.constants.NetConstants as NetConstants;

from Shared.dtos.ClientGameDto import ClientGameDto;
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

class ClientInstance(Player):
    def __init__(self):
        super().__init__();
        self.__name = str();
        self.__connection = None;
        self.__lastUpdateUtc = None;
        self.__gameIdentifier = None;
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
        return self.__gameIdentifier;

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

            return data;
        except Exception as error:
            print("[ERROR] " + str(error));

        return;

    def Disconnect(self):
        if not self.__connection:
            return;

        try:
            self.__connection.close();
            self.__gameIdentifier = None;
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
        if not self.__gameIdentifier:
            return;

        dto = ClientGameDto(self, self.__gameIdentifier);
        packet = PacketUtility.GetLeaveGamePacket(dto)

        reply = self.Send(packet);

        if reply:
            self.SetGame(None);

        return reply;

    def JoinGame(self, gameIdentifier):
        dto = ClientGameDto(self, gameIdentifier)
        packet = PacketUtility.GetJoinGamePacket(dto);

        reply = self.Send(packet);

        self.SetGame(reply);

        return reply;

    def GetPlayerList(self):
        if not self.__gameIdentifier:
            return None;

        dto = GamePlayerListDto(self.__gameIdentifier);
        packet = PacketUtility.GetPlayersListPacket(dto);

        reply = self.Send(packet);

        return reply.Players;

    def GetGameLobby(self):
        if not self.__gameIdentifier:
            return None;

        dto = None;
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

    def SetRole(self, role):
        # verify the game is changing our role and not something else
        if not self.__gameIdentifier:
            return;

        self.__role = role;
        return;

    def SetGame(self, gameIdentifier):
        if self.__gameIdentifier and gameIdentifier:
            # can't join a game when already in one
            return;

        self.__gameIdentifier = gameIdentifier;
        return;

    #endregion

if __name__ == "__main__":
    ClientInstance();
