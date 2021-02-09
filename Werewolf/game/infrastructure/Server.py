from flask import Flask, redirect;

import constants.NetConstants as NetConstants;

from game.Game import Game;

class Server():
    def __init__(self):
        self.__games = list();
        self.__flask = Flask("Werewolf server");
        self.__RegisterRoutes();
        return;

    @property
    def Games(self):
        return self.__games;

    def Run(self):
        try:
            self.__flask.run(NetConstants.IP, NetConstants.PORT);
            print("Server successfully started at port " + str(NetConstants.PORT));
        except:
            raise;

    def CreateGame(self, name):
        game = Game(name);
        self.__games.append(game);
        return;

    def JoinGame(self, gameIdentifier):
        gameToJoin = next(game for game in self.__games \
            if game.Identifier == gameIdentifier);

        if not gameToJoin:
            return False;

        return True;

    def __RegisterRoutes(self):
        @self.__flask.route(NetConstants.ROUTE_ROOT)
        @self.__flask.route(NetConstants.ROUTE_INDEX)
        def Home():
            return str(self.Games);

        @self.__flask.route(NetConstants.ROUTE_GAME_CREATE)
        def CreateGame(name):
            self.CreateGame(name);
            return redirect(NetConstants.ROUTE_ROOT);

        @self.__flask.route(NetConstants.ROUTE_GAME_JOIN)
        def JoinGame(name):
            self.JoinGame(name);
            return redirect(NetConstants.ROUTE_ROOT);

        return;
