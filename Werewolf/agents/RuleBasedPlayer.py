from Werewolf.agents.AgentPlayer import AgentPlayer;
from Werewolf.game.actions.Vote import Vote;

from Shared.enums.PlayerTypeEnum import PlayerTypeEnum;
from Shared.enums.TimeOfDayEnum import TimeOfDayEnum;
from Shared.enums.AgentTypeEnum import AgentTypeEnum;
import Shared.utility.LogUtility as LogUtility;

import random;

class RuleBasedPlayer(AgentPlayer):
    def __init__(self, name, game):
        super().__init__(name, game);

        # We keep a tally of every identifier we've ever played with for this instance
        self.__trust = {};
        self.__honestyFactor = random.uniform(0, 1);

    @property
    def AgentType(self):
        return AgentTypeEnum.RuleBasedAgent;

    def Act(self):
        action = None;

        if not self.IsAlive or not self.Game.HasStarted:
            return None;

        if self.Game.TimeOfDay == TimeOfDayEnum.Day:
            self.Talk();
            action = self.ActDay();
        elif self.Game.TimeOfDay == TimeOfDayEnum.Night:
            action = self.ActNight();

        return action;

    def ActDay(self):
        action = None;

        if not self.IsAlive or not self.Game.HasStarted:
            return None;

        self.Talk();

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
        for player in self.Game.Players:

            if player.Identifier != self.Identifier \
                and player.Identifier not in self.__trust:

                self.__trust[player.Identifier] = 0.0;

            pass;

        return;

    def PostGameSetup(self):
        return;

    #region Day

    def ActDayVillager(self):
        viablePlayersToVoteFor = [player for player in self.Game.Players\
            if player.IsAlive\
                and player.Identifier != self.Identifier];

        if not viablePlayersToVoteFor:
            return Vote(self, None);

        playersOrderedByTrust = sorted(viablePlayersToVoteFor,\
            key = lambda p: self.__trust[p.Identifier]);

        leastTrustedPlayer = next((p for p in playersOrderedByTrust), None);

        playerToVoteFor = leastTrustedPlayer if leastTrustedPlayer\
            else random.choice(viablePlayersToVoteFor);

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

        playersOrderedByTrust = sorted(viablePlayersToDivine,\
            key = lambda p: self.__trust[p.Identifier]);

        leastTrustedPlayer = next((p for p in playersOrderedByTrust), None);

        playerToDivine = leastTrustedPlayer if leastTrustedPlayer\
            else random.choice(viablePlayersToDivine);

        return Vote(self, playerToDivine);

    def ActNightGuard(self):
        viablePlayersToGuard = [player for player in self.Game.Players\
            if player.IsAlive];

        if not viablePlayersToGuard:
            return Vote(self, None);

        playerToGuard = random.choice(viablePlayersToGuard);

        return Vote(self, playerToGuard);

    #endregion

    #region Commiunication

    #@ray.remove(num_gpus)
    def Talk(self):

        # create message
        # add message to game

        # sway other players
        agents = self.Game.AgentPlayers;

        for agent in agents:
            agent.Sway();

        return;

    def Sway(self):
        return;

    #endregion
