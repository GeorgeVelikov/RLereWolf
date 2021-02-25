from Werewolf.agents.dummy.DummyPlayer import DummyPlayer;
from Werewolf.game.actions.Vote import Vote;

import random;

class DummyVillager(DummyPlayer):
    def __init__(self, name, game):
        super().__init__(name, game);

    def ActDay(self):
        viablePlayersToVoteFor = [player for player in self.__game.Players\
            if player.IsAlive\
                and player.Identifier != self.Identifier]

        if not viablePlayersToVoteFor:
            return;

        playerToVoteFor = random.choice(viablePlayersToVoteFor);

        vote = Vote(self, playerToVoteFor)

        self.__game.Vote(vote);

        return;

    def ActNight(self):
        return;