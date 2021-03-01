import Shared.constants.GameConstants as GameConstants;
from Shared.enums.PlayerTypeEnum import PlayerTypeEnum;

from Werewolf.game.roles.Villager import Villager;
from Werewolf.game.roles.Werewolf import Werewolf;
from Werewolf.game.roles.Seer import Seer;
from Werewolf.game.roles.Guard import Guard;

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
            numberOfWerewolves * [Werewolf()],\
            numberOfSeers * [Seer()],\
            numberOfGuards * [Guard()],\
            numberOfVillagers * [Villager()]], []);

    for player in players:
        roleType = random.choice(rolesBag);
        rolesBag.remove(roleType);

        player._Player__role = roleType;

        print(f"Player {player.Name} is a {player.Role}.");

    return;


def GetPlayerCountForRole(playerCount, playersToRoleRatio):
    return 1 + ((playerCount - playersToRoleRatio) // playersToRoleRatio);