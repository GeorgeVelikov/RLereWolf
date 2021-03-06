import Server.utility.ConversionHelper as ConversionHelper;
from Server.handlers.HandlerBase import HandlerBase;

from Shared.dtos.UpdatedEntityDto import UpdatedEntityDto;
from Shared.dtos.PlayerGameDto import PlayerGameDto;

import pickle;

class GameLobbyHandler(HandlerBase):
    def __init__(self, server, handlerContext):
        super().__init__(server, handlerContext);

    def GetGamesList(self, connection, packet):

        games = [ConversionHelper.GameToListDto(game)\
            for game in self.Games.values()\
                if not game.HasStarted];

        connection.sendall(pickle.dumps(games));

        return;

    def JoinGame(self, connection, packet):
        dto = packet.Data;

        game = self.HandlerContext.GetGameWithIdentifier(dto.GameIdentifier);

        if not game or game.IsFull:
            connection.sendall(pickle.dumps(None));
            return;

        player = dto.Player;

        lastUpdatedUtc = self.Server.UtcNow;

        game.Join(player);

        gameDto = ConversionHelper.GameToDto(game, lastUpdatedUtc);

        updatedEntityDto = UpdatedEntityDto(gameDto, lastUpdatedUtc);

        connection.sendall(pickle.dumps(updatedEntityDto));

        return;

    def LeaveGame(self, connection, packet):
        dto = packet.Data;

        game = self.HandlerContext.GetGameWithIdentifier(dto.GameIdentifier);

        if not game:
            connection.sendall(pickle.dumps(True));
            return;

        game.Leave(dto.Player);

        connection.sendall(pickle.dumps(True));

        return;

    def CreateGame(self, connection, packet):
        # reuse the server-side call but encapsulate it with the connection and packet check
        raise NotImplementedError("Not implemented yet");

    def GetGameLobby(self, connection, packet):
        wrapper = packet.Data;

        playerGameIdentifierDto = wrapper.Entity;
        lastUpdatedUtc = wrapper.UpdatedUtc;

        game = self.HandlerContext.GetGameWithIdentifier(playerGameIdentifierDto.GameIdentifier);
        player = game.GetPlayerByIdentifier(playerGameIdentifierDto.Player.Identifier)

        dto = PlayerGameDto(player, ConversionHelper.GameToDto(game, lastUpdatedUtc));

        updatedEntityDto = UpdatedEntityDto(dto, self.Server.UtcNow);

        connection.sendall(pickle.dumps(updatedEntityDto));

        return;
