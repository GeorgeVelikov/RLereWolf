import Shared.constants.GameConstants as GameConstants;
from Shared.enums.PlayerTypeEnum import PlayerTypeEnum;

from Werewolf.roles.Villager import Villager;
from Werewolf.roles.Seer import Seer;
from Werewolf.roles.Guard import Guard;
from Werewolf.roles.Werewolf import Werewolf;

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
            numberOfWerewolves * [str(PlayerTypeEnum.Werewolf)],\
            numberOfSeers * [str(PlayerTypeEnum.Seer)],\
            numberOfGuards * [str(PlayerTypeEnum.Guard)],\
            numberOfVillagers * [str(PlayerTypeEnum.Villager)]], []);

    for player in players:
        roleType = random.choice(rolesBag);
        rolesBag.remove(roleType);

        if roleType == str(PlayerTypeEnum.Villager):
            player._Player__role = Villager(player.Name);

        elif roleType == str(PlayerTypeEnum.Werewolf):
            player._Player__role = Werewolf(player.Name);

        elif roleType == str(PlayerTypeEnum.Seer):
            player._Player__role = Seer(player.Name);

        elif roleType == str(PlayerTypeEnum.Guard):
            player._Player__role = Guard(player.Name);

        print(f"Player {player.Name} is a {player.Role.Role}.");

    return;


def GetPlayerCountForRole(playerCount, playersToRoleRatio):
    return 1 + ((playerCount - playersToRoleRatio) // playersToRoleRatio);