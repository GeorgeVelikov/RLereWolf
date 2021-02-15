import Shared.constants.NetConstants as NetConstants;
import Shared.constants.GameConstants as GameConstants;

from Shared.dtos.ClientGameDto import ClientGameDto;
from Shared.dtos.GamePlayerListDto import GamePlayerListDto;

from Shared.Packet import Packet;
from Shared.enums.PacketTypeEnum import PacketTypeEnum;

# Temporary reference!
from Client.ClientInstance import ClientInstance;

from Werewolf.game.Game import Game;

import constants.LogConstants as LogConstants;

from datetime import datetime;

import threading;
import socket;
import pickle;
import sys;
import os;

class Server():
    def __init__(self):
        self.__connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        self.__connections = set();
        self.__games = list();
        self.CreateGame("Game 1");
        self.CreateGame("Game 2");
        self.CreateGame("Game 3");
        self.CreateGame("Game 4");

        self.Log(LogConstants.INFORMATION, "Server start up");

        return;

    @property
    def Games(self):
        return self.__games;

    @property
    def UtcNow(self):
        return datetime.utcnow();

    @property
    def UtcNowString(self):
        return self.UtcNow.strftime(NetConstants.DATETIME_FORMAT);

    def ShowActiveConnections(self):
        self.Log(LogConstants.INFORMATION, f"Active connections - {threading.activeCount() - 1}");

    #region Server

    def ClientHandle(self, connection, address):
        connection.send(b"Hello client");
        self.Log(LogConstants.INFORMATION, f"Connected to server - {address}");
        self.ShowActiveConnections();

        while True:
            try:
                packetStream = connection.recv(4 * NetConstants.KILOBYTE);

                packet = pickle.loads(packetStream);

                if not packet:
                    break;

                self.Log(LogConstants.REQUEST, f"Packet type - {str(packet.PacketType)}");

                if packet.PacketType == PacketTypeEnum.GetGamesList:
                    self.GetGamesList(connection, packet);

                elif packet.PacketType == PacketTypeEnum.JoinGame:
                    self.JoinGame(connection, packet);

                elif packet.PacketType == PacketTypeEnum.LeaveGame:
                    self.LeaveGame(connection, packet);

                elif packet.PacketType == PacketTypeEnum.GetPlayers:
                    self.GetPlayerList(connection, packet);

            except Exception as error:
                self.Log(LogConstants.ERROR, str(error));
                break;

        self.Log(LogConstants.INFORMATION, f"Lost connection to server - {address}");
        connection.close();

        return;

    def Run(self):
        try:
            self.__connection.bind(NetConstants.ADDRESS);
            self.__connection.listen();
            self.Log(LogConstants.INFORMATION, f"Server successfully started at {NetConstants.IP}:{NetConstants.PORT}");
            self.ShowActiveConnections();
        except socket.error as error:
            self.Log(LogConstants.ERROR, str(error));

        while True:
            connection, address = self.__connection.accept();
            threading.Thread(target = self.ClientHandle, args = (connection, address)).start();
        return;

    def Log(self, status, message):
        fileName = self.UtcNow.strftime("%d-%m-%Y");

        if not os.path.exists(LogConstants.DIRECTORY_LOGS):
            os.makedirs(LogConstants.DIRECTORY_LOGS);

        logMessage = f"{self.UtcNowString} {status} {message}.";
        print(logMessage);

        log = open(f"{LogConstants.DIRECTORY_LOGS}{os.path.sep}{fileName}.txt", "a");
        log.write("\n" + logMessage);
        log.close();

        return;

    #endregion

    #region Game calls

    def Connect(self, connection, packet):
        client = packet.Data;

        connection.sendall(pickle.dumps(None));

        return;

    def GetGamesList(self, connection, packet):
        games = dict((game.Identifier, game.Name) for game in self.__games);

        connection.sendall(pickle.dumps(games));

        return;

    def JoinGame(self, connection, packet):
        dto = packet.Data;

        game = self.GetGameWithIdentifier(dto.GameIdentifier);

        if not game:
            connection.sendall(pickle.dumps(None));

        game.Join(dto.Client);
        connection.sendall(pickle.dumps(dto.GameIdentifier));

        return;

    def LeaveGame(self, connection, packet):
        dto = packet.Data;

        game = self.GetGameWithIdentifier(dto.GameIdentifier);

        if not game:
            connection.sendall(pickle.dumps(True));

        game.Leave(dto.Client);
        connection.sendall(pickle.dumps(True));

        return;

    def CreateGame(self, connection, packet):
        # reuse the server-side call but encapsulate it with the connection and packet check
        raise NotImplementedError("Not implemented yet");

    def GetPlayerList(self, connection, packet):
        dto = packet.Data;

        game = self.GetGameWithIdentifier(dto.GameIdentifier);

        if not game:
            connection.sendall(pickle.dumps(None));

        playersByIdentifier = dict((player.Identifier, player.Name) for player in game.Players);

        replyDto = GamePlayerListDto(dto.GameIdentifier, playersByIdentifier);

        connection.sendall(pickle.dumps(replyDto));

    #endregion

    #region Server only calls
    # Client cannot directly use those!

    def CreateGame(self, name):
        game = Game(name);
        self.__games.append(game);

        return;

    def GetGameWithIdentifier(self, gameIdentifier):
        return next(g for g in self.__games if g.Identifier == gameIdentifier);

    #endregion

if __name__ == "__main__":
    Server().Run();