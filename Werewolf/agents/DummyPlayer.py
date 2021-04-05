from Werewolf.agents.AgentPlayer import AgentPlayer;
from Werewolf.game.actions.Vote import Vote;

from Shared.enums.PlayerTypeEnum import PlayerTypeEnum
import Shared.utility.LogUtility as LogUtility;

import random;

class DummyPlayer(AgentPlayer):
    def __init__(self, name, game):
        super().__init__(name, game);

    def ActDay(self):
        action = None;

        if not self.IsAlive or not self.Game.HasStarted:
            return action;

        if self.Role.Type == PlayerTypeEnum.Villager:
            action = self.ActDayVillager();
        elif self.Role.Type == PlayerTypeEnum.Werewolf:
            action = self.ActDayWerewolf();
        elif self.Role.Type == PlayerTypeEnum.Seer:
            action = self.ActDayVillager();
        elif self.Role.Type == PlayerTypeEnum.Guard:
            action = self.ActDayVillager();

        return action;

    def ActNight(self):
        action = None;

        if not self.IsAlive or not self.Game.HasStarted:
            return action;

        if self.Role.Type == PlayerTypeEnum.Villager:
            action = self.ActNightVillager();
        elif self.Role.Type == PlayerTypeEnum.Werewolf:
            action = self.ActNightWerewolf();
        elif self.Role.Type == PlayerTypeEnum.Seer:
            action = self.ActNightSeer();
        elif self.Role.Type == PlayerTypeEnum.Guard:
            action = self.ActNightGuard();

        return action;

    #region Day

    def ActDayVillager(self):
        viablePlayersToVoteFor = [player for player in self.Game.Players\
            if player.IsAlive\
                and player.Identifier != self.Identifier]

        if not viablePlayersToVoteFor:
            return;

        playerToVoteFor = random.choice(viablePlayersToVoteFor);

        return Vote(self, playerToVoteFor);

    def ActDayWerewolf(self):
        viablePlayersToVoteFor = [player for player in self.Game.Players\
            if player.IsAlive\
                and player.Identifier != self.Identifier\
                and player.Role.Type != PlayerTypeEnum.Werewolf]

        if not viablePlayersToVoteFor:
            return;

        playerToVoteFor = random.choice(viablePlayersToVoteFor);

        return Vote(self, playerToVoteFor);

    #endregion

    #region Night

    def ActNightVillager(self):
        return;

    def ActNightWerewolf(self):
        viablePlayersToVoteFor = [player for player in self.Game.Players\
            if player.IsAlive\
                and player.Identifier != self.Identifier\
                and player.Role.Type != PlayerTypeEnum.Werewolf]

        if not viablePlayersToVoteFor:
            return;

        playerToKill = random.choice(viablePlayersToVoteFor);

        return Vote(self, playerToKill);

    def ActNightSeer(self):
        viablePlayersToDivine = [player for player in self.Game.Players\
            if player.Identifier != self.Identifier];

        if not viablePlayersToDivine:
            return;

        playerToDivine = random.choice(viablePlayersToDivine);

        return Vote(self, playerToDivine);

    def ActNightGuard(self):
        viablePlayersToGuard = [player for player in self.Game.Players\
            if player.IsAlive];

        if not viablePlayersToGuard:
            return None;

        playerToGuard = random.choice(viablePlayersToGuard);

        return Vote(self, playerToGuard);

    #endregion