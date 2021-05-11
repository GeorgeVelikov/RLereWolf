from Shared.utility.Helpers import nameof;

class Statistics():
    def __init__(self):
        self.NumberOfPlayers = int();
        self.DeadAgentVoted = int();
        self.DeadAgentAttacked = int();
        self.TeammateAttacked = int();
        self.IncorrectAction = int();
        self.WerewolfWins = int();
        self.VillagerWins = int();
        self.TotalTurns = int();
        self.TotalDays = int();
        self.TotalGames = int();
        self.GameTimeSeconds = int();

    def __str__(self):
        statistics = \
            "\nNumber Of Players:" + str(self.NumberOfPlayers) +\
            "\nDead Agents Voted:" + str(self.DeadAgentVoted) +\
            "\nDead Agents Attacked:" + str(self.DeadAgentAttacked) +\
            "\nTeammates Attacked:" + str(self.TeammateAttacked) +\
            "\nIncorrect Actions:" + str(self.IncorrectAction) +\
            "\nWerewolf Wins:" + str(self.WerewolfWins) +\
            "\nVillager Wins:" + str(self.VillagerWins) +\
            "\nTotal Turns:" + str(self.TotalTurns) +\
            "\nTotal Days:" + str(self.TotalDays) +\
            "\nTotal Games:" + str(self.TotalGames) +\
            "\nGame Time (seconds):" + str(self.GameTimeSeconds);

        return statistics;
