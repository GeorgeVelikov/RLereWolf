class HandlerBase():
    def __init__(self, server, handlerContext):
        self.__server = server;
        self.__handlerContext = handlerContext;

    @property
    def Server(self):
        return self.__server;

    @property
    def HandlerContext(self):
        return self.__handlerContext;

    @property
    def Games(self):
        return self.__server.Games;
