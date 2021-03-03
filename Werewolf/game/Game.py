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
        self.__playersWhoCanActThisNight = set();

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
        return self.__players;

    @property
    def PlayerIdentifiers(self):
        return [p.Identifier for p in self.Players];

    @property
    def NightPlayers(self):
        return [p for p in self.Players if p.Role.HasNightAction];

    @property
    def NightPlayerIdentifiers(self):
        # don't reference self.NightPlayers, that's an extra list comprehension
        return [p.Identifier for p in self.Players if p.Role.HasNightAction];

    @property
    def TimeOfDay(self):
        return self.__timeOfDay;

    @property
    def HasAgentPlayers(self):
        return any(player for player in self.Players \
            if issubclass(type(player), AgentPlayer));

    @property
    def AgentPlayers(self):
        return [player for player in self.Players \
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

    def CheckWinCondition(self):
        # this will be defined in GameRules.py
        if GameRules.DoVillagersWin(self):
            LogUtility.CreateGameMessage("Villagers win!", self);
            self.Restart();
            return True;

        if GameRules.DoWerewolvesWin(self):
            LogUtility.CreateGameMessage("Werewolves win!", self);
            self.Restart();
            return True;

        return False;

    def StartDay(self):
        self.__votes = set();
        self.__timeOfDay = TimeOfDayEnum.Day;

        for agent in [ap for ap in self.AgentPlayers if ap.IsAlive]:
            agent.ActDay();

        return;

    def StartNight(self):
        self.__votes = set();
        self.__timeOfDay = TimeOfDayEnum.Night;

        self.__playersWhoCanActThisNight = set([np.Identifier for np in self.NightPlayers if np.IsAlive]);

        for agent in [ap for ap in self.AgentPlayers if ap.IsAlive]:
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
        alivePlayers = [ap for ap in self.Players if ap.IsAlive];
        playerIdentifiers = [p.Identifier for p in alivePlayers];

        if not vote.Player.Identifier in playerIdentifiers or\
            (vote.VotedPlayer and not vote.VotedPlayer.Identifier in playerIdentifiers):
            # players not in the game, error
            LogUtility.Error("Invalid vote, one of the players is not alive in the game", self);
            return;

        if not vote.VotedPlayer:
            LogUtility.CreateGameMessage(f"Player {vote.Player.Name} does not vote.", self);
        else:
            LogUtility.CreateGameMessage(f"Player {vote.Player.Name} voted to execute {vote.VotedPlayer.Name}.", self);

        self.Votes.add(vote);

        if len(self.Votes) == len(playerIdentifiers):
            self.CountVotesExecute();

        return;

    def CountVotesExecute(self):
        # remove the "wait" calls
        actualVotes = [v for v in self.Votes if v.VotedPlayer];

        (player, times) = self.GetPlayerAndTimesVoted(actualVotes);

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

        self.CheckWinCondition();
        return;

    #endregion

    #region Night

    def VoteNight(self, vote):
        playerIdentifiers = self.PlayerIdentifiers;

        if not vote.Player.Identifier in self.__playersWhoCanActThisNight:
            playerDetails = vote.Player.Name + " - " +  vote.Player.Identifier;
            LogUtility.Error(f"Player {playerDetails} cannot act in the night.", self);
            return;

        if vote.VotedPlayer and not vote.VotedPlayer.Identifier in playerIdentifiers:
            playerDetails = vote.VotedPlayer.Name + " - " +  vote.VotedPlayer.Identifier;
            LogUtility.Error(f"Invalid vote, target player {playerDetails} is not in the game", self);
            return;

        player = self.GetPlayerByIdentifier(vote.Player.Identifier);
        targetPlayer = self.GetPlayerByIdentifier(vote.VotedPlayer.Identifier);

        if vote.PlayerType == PlayerTypeEnum.Werewolf:
            self.Attack(player, targetPlayer);
        elif vote.PlayerType == PlayerTypeEnum.Seer:
            self.Divine(player, targetPlayer);
        elif vote.PlayerType == PlayerTypeEnum.Guard:
            self.Guard(player, targetPlayer);
        else:
            # I know this should semantically be before the actual addition of
            # the vote. However, we rely on the previous security checks
            LogUtility.Error(f"Player {player.Name} does not have a valid night role - {player.Role.Type}", self);
            return;

        self.Votes.add(vote);

        if len(self.Votes) == len(self.__playersWhoCanActThisNight):
            self.CountNightVotesAndEvents();
            self.__playersWhoCanActThisNight = set();

        return;

    def Attack(self, werewolf, player):
        if not player:
            LogUtility.Information(f"Werewolf {vote.Player.Name} waits.", self);

        LogUtility.Information(f"Werewolf {werewolf.Name} attacks {player.Name}.", self);
        return;

    def Guard(self, guard, player):
        if not player:
            LogUtility.Information(f"Guard {vote.Player.Name} waits.", self);

        guard.Role._Guard__canGuardTimes -= 1;
        LogUtility.Information(f"Guard {guard.Name} guards {player.Name}.", self);
        return;

    def Divine(self, seer, player):
        if not player:
            LogUtility.Information(f"Seer {vote.Player.Name} waits.", self);

        seer.Role._Seer__canDivineTimes -= 1;
        LogUtility.Information(f"Seer {seer.Name} divines {player.Name}.", self);
        return;

    def CountNightVotesAndEvents(self):
        # remove the "wait" calls
        actualVotes = [v for v in self.Votes if v.VotedPlayer];

        # actual votes
        votesToKill = [v for v in actualVotes if v.PlayerType == PlayerTypeEnum.Werewolf];

        (playerToKill, werewolfAttackTimes) = self.GetPlayerAndTimesVoted(votesToKill);

        # independent actions
        votesToGuard = [v for v in actualVotes if v.PlayerType == PlayerTypeEnum.Guard];
        votesToDivine = [v for v in actualVotes if v.PlayerType == PlayerTypeEnum.Seer];

        # we only want to make the fact known that someone was guarded if an attack on them
        # had occurred during the night. Otherwise it would advantage the werewolves.
        guardsForAttackedPlayer = [v.Player for v in votesToGuard \
            if playerToKill.Identifier == v.VotedPlayer.Identifier];

        if not guardsForAttackedPlayer:
            self.WerewolfKill(playerToKill);
        else:
            LogUtility.CreateGameMessage("Player " + playerToKill.Name +\
                " was attacked by werewolves in the night but was guarded and lives to see another day.", self);

        # Get votes for seer (these are independent from everything else)

        if not self.CheckWinCondition():
            self.__turn += 1;
            self.StartDay();

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

    def GetPlayerAndTimesVoted(self, votes):
        votedPlayerIdentifiers = [vote.VotedPlayer.Identifier for vote in votes];
        counter = Counter(votedPlayerIdentifiers);

        (mostVotedPlayerIdentifier, times) = counter.most_common(1)[0];

        player = self.GetPlayerByIdentifier(mostVotedPlayerIdentifier);

        return (player, times);

    def GetPlayerByIdentifier(self, playerIdentifier):
        return next((p for p in self.Players\
            if p.Identifier == playerIdentifier), None);

    def HasPlayerVotedAlready(self, playerIdentifier):
        return any(v for v in self.__votes \
            if v.Player.Identifier == playerIdentifier);

    #endregion
