from Werewolf.agents.AgentPlayer import AgentPlayer;
from Werewolf.game.actions.Vote import Vote;

from Shared.enums.PlayerTypeEnum import PlayerTypeEnum
import Shared.utility.LogUtility as LogUtility;

import random;

class DummyPlayer(AgentPlayer):
    def __init__(self, name, game):
        super().__init__(name, game);

    def ActDay(self):
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

        LogUtility.CreateGameMessage(f"Player {self.Name} voted to execute {playerToVoteFor.Name}.", self.Game);

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

        LogUtility.CreateGameMessage(f"Player {self.Name} voted to execute {playerToVoteFor.Name}.", self.Game);

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

        LogUtility.CreateGameMessage(f"Player {self.Name} voted to execute {playerToKill.Name}.", self.Game);

        return;

    def ActNightSeer(self):
        return;

    def ActNightGuard(self):
        return;

    #endregion