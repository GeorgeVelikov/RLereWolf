import Shared.constants.GameConstants as GameConstants;
import Shared.utility.LogUtility as LogUtility;
from Shared.enums.TimeOfDayEnum import TimeOfDayEnum;
from Shared.enums.PlayerTypeEnum import PlayerTypeEnum;
from Shared.exceptions.GameException import GameException;

from Werewolf.agents.AgentPlayer import AgentPlayer;
import Werewolf.game.GameRules as GameRules;

import uuid;
from collections import Counter;

class Game():
    def __init__(self, name):
        self.__identifier = uuid.uuid4().hex;
        self.__hasStarted = False;
        self.__name = name;
        self.__messages = set();
        self.__votes = set();
        self.__turn = int();
        self.__players = set();
        self.__timeOfDay = TimeOfDayEnum._None;

    def __str__(self):
        return self.Name + " - " + self.Identifier;

    def __repr__(self):
        return self.Name + " - " + self.Identifier;

    #region properties

    @property
    def Name(self):
        return self.__name;

    @property
    def Identifier(self):
        return self.__identifier;

    @property
    def HasStarted(self):
        return self.__hasStarted;

    @property
    def Name(self):
        return self.__name;

    @property
    def Messages(self):
        return self.__messages;

    @property
    def Votes(self):
        return self.__votes;

    @property
    def Turn(self):
        return self.__turn;

    # Currently in the base game, this is interchangeable with DayPlayers
    # There isn't really any roles that cannot vote during the day as
    # that would effectively "out" them as being a specific role
    @property
    def Players(self):
        return sorted(self.__players,\
            key = lambda p: p.Name, \
            reverse = False);

    @property
    def PlayerIdentifiers(self):
        return [p.Identifier for p in self.__players];

    @property
    def NightPlayers(self):
        return [p for p in self.__players if p.Role.HasNightAction];

    @property
    def NightPlayerIdentifiers(self):
        # don't reference self.NightPlayers, that's an extra list comprehension
        return [p.Identifier for p in self.__players if p.Role.HasNightAction];

    @property
    def TimeOfDay(self):
        return self.__timeOfDay;

    @property
    def HasAgentPlayers(self):
        return any(player for player in self.__players \
            if issubclass(type(player), AgentPlayer));

    @property
    def AgentPlayers(self):
        return [player for player in self.__players \
            if issubclass(type(player), AgentPlayer)];

    #endregion

    #region Game calls

    def Join(self, player):
        self.__players.add(player);
        return;

    def Leave(self, player):
        if (player.Identifier not in self.PlayerIdentifiers):
            LogUtility.Error(f"Player {player.Identifier} is not in the game.", self);
            # TODO: raise some silent exception
            return;

        # no need to sort, already alphabetical
        self.__players\
            .remove(self.GetPlayerByIdentifier(player.Identifier));

    def Start(self):
        if (len(self.__players) < GameConstants.MINIMAL_PLAYER_COUNT):
            LogUtility.Error(
                f"Cannot start game without having at least {GameConstants.MINIMAL_PLAYER_COUNT} players.", self);
            return;

        for player in self.__players:
            player._Player__isReady = False;

        GameRules.DistributeRolesBaseGame(self);

        self.__hasStarted = True;
        self.__turn = 1;

        self.StartDay();

        return;

    def Restart(self):
        for player in self.__players:
            player._Player__isReady = False;
            player._Player__role = None;

        for agent in self.AgentPlayers:
            agent._Player__isReady = True;

        self.__hasStarted = False;
        self.__votes = set();
        self.__turn = int();
        self.__timeOfDay = TimeOfDayEnum._None;

    def StartDay(self):
        self.__votes = set();
        self.__timeOfDay = TimeOfDayEnum.Day;

        for agent in self.AgentPlayers:
            agent.ActDay();

        return;

    def StartNight(self):
        self.__votes = set();
        self.__timeOfDay = TimeOfDayEnum.Night;

        for agent in self.AgentPlayers:
            agent.ActNight();

        return;

    def VoteStart(self, player):
        if not player:
            return;

        player._Player__isReady = not player._Player__isReady;

        isThereAnyNonReadyPlayers = any(p for p in self.__players if not p.IsReady);

        if isThereAnyNonReadyPlayers:
            return;

        self.Start();

        return;

    def Vote(self, vote):
        if not vote:
            LogUtility.Error("Vote cannot be casted, it is null.", self);
            return;

        if self.TimeOfDay == TimeOfDayEnum.Day:
            self.VoteDay(vote);
            return;

        if self.TimeOfDay == TimeOfDayEnum.Night:
            self.VoteNight(vote);
            return;

        LogUtility.Error("Time of day is not Day/Night", self);
        return;

    #region Day

    def VoteDay(self, vote):
        playerIdentifiers = self.PlayerIdentifiers;

        if not vote.Player.Identifier in playerIdentifiers or\
            not vote.VotedPlayer.Identifier in playerIdentifiers:
            # players not in the game, error
            LogUtility.Error("Invalid vote, one of the players is not in the game", self);
            return;

        self.Votes.add(vote);

        LogUtility.CreateGameMessage(f"Player {vote.Player.Name} voted to execute {vote.VotedPlayer.Name}.", self);

        if len(self.Votes) == len(playerIdentifiers):
            self.CountVotesExecute();

        return;

    def CountVotesExecute(self):
        (player, times) = self.GetPlayerAndTimesVoted();

        LogUtility.CreateGameMessage(f"{player.Name} has the most votes to get executed - {times}.", self);

        self.Execute(player);
        self.StartNight();
        return;

    def Execute(self, player):
        if player not in self.Players:
            LogUtility.Error(f"Cannot execute {player.Name} as they are not in the game {self.Name}", self);
            return;

        player._Player__isAlive = False;
        LogUtility.CreateGameMessage(f"{player.Name} is executed.", self);

        return;

    #endregion

    #region Night

    def VoteNight(self, vote):
        playerIdentifiers = self.PlayerIdentifiers;
        playersWhoCanActAtNight = self.NightPlayerIdentifiers;

        if not vote.Player.Identifier in playersWhoCanActAtNight:
            playerDetails = vote.Player.Name + " - " +  vote.Player.Identifier;
            LogUtility.Error(f"Player {playerDetails} cannot act in the night.", self);
            return;

        if not vote.VotedPlayer.Identifier in playerIdentifiers:
            playerDetails = vote.VotedPlayer.Name + " - " +  vote.VotedPlayer.Identifier;
            LogUtility.Error(f"Invalid vote, target player {playerDetails} is not in the game", self);
            return;

        player = self.GetPlayerByIdentifier(vote.Player.Identifier);
        targetPlayer = self.GetPlayerByIdentifier(vote.VotedPlayer.Identifier);

        if player.Role.Type == PlayerTypeEnum.Werewolf:
            self.Attack(player, targetPlayer);
        elif player.Role.Type == PlayerTypeEnum.Seer:
            self.Divine(player, targetPlayer);
        elif player.Role.Type == PlayerTypeEnum.Guard:
            self.Guard(player, targetPlayer);
        else:
            # I know this should semantically be before the actual addition of
            # the vote. However, we rely on the previous security checks
            LogUtility.Error(f"Player {player.Name} does not have a valid night role - {player.Role.Type}", self);
            return;

        self.Votes.add(vote);

        if len(self.Votes) == len(playersWhoCanActAtNight):
            self.CountNightVotes();

        return;

    def Attack(self, werewolf, player):
        LogUtility.Information(f"Werewolf {werewolf.Name} attacks {player.Name}.", self);
        return;

    def Guard(self, guard, player):
        LogUtility.Information(f"Guard {guard.Name} guards {player.Name}.", self);
        return;

    def Divine(self, seer, player):
        LogUtility.Information(f"Seer {seer.Name} divines {player.Name}.", self);
        return;

    def CountNightVotes(self):
        # Get votes for kill
        # Get votes for seer (these are independent from everything else)
        # Get guard calls

        # Get most voted player to attack, check if they're guarded
        # if guarded, don't kill and announce that they survived the night because they were guarded
        # if not guarded, kill them and announce their death
        return;

    def WerewolfKill(self, player):
        if player not in self.Players:
            LogUtility.Error(f"Cannot kill {player.Name} as they are not in the game {self.Name}", self);
            return;

        player._Player__isAlive = False;
        LogUtility.CreateGameMessage(f"{player.Name} is killed by the werewolves.", self);

        return;

    #endregion

    #endregion

    #region Helpers

    def GetPlayerAndTimesVoted(self):
        votedPlayerIdentifiers = [vote.VotedPlayer.Identifier for vote in self.__votes];
        counter = Counter(votedPlayerIdentifiers);

        (mostVotedPlayerIdentifier, times) = counter.most_common(1)[0];

        player = self.GetPlayerByIdentifier(mostVotedPlayerIdentifier);

        return (player, times);

    def GetPlayerByIdentifier(self, playerIdentifier):
        return next((p for p in self.__players\
            if p.Identifier == playerIdentifier), None);

    def HasPlayerVotedAlready(self, playerIdentifier):
        return any(v for v in self.__votes \
            if v.Player.Identifier == playerIdentifier);

    #endregion
