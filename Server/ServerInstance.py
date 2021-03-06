from Server.HandlerContext import HandlerContext;

import Shared.constants.NetConstants as NetConstants;
from Shared.enums.PacketTypeEnum import PacketTypeEnum;
import Shared.utility.LogUtility as LogUtility;

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
        self.__connections = dict();
        self.__games = dict();
        self.CreateGame("Game 1");
        self.CreateGame("Game 2");
        self.CreateGame("Game 3");
        self.CreateGame("Game 4");

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
    def UtcNow(self):
        return datetime.utcnow();

    def ShowActiveConnections(self):
        LogUtility.Information(f"Active connections - {threading.activeCount() - 1}");

    #region Server

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

                packet = pickle.loads(packetStream);

                if not packet:
                    break;

                LogUtility.Request(f"Packet type - {packet.PacketType}");

                validPacketTypes = PacketTypeEnum.Values();

                if packet.PacketType in validPacketTypes:
                    self.RedirectPacket(connection, packet);
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

    def RedirectPacket(self, connection, packet):
        # TODO: is there a neat way of routing this, similarly to C# attributes?

        if packet.PacketType == PacketTypeEnum.Connect:
            self.Connect(connection, packet);

        # game lobby calls
        elif packet.PacketType == PacketTypeEnum.GetGamesList:
            self.HandlerContext.GameLobbyHandler.GetGamesList(connection, packet);

        elif packet.PacketType == PacketTypeEnum.JoinGame:
            self.HandlerContext.GameLobbyHandler.JoinGame(connection, packet);

        elif packet.PacketType == PacketTypeEnum.LeaveGame:
            self.HandlerContext.GameLobbyHandler.LeaveGame(connection, packet);

        elif packet.PacketType == PacketTypeEnum.GameLobby:
            self.HandlerContext.GameLobbyHandler.GetGameLobby(connection, packet);

        # game action calls

        elif packet.PacketType == PacketTypeEnum.AddAgent:
            self.HandlerContext.GameActionHandler.AddAgentToGame(connection, packet);

        elif packet.PacketType == PacketTypeEnum.RemoveAgent:
            self.HandlerContext.GameActionHandler.RemoveAgentFromGame(connection, packet);

        elif packet.PacketType == PacketTypeEnum.VoteStart:
            self.HandlerContext.GameActionHandler.VoteStart(connection, packet);

        elif packet.PacketType == PacketTypeEnum.VotePlayer:
            self.HandlerContext.GameActionHandler.VotePlayer(connection, packet);

        elif packet.PacketType == PacketTypeEnum.AttackPlayer:
            self.HandlerContext.GameActionHandler.AttackPlayer(connection, packet);

        elif packet.PacketType == PacketTypeEnum.DivinePlayer:
            self.HandlerContext.GameActionHandler.DivinePlayer(connection, packet);

        elif packet.PacketType == PacketTypeEnum.GuardPlayer:
            self.HandlerContext.GameActionHandler.GuardPlayer(connection, packet);

        return;

    #endregion

    #region Game calls

    def Connect(self, connection, packet):
        dto = packet.Data;

        player = Player(dto.ClientName, dto.ClientIdentifier);

        connectionKey = connection.getpeername();
        self.__connections[connectionKey] = player;

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

            self.__connections.pop(connectionKey);

        LogUtility.Information(f"Lost connection (player {player}) to server - {connectionKey}");
        connection.shutdown(socket.SHUT_RDWR);
        connection.close();

        return;

    #endregion

    #region Server only calls

    def CreateGame(self, name):
        game = Game(name);

        self.__games[game.Identifier] = game;

        return game;

    #endregion

if __name__ == "__main__":
    ServerInstance().Run();
