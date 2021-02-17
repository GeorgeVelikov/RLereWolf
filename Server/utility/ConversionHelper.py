from Shared.dtos.GameDto import GameDto;
from Werewolf.game.Game import Game;

def GameToDto(game, lastUpdatedUtc):
    if not game:
        return None;

    # don't give any messages if there is no last updated date specified
    messages = list();

    if lastUpdatedUtc:
        messages = [m for m in messages if m.TimeStampUtc >= lastUpdatedUtc];

    return GameDto(game.Identifier,\
        game.HasStarted,\
        game.Name,\
        messages,\
        game.Players,\
        game.TimeOfDay,\
        game.TurnPhase);
