from Werewolf.agents.AgentPlayer import AgentPlayer;
from Werewolf.game.actions.Vote import Vote;

from Shared.enums.AgentTypeEnum import AgentTypeEnum;

import random;

class TrainablePlayer(AgentPlayer):
    def __init__(self, name, game):
        super().__init__(name, game);

    @property
    def AgentType(self):
        return AgentTypeEnum.TrainableAgent;

    # overrides from the base Agent class, needed by the client-server
    # game implementation to force a play from the user
    def ActDay(self):
        return self.Act();

    def ActNight(self):
        return self.Act();

    def Act(self):
        action = None;

        if not self.IsAlive or not self.Game.HasStarted:
            return None;

        # Currently random, we'll add metrics later
        playersToVoteFor = [player for player in self.Game.Players];

        if not playersToVoteFor:
            return Vote(self, None);

        votedPlayer = None

        # default to waiting
        if random.random() < 0.5:
            votedPlayer = random.choice(playersToVoteFor);

        action = Vote(self, votedPlayer);

        return action;

    def PreGameSetup(self):
        return;

    def PostGameSetup(self):
        return;

    #region Communication

    def Talk(self):
        return;

    def Sway(self):
        return;

    #endregion
