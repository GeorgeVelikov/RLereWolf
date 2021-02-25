import Shared.constants.GameConstants as GameConstants;
from Shared.enums.PlayerTypeEnum import PlayerTypeEnum;

import random;

def DistributeRolesBaseGame(players):
    playerCount = len(players);

    numberOfWerewolves = GetPlayerCountForRole(playerCount, GameConstants.PLAYERS_PER_WEREWOLF);
    numberOfSeers = GetPlayerCountForRole(playerCount, GameConstants.PLAYERS_PER_SEER);
    numberOfGuards = GetPlayerCountForRole(playerCount, GameConstants.PLAYERS_PER_GUARD);

    numberOfVillagers = playerCount \
        - numberOfWerewolves\
        - numberOfSeers\
        - numberOfGuards;

    rolesBag = \
        sum([\
            numberOfWerewolves * [PlayerTypeEnum.Werewolf],\
            numberOfSeers * [PlayerTypeEnum.Seer],\
            numberOfGuards * [PlayerTypeEnum.Guard],\
            numberOfVillagers * [PlayerTypeEnum.Villager]], []);

    for player in players:
        roleType = random.choice(rolesBag);
        rolesBag.remove(roleType);

        player._Player__role = roleType;

        print(f"Player {player.Name} is a {player.Role}.");

    return;


def GetPlayerCountForRole(playerCount, playersToRoleRatio):
    return 1 + ((playerCount - playersToRoleRatio) // playersToRoleRatio);