import Shared.constants.NetConstants as NetConstants;

from datetime import datetime;

import dateutil.tz;

class Message():
    def __init__(self, author, text):
        self.__timestampUtc = datetime.utcnow();
        self.__author = author;
        self.__text = text;

    def __str__(self):
        return f"[{self.TimeStampLocal}] {self.AuthorName} says: {self.Text}";

    def __repr__(self):
        return str(self);

    @property
    def TimeStampUtc(self):
        return self.__timestampUtc\
            .strftime(NetConstants.DATETIME_FORMAT);

    @property
    def TimeStampLocal(self):
        return datetime.fromtimestamp(self.TimeStampUtc)\
            .strftime(NetConstants.DATETIME_FORMAT);

    @property
    def AuthorIdentifier(self):
        return self.__author.Identifier;

    @property
    def AuthorName(self):
        return self.__author.Name;

    @property
    def Text(self):
        return self.__text;
