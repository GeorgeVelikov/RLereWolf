import Shared.constants.NetConstants as NetConstants;
from Shared.enums.PacketTypeEnum import PacketTypeEnum;
from Shared.dtos.UpdatedEntityDto import UpdatedEntityDto;
from Shared.dtos.PlayerGameDto import PlayerGameDto;
import Shared.utility.LogUtility as LogUtility;
import Shared.constants.LogConstants as LogConstants;

from Werewolf.game.Game import Game;
from Werewolf.game.Player import Player;
from Werewolf.agents.DummyPlayer import DummyPlayer;

from Werewolf.game.actions.Vote import Vote;

import Server.utility.ConversionHelper as ConversionHelper;

from datetime import datetime;
import threading;
import socket;
import pickle;

class ServerInstance():
    def __init__(self):
        self.__connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        self.__connections = dict();
        self.__games = dict();
        self.CreateGame("Game 1");
        self.CreateGame("Game 2");
        self.CreateGame("Game 3");
        self.CreateGame("Game 4");

        lastGame = list(self.__games.values())[-1];
        for i in range(0, 20):
            player = DummyPlayer(f"player_{i}", lastGame);
            player._Player__isReady = True;
            lastGame.Join(player);

        LogUtility.Information("Server start up");

        return;

    @property
    def Games(self):
        return self.__games;

    @property
    def UtcNow(self):
        return datetime.utcnow();

    def ShowActiveConnections(self):
        LogUtility.Information(f"Active connections - {threading.activeCount() - 1}");

    #region Server

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

            except Exception as error:
                LogUtility.Error(str(error));
                break;

        self.Disconnect(connection);

        return;

    def Run(self):
        try:
            self.__connection.bind(NetConstants.ADDRESS);
            self.__connection.listen();

            LogUtility.Information(f"Server successfully started at {NetConstants.IP}:{NetConstants.PORT}");

            self.ShowActiveConnections();
        except socket.error as error:
            LogUtility.Error(str(error));

        while True:
            connection, address = self.__connection.accept();
            threading.Thread(target = self.ClientHandle, args = (connection, address)).start();
        return;

    def RedirectPacket(self, connection, packet):

        if packet.PacketType == PacketTypeEnum.Connect:
            self.Connect(connection, packet);

        elif packet.PacketType == PacketTypeEnum.GetGamesList:
            self.GetGamesList(connection, packet);

        elif packet.PacketType == PacketTypeEnum.JoinGame:
            self.JoinGame(connection, packet);

        elif packet.PacketType == PacketTypeEnum.LeaveGame:
            self.LeaveGame(connection, packet);

        elif packet.PacketType == PacketTypeEnum.GameLobby:
            self.GetGameLobby(connection, packet);

        elif packet.PacketType == PacketTypeEnum.VoteStart:
            self.VoteStart(connection, packet);

        elif packet.PacketType == PacketTypeEnum.VotePlayer:
            self.VotePlayer(connection, packet);

        elif packet.PacketType == PacketTypeEnum.AttackPlayer:
            self.AttackPlayer(connection, packet);

        elif packet.PacketType == PacketTypeEnum.DivinePlayer:
            self.DivinePlayer(connection, packet);

        elif packet.PacketType == PacketTypeEnum.GuardPlayer:
            self.GuardPlayer(connection, packet);

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

        if connectionKey in self.__connections.keys():
            player = self.__connections[connectionKey];
            gameIdentifier = self.IsPlayerAlreadyInAGame(player);

            if gameIdentifier:
                game = self.GetGameWithIdentifier(gameIdentifier);
                game.Leave(player);

            self.__connections.pop(connectionKey);

        LogUtility.Information(f"Lost connection (player {player}) to server - {connectionKey}");
        connection.shutdown(2);
        connection.close();

        return;

    def GetGamesList(self, connection, packet):

        games = [ConversionHelper.GameToListDto(game)\
            for game in self.__games.values()\
                if not game.HasStarted];

        connection.sendall(pickle.dumps(games));

        return;

    def JoinGame(self, connection, packet):
        dto = packet.Data;

        game = self.GetGameWithIdentifier(dto.GameIdentifier);

        if not game:
            connection.sendall(pickle.dumps(None));
            return;

        player = dto.Player;

        lastUpdatedUtc = datetime.utcnow();

        game.Join(player);

        LogUtility.CreateGameMessage(f"Player '{player.Name}' has joined.", game);

        gameDto = ConversionHelper.GameToDto(game, lastUpdatedUtc);

        updatedEntityDto = UpdatedEntityDto(gameDto, lastUpdatedUtc);

        connection.sendall(pickle.dumps(updatedEntityDto));

        return;

    def LeaveGame(self, connection, packet):
        dto = packet.Data;

        game = self.GetGameWithIdentifier(dto.GameIdentifier);

        if not game:
            connection.sendall(pickle.dumps(True));
            return;

        game.Leave(dto.Player);
        LogUtility.CreateGameMessage(f"Player '{dto.Player.Name}' has left.", game);

        connection.sendall(pickle.dumps(True));

        return;

    def CreateGame(self, connection, packet):
        # reuse the server-side call but encapsulate it with the connection and packet check
        raise NotImplementedError("Not implemented yet");

    def GetGameLobby(self, connection, packet):
        wrapper = packet.Data;

        playerGameIdentifierDto = wrapper.Entity;
        lastUpdatedUtc = wrapper.UpdatedUtc;

        game = self.GetGameWithIdentifier(playerGameIdentifierDto.GameIdentifier);
        player = game.GetPlayerByIdentifier(playerGameIdentifierDto.Player.Identifier)

        dto = PlayerGameDto(player, ConversionHelper.GameToDto(game, lastUpdatedUtc));

        updatedEntityDto = UpdatedEntityDto(dto, datetime.utcnow());

        connection.sendall(pickle.dumps(updatedEntityDto));

        return;

    def VoteStart(self, connection, packet):
        wrapper = packet.Data;

        playerGameIdentifierDto = wrapper.Entity;
        lastUpdatedUtc = wrapper.UpdatedUtc;

        game = self.GetGameWithIdentifier(playerGameIdentifierDto.GameIdentifier);
        player = game.GetPlayerByIdentifier(playerGameIdentifierDto.Player.Identifier);

        game.VoteStart(player);

        dto = PlayerGameDto(player, ConversionHelper.GameToDto(game, lastUpdatedUtc));

        updatedEntityDto = UpdatedEntityDto(dto, datetime.utcnow());

        connection.sendall(pickle.dumps(updatedEntityDto));

        return;

    def VotePlayer(self, connection, packet):
        dto = packet.Data;
        game = self.GetGameWithIdentifier(dto.GameIdentifier);

        if not self.IsGameActionValid(game, dto):
            connection.sendall(pickle.dumps(False));

        player = game.GetPlayerByIdentifier(dto.Player.Identifier);
        targetPlayer = game.GetPlayerByIdentifier(dto.TargetPlayerIdentifier);

        if game.HasPlayerVotedAlready(player.Identifier):
            LogUtility.Error(f"Player {player.Name} - {player.Identifier} has voted already", game);
            connection.sendall(pickle.dumps(False));
            return;

        vote = Vote(player, targetPlayer);
        game.Vote(vote);
        connection.sendall(pickle.dumps(True));
        return;

    def AttackPlayer(self, connection, packet):
        dto = packet.Data;
        game = self.GetGameWithIdentifier(dto.GameIdentifier);

        if not self.IsGameActionValid(game, dto):
            connection.sendall(pickle.dumps(False));

        player = game.GetPlayerByIdentifier(dto.Player.Identifier);
        targetPlayer = game.GetPlayerByIdentifier(dto.TargetPlayerIdentifier);

        if game.HasPlayerVotedAlready(player.Identifier):
            LogUtility.Error(f"Player {player.Name} - {player.Identifier} has attacked already", game);
            connection.sendall(pickle.dumps(False));
            return;

        vote = Vote(player, targetPlayer);
        game.Vote(vote);

        connection.sendall(pickle.dumps(True));
        return;

    def DivinePlayer(self, connection, packet):
        dto = packet.Data;
        game = self.GetGameWithIdentifier(dto.GameIdentifier);

        if not self.IsGameActionValid(game, dto):
            connection.sendall(pickle.dumps(False));

        player = game.GetPlayerByIdentifier(dto.Player.Identifier);
        targetPlayer = game.GetPlayerByIdentifier(dto.TargetPlayerIdentifier);

        if game.HasPlayerVotedAlready(player.Identifier):
            LogUtility.Error(f"Player {player.Name} - {player.Identifier} has divined already", game);
            connection.sendall(pickle.dumps(False));
            return;

        vote = Vote(player, targetPlayer);
        game.Vote(vote);

        connection.sendall(pickle.dumps(True));
        return;

    def GuardPlayer(self, connection, packet):
        dto = packet.Data;
        game = self.GetGameWithIdentifier(dto.GameIdentifier);

        if not self.IsGameActionValid(game, dto):
            connection.sendall(pickle.dumps(False));

        player = game.GetPlayerByIdentifier(dto.Player.Identifier);
        targetPlayer = game.GetPlayerByIdentifier(dto.TargetPlayerIdentifier);

        if game.HasPlayerVotedAlready(player.Identifier):
            LogUtility.Error(f"Player {player.Name} - {player.Identifier} has guarded already", game);
            connection.sendall(pickle.dumps(False));
            return;

        vote = Vote(player, targetPlayer);
        game.Vote(vote);

        connection.sendall(pickle.dumps(True));
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

    def IsPlayerAlreadyInAGame(self, playerIdentifier):
        for game in self.__games.values():
            if not game.Players:
                continue;

            player = next((p for p in game.Players\
                if p.Identifier == playerIdentifier), None);

            if player:
                return game.Identifier;

        return None;

    def IsGameActionValid(self, game, gameActionDto):
        if not game.Identifier == self.IsPlayerAlreadyInAGame(gameActionDto.Player.Identifier):
            LogUtility.Error(f"Player {dto.Player.Name} - {dto.Player.Identifier} is not in game", game);
            return False;

        if not gameActionDto.TargetPlayerIdentifier:
            # this is probably okay as it could be a wait call
            return True;

        if not game.Identifier == self.IsPlayerAlreadyInAGame(gameActionDto.TargetPlayerIdentifier):
            LogUtility.Error(f"Target player id {dto.TargetPlayerIdentifier} is not in game", game);
            return False;

        return True;

    #endregion

if __name__ == "__main__":
    ServerInstance().Run();
