from Server.HandlerContext import HandlerContext;

import Shared.constants.NetConstants as NetConstants;
import Shared.utility.LogUtility as LogUtility;
from Shared.enums.PacketTypeEnum import PacketTypeEnum;

from Werewolf.game.Game import Game;
from Werewolf.game.Player import Player;

from datetime import datetime;
import traceback;
import threading;
import socket;
import pickle;

class ServerInstance():
    def __init__(self):
        self.__connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        self.__handlerContext = HandlerContext(self);
        self.__validPacketTypes = PacketTypeEnum.Values();
        self.__connections = dict();
        self.__games = dict();

        self.__handlerContext.CreateGame("Game Alpha");
        self.__handlerContext.CreateGame("Game Beta");
        self.__handlerContext.CreateGame("Game Gamma");
        self.__handlerContext.CreateGame("Game Delta");

        LogUtility.Information("Server start up");

        return;

    @property
    def Games(self):
        return self.__games;

    @property
    def Connections(self):
        return self.__connections;

    @property
    def HandlerContext(self):
        return self.__handlerContext;

    @property
    def ValidPacketTypes(self):
        return self.__validPacketTypes;

    @property
    def UtcNow(self):
        return datetime.utcnow();

    def ShowActiveConnections(self):
        LogUtility.Information(f"Active connections - {len(self.__connections)}");

    def Run(self):
        try:
            self.__connection.bind(NetConstants.ADDRESS);
            self.__connection.listen();

            LogUtility.Information(f"Server successfully started at {NetConstants.IP}:{NetConstants.PORT}");

            self.ShowActiveConnections();
        except socket.error as error:
            trace = traceback.format_exc();
            LogUtility.Error(str(error) + "\n\n" + trace);

        while True:
            connection, address = self.__connection.accept();
            threading.Thread(target = self.ClientHandle, args = (connection, address)).start();
        return;

    def ClientHandle(self, connection, address):
        while True:
            try:
                packetStream = connection.recv(4 * NetConstants.KILOBYTE);

                if not packetStream:
                    # connection is interrupted/closed by client because we get null back
                    break;

                packet = pickle.loads(packetStream);

                if not packet or not packet.PacketType:
                    # This is really just a sanity check and making sure nothing
                    # unknown is coming that could potentially break the server
                    break;

                LogUtility.Request(f"Packet type - {packet.PacketType}");

                if packet.PacketType in self.ValidPacketTypes:
                    self.HandlerContext.RedirectPacket(connection, packet);
                else:
                    clientKey = connection.getpeername();
                    client = self.Connections[clientKey];
                    # this has caught me off a few times
                    LogUtility.Error(f"Packet type is not supported - {packet.PacketType}, " +\
                        f"sent from {client.Name} - {clientKey}. Add to valid packet types!");
                    connection.sendall(pickle.dumps(False));

            except Exception as error:
                trace = traceback.format_exc();
                LogUtility.Error(str(error) + "\n\n" + trace);
                break;

        self.Disconnect(connection);

        return;

    def Connect(self, connection, packet):
        dto = packet.Data;

        player = Player(dto.ClientName, dto.ClientIdentifier);

        connectionKey = connection.getpeername();
        self.Connections[connectionKey] = player;

        LogUtility.Information(f"Connected to server (player {player}) - {connectionKey}");
        self.ShowActiveConnections();

        connection.sendall(pickle.dumps(player));

        return;

    def Disconnect(self, connection):
        connectionKey = connection.getpeername();
        player = None;

        if connectionKey in self.Connections.keys():
            player = self.Connections[connectionKey];
            gameIdentifier = self.HandlerContext.IsPlayerAlreadyInAGame(player);

            if gameIdentifier:
                game = self.HandlerContext.GetGameWithIdentifier(gameIdentifier);
                game.Leave(player);

            self.Connections.pop(connectionKey);

        LogUtility.Information(f"Lost connection (player {player}) to server - {connectionKey}");
        connection.shutdown(socket.SHUT_RDWR);
        connection.close();

        self.ShowActiveConnections();

        return;

if __name__ == "__main__":
    ServerInstance().Run();