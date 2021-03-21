import Shared.constants.NetConstants as NetConstants;
import Shared.utility.DateTimeUtility as DateTimeUtility

from datetime import datetime;

class MessageDto():
    def __init__(self,\
        author,\
        text,\
        forPlayer = None,\
        forRole = None,\
        messageMetaData = None):

        self.__timeUtc = datetime.utcnow();
        self.__author = author;
        self.__text = text;
        self.__isHumanAuthor = True if author else False;

        # this can be a whisper, similar sort of "message the team" functionality
        self.__forRole = forRole;

        # only specify this is if it's a "private" message
        self.__forPlayer = forPlayer;

        # a better way of keeping track of the message type, message type, message target etc.
        self.__messageMetaData = messageMetaData;

    def __str__(self):
        return self.TimeStampLocal + " " + self.Content;

    def __repr__(self):
        return str(self);

    @property
    def Author(self):
        if self.__isHumanAuthor:
            return self.__author;

        return "[SERVER]";

    # Used by the server to filter out messages
    # when delivering to the client
    @property
    def TimeUtc(self):
        return self.__timeUtc;

    @property
    def ForRole(self):
        return self.__forRole;

    @property
    def ForPlayer(self):
        return self.__forPlayer;

    @property
    def TimeStampUtc(self):
        return self.__timeUtc\
            .strftime(NetConstants.DATETIME_FORMAT);

    @property
    def TimeStampLocal(self):
        return DateTimeUtility.UtcToLocal(self.__timeUtc)\
            .strftime(NetConstants.TIME_FORMAT);

    @property
    def AuthorIdentifier(self):
        if not self.__isHumanAuthor:
            return self.Author;

        return self.__author.Identifier;

    @property
    def AuthorName(self):
        if not self.__isHumanAuthor:
            return self.Author;

        return self.__author.Name;

    @property
    def Text(self):
        return self.__text;

    @property
    def Content(self):
        return \
            ("[PRIVATE] " if self.ForPlayer else str()) +\
            ("[WHISPER] " if self.ForRole else str()) +\
            self.AuthorName + " " + ("says: " if self.__isHumanAuthor else str()) +\
            self.Text;

    @property
    def MetaData(self):
        return self.__messageMetaData;
