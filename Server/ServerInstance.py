import Shared.constants.NetConstants as NetConstants;
import Shared.constants.GameConstants as GameConstants;
from Shared.enums.PacketTypeEnum import PacketTypeEnum;
from Shared.dtos.UpdatedEntityDto import UpdatedEntityDto;

from Werewolf.game.Game import Game;

import Server.utility.ConversionHelper as ConversionHelper;
import Server.utility.ServerUtility as ServerUtility;
import Server.constants.LogConstants as LogConstants;

from datetime import datetime;
import threading;
import socket;
import pickle;

class ServerInstance():
    def __init__(self):
        self.__connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        self.__connections = set();
        self.__games = dict();
        self.CreateGame("Game 1");
        self.CreateGame("Game 2");
        self.CreateGame("Game 3");
        self.CreateGame("Game 4");

        ServerUtility.Log(LogConstants.INFORMATION, "Server start up");

        return;

    @property
    def Games(self):
        return self.__games;

    @property
    def UtcNow(self):
        return datetime.utcnow();

    def ShowActiveConnections(self):
        ServerUtility.Log(LogConstants.INFORMATION, f"Active connections - {threading.activeCount() - 1}");

    #region Server

    def ClientHandle(self, connection, address):
        connection.send(b"Hello client");
        ServerUtility.Log(LogConstants.INFORMATION, f"Connected to server - {address}");
        self.ShowActiveConnections();

        while True:
            try:
                packetStream = connection.recv(4 * NetConstants.KILOBYTE);

                packet = pickle.loads(packetStream);

                if not packet:
                    break;

                ServerUtility.Log(LogConstants.REQUEST, f"Packet type - {str(packet.PacketType)}");

                validPacketTypes = PacketTypeEnum.Values()

                if packet.PacketType in validPacketTypes:
                    self.RedirectPacket(connection, packet);

            except Exception as error:
                ServerUtility.Log(LogConstants.ERROR, str(error));
                break;

        ServerUtility.Log(LogConstants.INFORMATION, f"Lost connection to server - {address}");
        connection.close();

        return;

    def Run(self):
        try:
            self.__connection.bind(NetConstants.ADDRESS);
            self.__connection.listen();

            ServerUtility.Log(LogConstants.INFORMATION, \
                f"Server successfully started at {NetConstants.IP}:{NetConstants.PORT}");

            self.ShowActiveConnections();
        except socket.error as error:
            ServerUtility.Log(LogConstants.ERROR, str(error));

        while True:
            connection, address = self.__connection.accept();
            threading.Thread(target = self.ClientHandle, args = (connection, address)).start();
        return;

    def RedirectPacket(self, connection, packet):
        if packet.PacketType == PacketTypeEnum.GetGamesList:
            self.GetGamesList(connection, packet);

        elif packet.PacketType == PacketTypeEnum.JoinGame:
            self.JoinGame(connection, packet);

        elif packet.PacketType == PacketTypeEnum.LeaveGame:
            self.LeaveGame(connection, packet);

        elif packet.PacketType == PacketTypeEnum.GameLobby:
            self.GetGameLobby(connection, packet);

        return;

    #endregion

    #region Game calls

    def Connect(self, connection, packet):
        client = packet.Data;

        connection.sendall(pickle.dumps(None));

        return;

    def GetGamesList(self, connection, packet):
        games = dict((identifier, game.Name)\
            for (identifier, game) in self.__games.items() \
                if not game.HasStarted);

        connection.sendall(pickle.dumps(games));

        return;

    def JoinGame(self, connection, packet):
        dto = packet.Data;

        game = self.GetGameWithIdentifier(dto.GameIdentifier);

        if not game:
            connection.sendall(pickle.dumps(None));

        player = dto.Player;

        lastUpdatedUtc = datetime.utcnow();

        game.Join(player);

        game.Messages.add(\
            ServerUtility.CreateGameMessage(f"Player '{player.Name}' has joined."));

        gameDto = ConversionHelper.GameToDto(game, lastUpdatedUtc);

        updatedEntityDto = UpdatedEntityDto(gameDto, lastUpdatedUtc);

        connection.sendall(pickle.dumps(updatedEntityDto));

        return;

    def LeaveGame(self, connection, packet):
        dto = packet.Data;

        game = self.GetGameWithIdentifier(dto.GameIdentifier);

        if not game:
            connection.sendall(pickle.dumps(True));

        game.Leave(dto.Player);
        connection.sendall(pickle.dumps(True));

        return;

    def CreateGame(self, connection, packet):
        # reuse the server-side call but encapsulate it with the connection and packet check
        raise NotImplementedError("Not implemented yet");

    def GetGameLobby(self, connection, packet):
        wrapper = packet.Data;

        playerGameDto = wrapper.Entity;
        lastUpdatedUtc = wrapper.UpdatedUtc;

        game = self.GetGameWithIdentifier(playerGameDto.GameIdentifier);

        gameDto = ConversionHelper.GameToDto(game, lastUpdatedUtc);

        updatedEntityDto = UpdatedEntityDto(gameDto, datetime.utcnow());

        connection.sendall(pickle.dumps(updatedEntityDto));

        return;

    #endregion

    #region Server only calls
    # Client cannot directly use those!

    def CreateGame(self, name):
        game = Game(name);

        self.__games[game.Identifier] = game;

        return;

    def GetGameWithIdentifier(self, gameIdentifier):
        if not gameIdentifier in self.__games:
            return None;

        return self.__games[gameIdentifier];

    #endregion

if __name__ == "__main__":
    ServerInstance().Run();
