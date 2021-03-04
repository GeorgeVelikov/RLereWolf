from Werewolf.agents.AgentPlayer import AgentPlayer;
from Werewolf.game.actions.Vote import Vote;

from Shared.enums.PlayerTypeEnum import PlayerTypeEnum
import Shared.utility.LogUtility as LogUtility;

import random;

class DummyPlayer(AgentPlayer):
    def __init__(self, name, game):
        super().__init__(name, game);

    def ActDay(self):
        if not self.IsAlive or not self.Game.HasStarted:
            return;

        if self.Role.Type == PlayerTypeEnum.Villager:
            self.ActDayVillager();
        elif self.Role.Type == PlayerTypeEnum.Werewolf:
            self.ActDayWerewolf();
        elif self.Role.Type == PlayerTypeEnum.Seer:
            self.ActDayVillager();
        elif self.Role.Type == PlayerTypeEnum.Guard:
            self.ActDayVillager();

        return;

    def ActNight(self):
        if not self.IsAlive or not self.Game.HasStarted:
            return;

        if self.Role.Type == PlayerTypeEnum.Villager:
            self.ActNightVillager();
        elif self.Role.Type == PlayerTypeEnum.Werewolf:
            self.ActNightWerewolf();
        elif self.Role.Type == PlayerTypeEnum.Seer:
            self.ActNightSeer();
        elif self.Role.Type == PlayerTypeEnum.Guard:
            self.ActNightGuard();

        return;

    #region Day

    def ActDayVillager(self):
        viablePlayersToVoteFor = [player for player in self.Game.Players\
            if player.IsAlive\
                and player.Identifier != self.Identifier]

        if not viablePlayersToVoteFor:
            return;

        playerToVoteFor = random.choice(viablePlayersToVoteFor);

        vote = Vote(self, playerToVoteFor)

        self.Game.Vote(vote);
        return;

    def ActDayWerewolf(self):
        viablePlayersToVoteFor = [player for player in self.Game.Players\
            if player.IsAlive\
                and player.Identifier != self.Identifier\
                and player.Role != PlayerTypeEnum.Werewolf]

        if not viablePlayersToVoteFor:
            return;

        playerToVoteFor = random.choice(viablePlayersToVoteFor);

        vote = Vote(self, playerToVoteFor)

        self.Game.Vote(vote);
        return;

    #endregion

    #region Night

    def ActNightVillager(self):
        return;

    def ActNightWerewolf(self):
        viablePlayersToVoteFor = [player for player in self.Game.Players\
            if player.IsAlive\
                and player.Identifier != self.Identifier\
                and player.Role != PlayerTypeEnum.Werewolf]

        if not viablePlayersToVoteFor:
            return;

        playerToKill = random.choice(viablePlayersToVoteFor);

        vote = Vote(self, playerToKill)

        self.Game.Vote(vote);
        return;

    def ActNightSeer(self):
        viablePlayersToDivine = [player for player in self.Game.Players\
            if player.Identifier != self.Identifier];

        if not viablePlayersToDivine:
            return;

        playerToDivine = random.choice(viablePlayersToDivine);

        vote = Vote(self, playerToDivine)

        self.Game.Vote(vote);
        return;

    def ActNightGuard(self):
        viablePlayersToGuard = [player for player in self.Game.Players\
            if player.IsAlive];

        if not viablePlayersToGuard:
            return;

        playerToGuard = random.choice(viablePlayersToGuard);

        vote = Vote(self, playerToGuard)

        self.Game.Vote(vote);
        return;

    #endregion