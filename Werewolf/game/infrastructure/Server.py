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

    def __RegisterRoutes(self):
        @self.__flask.route(NetConstants.ROOT)
        @self.__flask.route(NetConstants.INDEX)
        def Home():
            return str(self.Games);

        @self.__flask.route(NetConstants.GAME_CREATE)
        def CreateGame(name):
            self.CreateGame(name);
            return redirect(NetConstants.ROOT);

        return;
