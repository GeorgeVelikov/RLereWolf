# we might wand to handle only GameExceptions a bit neater than other ones
class GameException(Exception):
    def __init__(self, message):
        super().__init__(message);