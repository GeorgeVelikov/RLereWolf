from Werewolf.agents.AgentPlayer import AgentPlayer;
from Werewolf.game.actions.Vote import Vote;

import random;

class TrainablePlayer(AgentPlayer):
    def __init__(self, name, game):
        super().__init__(name, game);

    def Act(self):
        action = None;

        if not self.IsAlive or not self.Game.HasStarted:
            return None;

        # Currently random, we'll add metrics later
        playersToVoteFor = [player for player in self.Game.Players];

        if not playersToVoteFor:
            return None;

        votedPlayer = None

        # default to waiting
        if random.random() < 0.5:
            votedPlayer = random.choice(playersToVoteFor);

        action = Vote(self, votedPlayer);

        return action;