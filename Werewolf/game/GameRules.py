import Shared.constants.GameConstants as GameConstants;
import Shared.utility.LogUtility as LogUtility;
from Shared.enums.PlayerTypeEnum import PlayerTypeEnum;

from Werewolf.game.roles.Villager import Villager;
from Werewolf.game.roles.Werewolf import Werewolf;
from Werewolf.game.roles.Seer import Seer;
from Werewolf.game.roles.Guard import Guard;

import random;

def DistributeRolesBaseGame(game):
    players = game.Players;
    playerCount = len(players);

    numberOfWerewolves = GetPlayerCountForRole(playerCount, GameConstants.PLAYERS_PER_WEREWOLF);
    numberOfSeers = GetPlayerCountForRole(playerCount, GameConstants.PLAYERS_PER_SEER);
    numberOfGuards = GetPlayerCountForRole(playerCount, GameConstants.PLAYERS_PER_GUARD);

    numberOfVillagers = playerCount\
        - numberOfWerewolves\
        - numberOfSeers\
        - numberOfGuards;

    if (numberOfVillagers < 0):
        LogUtility.Error("Cannot have a game with less than 0 villagers.", game);

    if (numberOfVillagers == 0):
        LogUtility.Warning("Game has 0 villagers.", game);

    rolesBag = sum([\
        numberOfWerewolves * [Werewolf()],\
        numberOfSeers * [Seer()],\
        numberOfGuards * [Guard()],\
        numberOfVillagers * [Villager()]], []);

    for player in players:
        roleType = random.choice(rolesBag);
        rolesBag.remove(roleType);

        player._Player__role = roleType;

        LogUtility.Information(f"'{player.Name}' is a {player.Role.Type}.", game);

    return;

def DoWerewolvesWin(game):
    werewolves = [w for w in game.Players if w.IsAlive\
        and w.Role.Type == PlayerTypeEnum.Werewolf];

    villagers = [w for w in game.Players if w.IsAlive\
        and w.Role.Type != PlayerTypeEnum.Werewolf];

    # this just makes debugging easier since this gets called many times
    if len(werewolves) < len(villagers):
        return False;

    werewolfNames = "\n\t\t\t  "+ "\n\t\t\t  "\
        .join([w.Name for w in game.Players if w.Role.Type == PlayerTypeEnum.Werewolf]);

    LogUtility.CreateGameMessage(f"\n\n\n\t\t\tWerewolves win!{werewolfNames}\n\n", game);
    return True;

def DoVillagersWin(game):
    werewolves = [w for w in game.Players if w.IsAlive\
        and w.Role.Type == PlayerTypeEnum.Werewolf]

    if werewolves:
        return False;

    # if all werewolves are dead, the villagers win
    LogUtility.CreateGameMessage("\n\n\n\t\t\tVillagers win!\n\n", game);
    return True;

def GetPlayerCountForRole(playerCount, playersToRoleRatio):
    additionalCount = (playerCount - playersToRoleRatio) // playersToRoleRatio;
    return 1 + (additionalCount if additionalCount > 0 else 0);