from Shared.dtos.GameDto import GameDto;
from Werewolf.game.Game import Game;

def GameToDto(game):
    if not game:
        return None;

    return GameDto(game.Identifier,\
        game.HasStarted,\
        game.Name,\
        game.Messages,\
        game.Players,\
        game.TimeOfDay,\
        game.TurnPhase);
