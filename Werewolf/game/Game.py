from Shared.enums.TimeOfDayEnum import TimeOfDayEnum;
from Shared.enums.TurnPhaseTypeEnum import TurnPhaseTypeEnum;
from Shared.exceptions.GameException import GameException;

import Shared.constants.GameConstants as GameConstant;

from Werewolf.roles.Villager import Villager;
from Werewolf.roles.Seer import Seer;
from Werewolf.roles.Guard import Guard;
from Werewolf.roles.Werewolf import Werewolf;

import hashlib;
import uuid;

class Game():
    def __init__(self, name):
        self.__identifier = uuid.uuid4().hex;
        self.__hasStarted = False;
        self.__name = name;
        self.__messages = set();
        self.__turnVotes = dict();
        self.__turn = int();
        self.__players = set();
        self.__timeOfDay = TimeOfDayEnum._None;
        self.__turnPhase = TurnPhaseTypeEnum._None;

    def __str__(self):
        return self.__name + " - " + self.Identifier;

    def __repr__(self):
        return self.__name + " - " + self.Identifier;

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
    def TurnVotes(self):
        return self.__turnVotes;

    @property
    def Turn(self):
        return self.__turn;

    @property
    def Players(self):
        return sorted(self.__players,\
            key = lambda p: p.Name, \
            reverse = False);

    @property
    def PlayerIdentifiers(self):
        return [p.Identifier for p in self.__players];

    @property
    def TimeOfDay(self):
        return self.__timeOfDay;

    @property
    def TurnPhase(self):
        return self.__turnPhase;

    #endregion

    #region Game calls

    def Join(self, player):
        self.__players.add(player);
        return;

    def Leave(self, player):
        if (player.Identifier not in self.PlayerIdentifiers):
            print(f"[ERROR] Player {player.Identifier} is not in the game.");
            # TODO: raise some silent exception
            return;

        # no need to sort, already alphabetical
        self.__players\
            .remove(self.GetPlayerByIdentifier(player.Identifier));

    def Start(self):
        if (len(self.__players) < GameConstant.MINIMAL_PLAYER_COUNT):
            print(f"[ERROR] Cannot start game without having at least {GameConstant.MINIMAL_PLAYER_COUNT} players.");
            return;

        for player in self.__players:
            player._Player__isReady = False;

        self.__startVotes = dict();
        self.__hasStrated = True;
        self.__turn = 1;
        self.__timeOfDay == TimeOfDayEnum.Day;
        self.__turnPhase = TurnPhaseTypeEnum.Introduction;
        return;

    def Restart(self):
        for player in self.__players:
            player._Player__isReady = False;
            player._Player__role = None;

        self.__hasStarted = False;
        self.__turnVotes = dict();
        self.__startVotes = set();
        self.__turn = int();
        self.__timeOfDay = TimeOfDayEnum._None;
        self.__turnPhase = TurnPhaseTypeEnum._None;

    def NextPhase(self):
        self.__turnPhase.Next();
        return;

    def NextPlayerTurn(self):
        return;

    def VoteStart(self, player):
        if not player:
            return;

        player._Player__isReady = not player._Player__isReady;

        isThereAnyNonReadyPlayers = next((p for p in self.__players if not p.IsReady), None);

        if isThereAnyNonReadyPlayers:
            return;

        self.Start();

        return;

    #endregion

    #region Helpers

    def GetPlayerByIdentifier(self, playerIdentifier):
        return next(p for p in self.__players\
            if p.Identifier == playerIdentifier);

    #endregion
