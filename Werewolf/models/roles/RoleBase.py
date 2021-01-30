from abc import abstractmethod;

from enums.PlayerTypeEnum import PlayerTypeEnum;

class RoleBase():
    def __init__(self, name):
        if (not isinstance(name, str)):
            raise TypeError("Name must be a string in order to create a player.");
            return;

        self.__name = name.strip();
        return;

    @property
    def Name(self):
        return self.__name;

    @property
    def Role(self):
        return PlayerTypeEnum._None;

    def Talk(self, message):
        if (not isinstance(message, str)):
            raise TypeError("Message must be a string in order to Talk.");
            return;

        message = message.strip();

        if (message.isspace()):
            return;

        # TODO: call server to say something;
        print(self.Name + ": " + message);
        return;

    def Vote(self, player):
        if (not isinstance(player, RoleBase)):
            # TODO: not a very good "friendly" message
            raise TypeError("Player must be inherited from RoleBase in order to Vote.");
            return;

        if (self == player):
            # TODO: not a very good "friendly" message, this probably needs to be handled elsewhere?
            raise ValueError("Player cannot vote for themselves.");
            return;

        # TODO: call server to vote
        print(self.Name + " votes to kill " + player.Name);
        return;