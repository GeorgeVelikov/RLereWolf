from Werewolf.agents.AgentPlayer import AgentPlayer;
from Werewolf.game.actions.Vote import Vote;

from Shared.enums.PlayerTypeEnum import PlayerTypeEnum;
from Shared.enums.TimeOfDayEnum import TimeOfDayEnum;
from Shared.enums.AgentTypeEnum import AgentTypeEnum;
import Shared.utility.LogUtility as LogUtility;

import random;

class DummyPlayer(AgentPlayer):
    def __init__(self, name, game):
        super().__init__(name, game);

    @property
    def AgentType(self):
        return AgentTypeEnum.DummyAgent;

    def Act(self):
        action = None;

        if not self.IsAlive or not self.Game.HasStarted:
            return None;

        if self.Game.TimeOfDay == TimeOfDayEnum.Day:
            action = self.ActDay();
        elif self.Game.TimeOfDay == TimeOfDayEnum.Night:
            action = self.ActNight();

        return action;

    def ActDay(self):
        action = None;

        if not self.IsAlive or not self.Game.HasStarted:
            return None;

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
            return None;

        if self.Role.Type == PlayerTypeEnum.Villager:
            action = self.ActNightVillager();
        elif self.Role.Type == PlayerTypeEnum.Werewolf:
            action = self.ActNightWerewolf();
        elif self.Role.Type == PlayerTypeEnum.Seer:
            action = self.ActNightSeer();
        elif self.Role.Type == PlayerTypeEnum.Guard:
            action = self.ActNightGuard();

        return action;

    def PreGameSetup(self):
        return;

    def PostGameSetup(self):
        return;

    #region Day

    def ActDayVillager(self):
        viablePlayersToVoteFor = [player for player in self.Game.Players\
            if player.IsAlive\
                and player.Identifier != self.Identifier]

        if not viablePlayersToVoteFor:
            return Vote(self, None);

        playerToVoteFor = random.choice(viablePlayersToVoteFor);

        return Vote(self, playerToVoteFor);

    def ActDayWerewolf(self):
        viablePlayersToVoteFor = [player for player in self.Game.Players\
            if player.IsAlive\
                and player.Identifier != self.Identifier\
                and player.Role.Type != PlayerTypeEnum.Werewolf]

        if not viablePlayersToVoteFor:
            return Vote(self, None);

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
            return Vote(self, None);

        playerToKill = random.choice(viablePlayersToVoteFor);

        return Vote(self, playerToKill);

    def ActNightSeer(self):
        viablePlayersToDivine = [player for player in self.Game.Players\
            if player.Identifier != self.Identifier];

        if not viablePlayersToDivine:
            return Vote(self, None);

        playerToDivine = random.choice(viablePlayersToDivine);

        return Vote(self, playerToDivine);

    def ActNightGuard(self):
        viablePlayersToGuard = [player for player in self.Game.Players\
            if player.IsAlive];

        if not viablePlayersToGuard:
            return Vote(self, None);

        playerToGuard = random.choice(viablePlayersToGuard);

        return Vote(self, playerToGuard);

    #endregion

    #region Communication

    def Talk(self):
        return;

    def Sway(self):
        return;

    #endregion
