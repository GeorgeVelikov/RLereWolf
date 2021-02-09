from enums.PlayerTypeEnum import PlayerTypeEnum;
from models.roles.RoleBase import RoleBase;

class Werewolf(RoleBase):
    def __init__(self, name):
        super().__init__(name);

    @property
    def Role(self):
        return PlayerTypeEnum.Werewolf;

    # specific to werewolves or roles that "know" their team members
    def Whisper(self, message):
        if (not isinstance(message, str)):
            raise TypeError("Message must be a string in order to Whisper.");
            return;

        message = message.strip();

        if (message.isspace()):
            return;

        # TODO: call server to whisper to team members something;
        print(self.Name + ": " + message);
        return;

    def Attack(self, player):
        if (not isinstance(player, RoleBase)):
            # TODO: not a very good "friendly" message
            raise TypeError("Player must be inherited from RoleBase in order to Attack.");
            return;

        if (self == player):
            # TODO: not a very good "friendly" message, this probably needs to be handled elsewhere?
            raise ValueError("Werewolf cannot attack themselves.");
            return;

        # TODO: call server to attack/vote. Werewolves must agree on who to attack.
        print(self.Name + " votes to attack " + player.Name);
        return;