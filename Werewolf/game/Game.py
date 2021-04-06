import Shared.constants.GameConstants as GameConstants;
import Shared.utility.LogUtility as LogUtility;
from Shared.enums.TimeOfDayEnum import TimeOfDayEnum;
from Shared.enums.PlayerTypeEnum import PlayerTypeEnum;
from Shared.enums.FactionTypeEnum import FactionTypeEnum;
from Shared.enums.VoteResultTypeEnum import VoteResultTypeEnum;
from Shared.exceptions.GameException import GameException;

from Werewolf.agents.AgentPlayer import AgentPlayer;
import Werewolf.game.GameRules as GameRules;

import uuid;
import random;
from collections import Counter;

class Game():
    def __init__(self, name, agentsAutomaticallyPlay = True):
        self.__identifier = uuid.uuid4().hex;
        self.__hasStarted = False;
        self.__name = name;
        self.__messages = set();
        self.__votes = set();
        self.__turn = int();
        self.__players = set();
        self.__playerIdentifiersThatCanVote = set();
        self.__timeOfDay = TimeOfDayEnum._None;

        self.__agentsAutomaticallyPlay = agentsAutomaticallyPlay;

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
        return [p for p in self.Players if (p.Role and p.Role.HasNightAction)];

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

    @property
    def IsFull(self):
        return len(self.Players) >= GameConstants.MAXIMUM_PLAYER_COUNT;

    #endregion

    #region Game calls

    def Join(self, player):
        if self.IsFull:
            # can't really be hit by normal users, this can only get hit by trying to add agents
            LogUtility.Warning(f"'{player.Name}' cannot join the game, the game is full!", self);
            return;

        # TODO: This is kind of nasty and we should probably have a server player
        # and a game instance player entity, but this will do as a first pass. This
        # implies that the server is a "common world" instead of having a meta-player identity
        player._Player__isReady = False;
        self.__players.add(player);
        LogUtility.CreateGameMessage(f"'{player.Name}' has joined.", self);
        return;

    def Leave(self, player):
        if (player.Identifier not in self.PlayerIdentifiers):
            LogUtility.Error(f"'{player.Name}' is not in the game.", self);
            # TODO: raise some silent exception
            return;

        playerToLeave = self.GetPlayerByIdentifier(player.Identifier);
        self.__players.remove(playerToLeave);
        playerToLeave._Player__role = None;

        if playerToLeave.Identifier in self.__playerIdentifiersThatCanVote:
            self.__playerIdentifiersThatCanVote.remove(playerToLeave.Identifier);

        self.__votes = set([v for v in self.__votes\
            if v.Player != playerToLeave and v.VotedPlayer != playerToLeave]);

        LogUtility.CreateGameMessage(f"'{playerToLeave.Name}' has left.", self);

        gameIsOver, winningFaction = self.CheckWinCondition();

        if not gameIsOver and not self.__playerIdentifiersThatCanVote:
            if self.__timeOfDay == TimeOfDayEnum.Day:
                self.CountVotesExecute();
            elif self.__timeOfDay == TimeOfDayEnum.Night:
                self.CountNightVotesAndEvents();

            return;

        self.Restart();
        return;

    def Start(self):
        if (len(self.__players) < GameConstants.MINIMAL_PLAYER_COUNT):
            LogUtility.Error(
                f"Cannot start game without having at least {GameConstants.MINIMAL_PLAYER_COUNT} players.", self);
            return;

        for player in self.__players:
            player._Player__isAlive = True;
            player._Player__isReady = False;

        GameRules.DistributeRolesBaseGame(self);

        self.__hasStarted = True;
        self.__turn = 0;

        self.StartDay();

        return;

    def Restart(self):
        LogUtility.CreateGameMessage("Restarting game lobby", self);

        for player in self.__players:
            player._Player__isAlive = True;
            player._Player__isReady = False;
            player._Player__role = None;

        for agent in self.AgentPlayers:
            agent._Player__isReady = True;

        self.__hasStarted = False;
        self.__votes = set();
        self.__turn = int();
        self.__timeOfDay = TimeOfDayEnum._None;

    def CheckWinCondition(self):
        if not self.HasStarted:
            return (False, FactionTypeEnum._None);

        if len(self.Players) < GameConstants.MINIMAL_PLAYER_COUNT:
            LogUtility.CreateGameMessage(f"Minimum of {GameConstants.MINIMAL_PLAYER_COUNT} players required.", self);
            return (True, FactionTypeEnum._None);

        # this will be defined in GameRules.py
        if GameRules.DoVillagersWin(self):
            return (True, FactionTypeEnum.Villagers);

        if GameRules.DoWerewolvesWin(self):
            return (True, FactionTypeEnum.Werewolves);

        return (False, FactionTypeEnum._None);

    def StartDay(self):
        self.__turn += 1;
        self.__votes = set();
        self.__timeOfDay = TimeOfDayEnum.Day;
        self.ShowTurnAndTime();

        self.__playerIdentifiersThatCanVote = set([p.Identifier for p in self.Players if p.IsAlive]);

        if self.__agentsAutomaticallyPlay:
            agentPlayers = self.AgentPlayers
            shuffledAgentPLayers = random.sample(agentPlayers, len(agentPlayers));
            for agent in [ap for ap in shuffledAgentPLayers if ap.IsAlive]:
                vote = agent.ActDay();

                if not vote:
                    continue;

                self.Vote(vote);

        return;

    def StartNight(self):
        self.__votes = set();
        self.__timeOfDay = TimeOfDayEnum.Night;
        self.ShowTurnAndTime();

        self.__playerIdentifiersThatCanVote = set([p.Identifier for p in self.NightPlayers if p.IsAlive]);

        if self.__agentsAutomaticallyPlay:
            agentPlayers = self.AgentPlayers
            shuffledAgentPLayers = random.sample(agentPlayers, len(agentPlayers));
            for agent in [ap for ap in shuffledAgentPLayers if ap.IsAlive]:
                vote = agent.ActNight();

                if not vote:
                    continue;

                self.Vote(vote);

        return;

    def ShowTurnAndTime(self):
        capitalGameTime = str(self.TimeOfDay).capitalize();
        LogUtility.CreateGameMessage(f"\n\n\n\t\tTurn: {self.Turn}\t\tTime: {capitalGameTime}\n\n", self);
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

        if not vote.Player.Identifier in self.__playerIdentifiersThatCanVote:
            LogUtility.Error(f"Invalid vote, player {vote.Player.Name} cannot vote.", self);
            return VoteResultTypeEnum.InvalidAction;

        if vote.VotedPlayer and not vote.VotedPlayer.Identifier in playerIdentifiers:
            # players not in the game, error
            LogUtility.Error(f"Invalid vote, target player {vote.VotedPlayer.Name} is not alive", self);
            return VoteResultTypeEnum.DeadPlayerTargeted;

        if not vote.VotedPlayer:
            LogUtility.CreateGameMessage(f"'{vote.Player.Name}' does not vote.", self);
            return VoteResultTypeEnum.WaitAction;
        else:
            LogUtility.CreateGameMessage(f"'{vote.Player.Name}' voted to execute {vote.VotedPlayer.Name}.", self);

        self.Votes.add(vote);
        self.__playerIdentifiersThatCanVote.remove(vote.Player.Identifier);

        if not self.__playerIdentifiersThatCanVote:
            self.CountVotesExecute();

        return VoteResultTypeEnum.SuccessfulAction;

    def CountVotesExecute(self):
        # remove the "wait" calls
        actualVotes = [v for v in self.Votes if v.VotedPlayer];

        (player, times) = self.GetPlayerAndTimesVoted(actualVotes);

        if not player or not times:
            LogUtility.CreateGameMessage(f"No one gets executed during the day.", self);
        else:
            LogUtility.CreateGameMessage(f"{player.Name} has the most votes to get executed - {times}.", self);

            self.Execute(player);

        gameIsOver, winningFaction = self.CheckWinCondition();

        if gameIsOver:
            # don't go to other turn and don't start the day if the game is over
            self.Restart();
            return;

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

        if not vote.Player.Identifier in self.__playerIdentifiersThatCanVote:
            playerDetails = "'" + vote.Player.Name + "' - " +  vote.Player.Identifier;
            LogUtility.Error(f"{playerDetails} cannot act in the night.", self);
            return VoteResultTypeEnum.InvalidAction;

        if vote.VotedPlayer and not vote.VotedPlayer.Identifier in playerIdentifiers:
            playerDetails = vote.VotedPlayer.Name + " - " +  vote.VotedPlayer.Identifier;
            LogUtility.Error(f"Invalid vote, target player {playerDetails} is not in the game", self);
            return VoteResultTypeEnum.DeadPlayerTargeted;

        player = self.GetPlayerByIdentifier(vote.Player.Identifier);
        targetPlayer = self.GetPlayerByIdentifier(vote.VotedPlayer.Identifier) if vote.VotedPlayer else None;

        voteResult = VoteResultTypeEnum.WaitAction;

        if vote.PlayerType == PlayerTypeEnum.Werewolf:
            voteResult = self.Attack(player, targetPlayer);
        elif vote.PlayerType == PlayerTypeEnum.Seer:
            voteResult = self.Divine(player, targetPlayer);
        elif vote.PlayerType == PlayerTypeEnum.Guard:
            voteResult = self.Guard(player, targetPlayer);
        else:
            # I know this should semantically be before the actual addition of
            # the vote. However, we rely on the previous security checks
            LogUtility.Error(f"'{player.Name}' does not have a valid night role - {player.Role.Type}", self);
            return VoteResultTypeEnum.CannotActDuringTimeOfDay;

        self.Votes.add(vote);
        self.__playerIdentifiersThatCanVote.remove(player.Identifier);

        if not self.__playerIdentifiersThatCanVote:
            self.CountNightVotesAndEvents();

        return voteResult;

    def Attack(self, werewolf, player):
        if not player:
            # Should werewolves be able to wait? Is this even an actual use case?
            LogUtility.Information(f"Werewolf '{werewolf.Name}' waits.", self);
            return VoteResultTypeEnum.WaitAction;

        LogUtility.Information(f"Werewolf '{werewolf.Name}' attacks '{player.Name}'.", self);

        if player.Role.Type == PlayerTypeEnum.Werewolf:
            return VoteResultTypeEnum.WerewolfCannibalism;

        return VoteResultTypeEnum.SuccessfulAction;

    def Guard(self, guard, player):
        if not player:
            LogUtility.Information(f"Guard '{guard.Name}' waits.", self);
            return VoteResultTypeEnum.WaitAction;

        guard.Role._Guard__canGuardTimes -= 1;
        LogUtility.Information(f"Guard '{guard.Name}' guards '{player.Name}'.", self);
        return VoteResultTypeEnum.SuccessfulAction;

    def Divine(self, seer, player):
        if not player:
            LogUtility.Information(f"Seer '{seer.Name}' waits.", self);
            return VoteResultTypeEnum.WaitAction;

        LogUtility.Information(f"Seer '{seer.Name}' divines '{player.Name}'.", self);
        return VoteResultTypeEnum.SuccessfulAction;

    def CountNightVotesAndEvents(self):
        # remove the "wait" calls
        actualVotes = [v for v in self.Votes if v.VotedPlayer];

        # actual votes
        votesToKill = [v for v in actualVotes if v.PlayerType == PlayerTypeEnum.Werewolf];

        # independent actions
        votesToGuard = [v for v in actualVotes if v.PlayerType == PlayerTypeEnum.Guard];
        votesToDivine = [v for v in actualVotes if v.PlayerType == PlayerTypeEnum.Seer];

        (playerToKill, werewolfAttackTimes) = self.GetPlayerAndTimesVoted(votesToKill);

        if not playerToKill or not werewolfAttackTimes:
            LogUtility.CreateGameMessage(f"No one gets attacked during the night.", self);
        else:
            # we only want to make the fact known that someone was guarded if an attack on them
            # had occurred during the night. Otherwise it would advantage the werewolves.
            guardsForAttackedPlayer = [v.Player for v in votesToGuard \
                if playerToKill.Identifier == v.VotedPlayer.Identifier];

            if not guardsForAttackedPlayer:
                self.WerewolfKill(playerToKill);
            else:
                LogUtility.CreateGameMessage("'" + playerToKill.Name +\
                    "' was attacked by werewolves in the night but was guarded and lives to see another day.", self);

        for vote in votesToDivine:
            divinedPlayer = vote.VotedPlayer;
            isDivinedPlayerWereolf = divinedPlayer.Role.Type == PlayerTypeEnum.Werewolf;
            negator = str() if isDivinedPlayerWereolf else "NOT";

            message = f"'{divinedPlayer.Name}' was divined, they are {negator} a werewolf.";
            LogUtility.CreatePrivateGameMessage(message, self, vote.Player.Identifier);

            pass;

        # Get votes for seer (these are independent from everything else)

        gameIsOver, winningFaction = self.CheckWinCondition();

        if gameIsOver:
            # don't go to other turn and don't start the day if the game is over
            self.Restart();
            return;

        self.StartDay();

        return;

    def WerewolfKill(self, player):
        if player not in self.Players:
            LogUtility.Error(f"Cannot kill '{player.Name}' as they are not in the game '{self.Name}'", self);
            return;

        player._Player__isAlive = False;
        LogUtility.CreateGameMessage(f"'{player.Name}' is killed by the werewolves.", self);

        return;

    #endregion

    #endregion

    #region Helpers

    def GetPlayerAndTimesVoted(self, votes):
        votedPlayerIdentifiers = [vote.VotedPlayer.Identifier for vote in votes];
        counter = Counter(votedPlayerIdentifiers);

        mostCommon = counter.most_common(1);

        if not mostCommon:
            return (None, None);

        (mostVotedPlayerIdentifier, times) = mostCommon[0];

        player = self.GetPlayerByIdentifier(mostVotedPlayerIdentifier);

        return (player, times);

    def GetPlayerByIdentifier(self, playerIdentifier):
        return next((p for p in self.Players\
            if p.Identifier == playerIdentifier), None);

    def HasPlayerVotedAlready(self, playerIdentifier):
        return any(v for v in self.__votes \
            if v.Player.Identifier == playerIdentifier);

    #endregion
