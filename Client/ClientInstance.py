import Shared.constants.GameConstants as GameConstants;
import Shared.constants.NetConstants as NetConstants;
from Shared.dtos.PlayerGameIdentifierDto import PlayerGameIdentifierDto;
from Shared.dtos.UpdatedEntityDto import UpdatedEntityDto;
from Shared.dtos.ConnectDto import ConnectDto;
from Shared.Packet import Packet;
from Shared.utility.Helpers import nameof;

from Werewolf.game.Player import Player;

import Client.utility.PacketUtility as PacketUtility;
from Client.context.ViewModelContext import ViewModelContext;

from datetime import datetime;
import socket;
import pickle;
import threading;
import time;
import uuid;


class ClientInstance():
    def __init__(self):
        self.__context = ViewModelContext(self);

        self.__name = str();
        self.__identifier = uuid.uuid4().hex;

        self.__connection = None;
        self.__lastUpdatedUtc = None;
        self.__player = None;
        self.__game = None;

        self.__context.UIContext.ShowMainMenu();
        self.__context.UIContext.StartMainWindow();

    @property
    def Context(self):
        return self.__context;

    @property
    def Name(self):
        return self.__name;

    @property
    def Identifier(self):
        return self.__identifier;

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

            dto = ConnectDto(self.Name, self.Identifier);
            packet = PacketUtility.GetConnectPacket(dto);

            reply = self.Send(packet);

            self.__player = reply;
            return reply;
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

        dto = PlayerGameIdentifierDto(self.__player, self.GameIdentifier);
        packet = PacketUtility.GetLeaveGamePacket(dto)

        reply = self.Send(packet);

        if reply:
            self.__game = None;

        return reply;

    def JoinGame(self, gameIdentifier):
        dto = PlayerGameIdentifierDto(self.__player, gameIdentifier)
        packet = PacketUtility.GetJoinGamePacket(dto);

        reply = self.Send(packet);

        self.__game = reply.Entity;
        self.__lastUpdatedUtc = reply.UpdatedUtc;

        return reply;

    def GetGameLobby(self):
        if not self.GameIdentifier:
            return None;

        dto = PlayerGameIdentifierDto(self.__player, self.GameIdentifier);
        wrapperDto = UpdatedEntityDto(dto, self.__lastUpdatedUtc);

        packet = PacketUtility.GetGameLobbyPacket(wrapperDto);

        reply = self.Send(packet);

        self.__game = reply.Entity.Game;
        self.__player = reply.Entity.Player;
        self.__lastUpdatedUtc = reply.UpdatedUtc;

        return self.__game;

    def VoteStart(self):
        if not self.GameIdentifier:
            return None;

        dto = PlayerGameIdentifierDto(self.__player, self.GameIdentifier);
        wrapperDto = UpdatedEntityDto(dto, self.__lastUpdatedUtc);

        packet = PacketUtility.GetVoteGameStartPacket(wrapperDto);

        reply = self.Send(packet);

        self.__game = reply.Entity.Game;
        self.__player = reply.Entity.Player;
        self.__lastUpdatedUtc = reply.UpdatedUtc;

        return reply;

    #endregion

    #region Client

    def SetName(self, name):
        if (not isinstance(name, str)):
            print("[ERROR] Name must be a string in order to create a player.")
            return;

        self.__name = name.strip();
        return;

    def QuitGame(self):
        self.__mainWindow.Close();
        return;

    #endregion

if __name__ == "__main__":
    ClientInstance();
