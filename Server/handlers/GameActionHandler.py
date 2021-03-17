import Server.utility.ConversionHelper as ConversionHelper;
from Server.handlers.HandlerBase import HandlerBase;

import Shared.utility.LogUtility as LogUtility;
from Shared.dtos.UpdatedEntityDto import UpdatedEntityDto;
from Shared.dtos.PlayerGameDto import PlayerGameDto;
from Shared.utility.Helpers import GenerateFirstName;

from Werewolf.agents.DummyPlayer import DummyPlayer;
from Werewolf.game.actions.Vote import Vote;

import pickle;
import random;

class GameActionHandler(HandlerBase):
    def __init__(self, server, handlerContext):
        super().__init__(server, handlerContext);

    def AddAgentToGame(self, connection, packet):
        dto = packet.Data;
        gameIdentifier = dto.GameIdentifier;

        game = self.HandlerContext.GetGameWithIdentifier(gameIdentifier);

        if not game:
            connection.sendall(pickle.dumps(False));
            return;

        agent = DummyPlayer(GenerateFirstName(), game);

        connection.sendall(pickle.dumps(True));
        return;

    def RemoveAgentFromGame(self, connection, packet):
        dto = packet.Data;
        gameIdentifier = dto.GameIdentifier;

        game = self.HandlerContext.GetGameWithIdentifier(gameIdentifier);

        if not game.HasAgentPlayers:
            connection.sendall(pickle.dumps(True));
            return;

        randomAgent = random.choice(game.AgentPlayers);
        game.Leave(randomAgent);
        del randomAgent;

        connection.sendall(pickle.dumps(True));
        return;

    def VoteStart(self, connection, packet):
        wrapper = packet.Data;

        playerGameIdentifierDto = wrapper.Entity;
        lastUpdatedUtc = wrapper.UpdatedUtc;

        game = self.HandlerContext.GetGameWithIdentifier(playerGameIdentifierDto.GameIdentifier);
        player = game.GetPlayerByIdentifier(playerGameIdentifierDto.Player.Identifier);

        game.VoteStart(player);

        gameDto = ConversionHelper.GameToDto(game, lastUpdatedUtc, player.Identifier);
        dto = PlayerGameDto(player, gameDto);

        updatedEntityDto = UpdatedEntityDto(dto, self.Server.UtcNow);

        connection.sendall(pickle.dumps(updatedEntityDto));

        return;

    def VotePlayer(self, connection, packet):
        dto = packet.Data;
        game = self.HandlerContext.GetGameWithIdentifier(dto.GameIdentifier);

        if not self.HandlerContext.IsGameActionValid(game, dto):
            connection.sendall(pickle.dumps(False));

        player = game.GetPlayerByIdentifier(dto.Player.Identifier);
        targetPlayer = game.GetPlayerByIdentifier(dto.TargetPlayerIdentifier);

        if game.HasPlayerVotedAlready(player.Identifier):
            LogUtility.Error(f"'{player.Name}' - {player.Identifier} has voted already", game);
            connection.sendall(pickle.dumps(False));
            return;

        vote = Vote(player, targetPlayer);
        game.Vote(vote);
        connection.sendall(pickle.dumps(True));
        return;

    def AttackPlayer(self, connection, packet):
        dto = packet.Data;
        game = self.HandlerContext.GetGameWithIdentifier(dto.GameIdentifier);

        if not self.HandlerContext.IsGameActionValid(game, dto):
            connection.sendall(pickle.dumps(False));

        player = game.GetPlayerByIdentifier(dto.Player.Identifier);
        targetPlayer = game.GetPlayerByIdentifier(dto.TargetPlayerIdentifier);

        if game.HasPlayerVotedAlready(player.Identifier):
            LogUtility.Error(f"'{player.Name}' - {player.Identifier} has attacked already", game);
            connection.sendall(pickle.dumps(False));
            return;

        vote = Vote(player, targetPlayer);
        game.Vote(vote);

        connection.sendall(pickle.dumps(True));
        return;

    def DivinePlayer(self, connection, packet):
        dto = packet.Data;
        game = self.HandlerContext.GetGameWithIdentifier(dto.GameIdentifier);

        if not self.HandlerContext.IsGameActionValid(game, dto):
            connection.sendall(pickle.dumps(False));

        player = game.GetPlayerByIdentifier(dto.Player.Identifier);
        targetPlayer = game.GetPlayerByIdentifier(dto.TargetPlayerIdentifier);

        if game.HasPlayerVotedAlready(player.Identifier):
            LogUtility.Error(f"'{player.Name}' - {player.Identifier} has divined already", game);
            connection.sendall(pickle.dumps(False));
            return;

        vote = Vote(player, targetPlayer);
        game.Vote(vote);

        connection.sendall(pickle.dumps(True));
        return;

    def GuardPlayer(self, connection, packet):
        dto = packet.Data;
        game = self.HandlerContext.GetGameWithIdentifier(dto.GameIdentifier);

        if not self.HandlerContext.IsGameActionValid(game, dto):
            connection.sendall(pickle.dumps(False));

        player = game.GetPlayerByIdentifier(dto.Player.Identifier);
        targetPlayer = game.GetPlayerByIdentifier(dto.TargetPlayerIdentifier);

        if game.HasPlayerVotedAlready(player.Identifier):
            LogUtility.Error(f"'{player.Name}' - {player.Identifier} has guarded already", game);
            connection.sendall(pickle.dumps(False));
            return;

        vote = Vote(player, targetPlayer);
        game.Vote(vote);

        connection.sendall(pickle.dumps(True));
        return;
