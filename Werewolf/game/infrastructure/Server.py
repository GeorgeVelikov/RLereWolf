import constants.NetConstants as NetConstants;
import constants.GameConstants as GameConstants;

from enums.PacketTypeEnum import PacketTypeEnum;
from game.Game import Game;
from game.infrastructure.Client import Client;
from game.infrastructure.Packet import Packet;

from models.dtos.ClientJoinGameDto import ClientGameDto

from datetime import datetime;

import threading;
import socket;
import pickle;
import sys;

class Server():
    def __init__(self):
        self.__connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        self.__connections = set();
        self.__games = list();
        self.CreateGame("Game 1");
        self.CreateGame("Game 2");
        self.CreateGame("Game 3");
        self.CreateGame("Game 4");
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
        print(f"{self.UtcNowString} [STATUS] Active connections - {threading.activeCount() - 1}");

    #region Server

    def ClientHandle(self, connection, address):
        connection.send(b"Hello client");
        print(f"{self.UtcNowString} [STATUS] Connected to server - {address}.");
        self.ShowActiveConnections();

        while True:
            try:
                packetStream = connection.recv(4 * NetConstants.KILOBYTE);

                packet = pickle.loads(packetStream);

                if not packet:
                    break;

                print(f"{self.UtcNowString} [REQUEST] Packet type - {str(packet.PacketType)}.");

                if packet.PacketType == PacketTypeEnum.GetGamesList:
                    self.GetGamesList(connection, packet);

                elif packet.PacketType == PacketTypeEnum.JoinGame:
                    self.JoinGame(connection, packet);

                elif packet.PacketType == PacketTypeEnum.LeaveGame:
                    self.LeaveGame(connection, packet);

            except Exception as error:
                print(f"{self.UtcNowString} [ERROR] " + str(error));
                break;

        print(f"{self.UtcNowString} [STATUS] Lost connection to server - {address}.");
        connection.close();

        return;

    def Run(self):
        try:
            self.__connection.bind(NetConstants.ADDRESS);
            self.__connection.listen();
            print(f"{self.UtcNowString} [STATUS] Server successfully started at {NetConstants.IP}:{NetConstants.PORT}");
            self.ShowActiveConnections();
        except socket.error as error:
            print("{self.UtcNowString} [ERROR] " + str(error));

        while True:
            connection, address = self.__connection.accept();
            threading.Thread(target = self.ClientHandle, args = (connection, address)).start();
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

        game = next(g for g in self.__games if g.Identifier == dto.GameIdentifier);

        if not game:
            connection.sendall(pickle.dumps(None));

        game.Join(dto.Client);
        connection.sendall(pickle.dumps(dto.GameIdentifier));

        return;

    def LeaveGame(self, connection, packet):
        dto = packet.Data;

        game = next(g for g in self.__games if g.Identifier == dto.GameIdentifier);

        if not game:
            connection.sendall(pickle.dumps(True));

        game.Leave(dto.Client);
        connection.sendall(pickle.dumps(True));

        return;

    def CreateGame(self, name):
        game = Game(name);
        self.__games.append(game);

        return;

    #endregion

if __name__ == "__main__":
    Server().Run();
