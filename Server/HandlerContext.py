from Server.handlers.GameActionHandler import GameActionHandler;
from Server.handlers.GameLobbyHandler import GameLobbyHandler;

import Shared.utility.LogUtility as LogUtility;
from Shared.enums.PacketTypeEnum import PacketTypeEnum;

class HandlerContext():
    def __init__(self, server):
        self.__server = server;
        self.__gameLobbyHandler = GameLobbyHandler(server, self);
        self.__gameActionHandler = GameActionHandler(server, self);

    @property
    def Server(self):
        return self.__server;

    @property
    def GameLobbyHandler(self):
        return self.__gameLobbyHandler;

    @property
    def GameActionHandler(self):
        return self.__gameActionHandler;

    def RedirectPacket(self, connection, packet):
        # TODO: is there a neat way of routing this, similarly to C# attributes?

        if packet.PacketType == PacketTypeEnum.Connect:
            self.Server.Connect(connection, packet);

        # game lobby calls
        elif packet.PacketType == PacketTypeEnum.GetGamesList:
            self.GameLobbyHandler.GetGamesList(connection, packet);

        elif packet.PacketType == PacketTypeEnum.JoinGame:
            self.GameLobbyHandler.JoinGame(connection, packet);

        elif packet.PacketType == PacketTypeEnum.LeaveGame:
            self.GameLobbyHandler.LeaveGame(connection, packet);

        elif packet.PacketType == PacketTypeEnum.GameLobby:
            self.GameLobbyHandler.GetGameLobby(connection, packet);

        # game action calls

        elif packet.PacketType == PacketTypeEnum.AddAgent:
            self.GameActionHandler.AddAgentToGame(connection, packet);

        elif packet.PacketType == PacketTypeEnum.RemoveAgent:
            self.GameActionHandler.RemoveAgentFromGame(connection, packet);

        elif packet.PacketType == PacketTypeEnum.VoteStart:
            self.GameActionHandler.VoteStart(connection, packet);

        elif packet.PacketType == PacketTypeEnum.VotePlayer:
            self.GameActionHandler.VotePlayer(connection, packet);

        elif packet.PacketType == PacketTypeEnum.Talk:
            self.GameActionHandler.Talk(connection, packet);

        elif packet.PacketType == PacketTypeEnum.Whisper:
            self.GameActionHandler.Whisper(connection, packet);

        elif packet.PacketType == PacketTypeEnum.AttackPlayer:
            self.GameActionHandler.AttackPlayer(connection, packet);

        elif packet.PacketType == PacketTypeEnum.DivinePlayer:
            self.GameActionHandler.DivinePlayer(connection, packet);

        elif packet.PacketType == PacketTypeEnum.GuardPlayer:
            self.GameActionHandler.GuardPlayer(connection, packet);

        return;

    def GetGameWithIdentifier(self, gameIdentifier):
        if not gameIdentifier in self.Server.Games.keys():
            LogUtility.Error(f"Game {gameIdentifier} does not exist.");
            return None;

        return self.Server.Games[gameIdentifier];

    def IsPlayerAlreadyInAGame(self, playerIdentifier):
        for game in self.Server.Games.values():
            if not game.Players:
                continue;

            player = next((p for p in game.Players\
                if p.Identifier == playerIdentifier), None);

            if player:
                return game.Identifier;

        return None;

    def IsGameActionValid(self, game, gameActionDto):
        if not game.Identifier == self.IsPlayerAlreadyInAGame(gameActionDto.Player.Identifier):
            LogUtility.Error(f"'{dto.Player.Name}' - {dto.Player.Identifier} is not in game", game);
            return False;

        if not gameActionDto.TargetPlayerIdentifier:
            # this is probably okay as it could be a wait call
            return True;

        if not game.Identifier == self.IsPlayerAlreadyInAGame(gameActionDto.TargetPlayerIdentifier):
            LogUtility.Error(f"Target player id {dto.TargetPlayerIdentifier} is not in game", game);
            return False;

        return True;
