import Server.utility.ConversionHelper as ConversionHelper;
from Server.handlers.HandlerBase import HandlerBase;

import Shared.constants.CommunicationPresetConstants as CommunicationPresets;
import Shared.utility.LogUtility as LogUtility;
from Shared.dtos.UpdatedEntityDto import UpdatedEntityDto;
from Shared.dtos.PlayerGameDto import PlayerGameDto;
from Shared.dtos.MessageMetaDataDto import MessageMetaDataDto;
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

        gameDto = ConversionHelper.GameToDto(game, lastUpdatedUtc, player);
        dto = PlayerGameDto(player, gameDto);

        updatedEntityDto = UpdatedEntityDto(dto, self.Server.UtcNow);

        connection.sendall(pickle.dumps(updatedEntityDto));

        return;

    def Talk(self, connection, packet):
        messageRequestDto = packet.Data;

        if not messageRequestDto or not messageRequestDto.IsValid:
            connection.sendall(pickle.dumps(False));
            return;

        game = self.HandlerContext.GetGameWithIdentifier(messageRequestDto.GameIdentifier);
        talkMessage = messageRequestDto.TalkMessage;

        player = game.GetPlayerByIdentifier(messageRequestDto.PlayerIdentifier);
        targetPlayer = None;

        if messageRequestDto.TargetPlayerIdentifier:
            targetPlayer = game.GetPlayerByIdentifier(messageRequestDto.TargetPlayerIdentifier);

        messageMetaDataDto = MessageMetaDataDto(\
            messageRequestDto.PlayerIdentifier,\
            messageRequestDto.TargetPlayerIdentifier,\
            messageRequestDto.TargetPlayerRole,\
            talkMessage.MessageType);

        messageText = self.ConstructMessageText(\
            talkMessage,\
            targetPlayer,\
            messageMetaDataDto.TargetRole);

        # this is automatically added to the game, no need to serialize
        # it and send it back the game loop will handle all of the magic
        messageDto = LogUtility.CreateTalkGameMessage(\
            player,\
            messageText,\
            messageMetaDataDto,\
            game);

        connection.sendall(pickle.dumps(True));
        return;

    def Whisper(self, connection, packet):
        messageRequestDto = packet.Data;

        if not messageRequestDto or not messageRequestDto.IsValid:
            connection.sendall(pickle.dumps(False));
            return;

        game = self.HandlerContext.GetGameWithIdentifier(messageRequestDto.GameIdentifier);
        talkMessage = messageRequestDto.TalkMessage;

        player = game.GetPlayerByIdentifier(messageRequestDto.PlayerIdentifier);
        targetPlayer = None;

        if messageRequestDto.TargetPlayerIdentifier:
            targetPlayer = game.GetPlayerByIdentifier(messageRequestDto.TargetPlayerIdentifier);

        messageMetaDataDto = MessageMetaDataDto(\
            messageRequestDto.PlayerIdentifier,\
            messageRequestDto.TargetPlayerIdentifier,\
            messageRequestDto.TargetPlayerRole,\
            talkMessage.MessageType);

        messageText = self.ConstructMessageText(\
            talkMessage,\
            targetPlayer,\
            messageMetaDataDto.TargetRole);

        # this is automatically added to the game, no need to serialize
        # it and send it back the game loop will handle all of the magic
        messageDto = LogUtility.CreateWhisperGameMessage(\
            player,\
            messageText,\
            messageMetaDataDto,\
            game,\
            player.Role.Type);

        connection.sendall(pickle.dumps(True));
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

    #region Helpers

    def ConstructMessageText(self, talkMessage, targetPlayer, targetRole):
        if not talkMessage:
            return None;

        text = talkMessage.MessageTemplate;

        if (CommunicationPresets.PLAYER in text) and targetPlayer:
            text = text\
                .replace(CommunicationPresets.PLAYER, targetPlayer.Name);
        elif (CommunicationPresets.PLAYER in text) and not targetPlayer:
            return None;

        if (CommunicationPresets.ROLE in text) and targetRole:
            text = text\
                .replace(CommunicationPresets.ROLE, str(targetRole));
        elif (CommunicationPresets.ROLE in text) and not targetRole:
            return None;

        return text;

    #endregion
