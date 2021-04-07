from Shared.utility.Helpers import nameof;

class Statistics():
    def __init__(self):
        self.DeadAgentVoted = int();
        self.DeadAgentAttacked = int();
        self.TeammateAttacked = int();
        self.IncorrectAction = int();
        self.WerewolfWins = int();
        self.VillagerWins = int();
        self.TotalDays = int();
        self.TotalGames = int();

    def __str__(self):
        statistics = \
            "\nDead Agents Voted:"+ str(self.DeadAgentVoted) +\
            "\nDead Agents Attacked:"+ str(self.DeadAgentAttacked) +\
            "\nTeammates Attacked:"+ str(self.TeammateAttacked) +\
            "\nIncorrect Actions:"+ str(self.IncorrectAction) +\
            "\nWerewolf Wins:"+ str(self.WerewolfWins) +\
            "\nVillager Wins:"+ str(self.VillagerWins) +\
            "\nTotal Days:"+ str(self.TotalDays) +\
            "\nTotal Games:"+ str(self.TotalGames);

        return statistics;
