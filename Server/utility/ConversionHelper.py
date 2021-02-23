from Shared.dtos.GameDto import GameDto;
from Shared.dtos.GameListDto import GameListDto;
from Werewolf.game.Game import Game;

def GameToDto(game, lastUpdatedUtc):
    if not game:
        return None;

    # don't give any messages if there is no last updated date specified
    messages = list();

    if lastUpdatedUtc:
        messages = [m for m in game.Messages if m.TimeUtc >= lastUpdatedUtc];

    return GameDto(game.Identifier,\
        game.HasStarted,\
        game.Name,\
        messages,\
        game.Players,\
        game.TimeOfDay);

def GameToListDto(game):
    if not game:
        return None;

    return GameListDto(game.Identifier,\
        game.Name,\
        len(game.Players));