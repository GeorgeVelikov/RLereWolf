import constants.NetConstants as NetConstants;
import constants.GameConstants as GameConstants;

from game.Game import Game;

from datetime import datetime;

import threading;
import socket;
import pickle;
import sys;

class Server():
    def __init__(self):
        self.__connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        self.__games = list();
        self.CreateGame("Game");
        return;

    @property
    def Games(self):
        return self.__games;

    @property
    def UtcNow(self):
        return datetime.utcnow();

    @property
    def UtcNowString(self):
        return self.UtcNow.strftime(NetConstants.DATETIME_FORMAT);

    def ShowActiveConnections(self):
        print(f"{self.UtcNowString} [STATUS] Active connections - {threading.activeCount() - 1}");

    def ClientHandle(self, connection, address):
        connection.send(b"Hello client");
        print(f"{self.UtcNowString} [STATUS] Connected to server - {address}.");
        self.ShowActiveConnections();

        while True:
            try:
                data = connection\
                    .recv(4 * NetConstants.KILOBYTE)\
                    .decode();

                if not data:
                    break;

                print(data);

                # TODO: grab the game instance from a game identifier param
                #game = next(game for game in self.__games \
                #    if game.Identifier == gameIdentifier);

                #if not game:
                #   break;

                # Do game calls in here!

                # Give users the game state back
                game = self.__games[0];
                connection.sendall(pickle.dumps(game));
            except Exception as error:
                print("{self.UtcNowString} [ERROR] " + str(error));
                break;


        print(f"{self.UtcNowString} [STATUS] Lost connection to server - {address}.");
        connection.close();

        return;

    def Run(self):
        try:
            self.__connection.bind(NetConstants.ADDRESS);
            self.__connection.listen();
            print(f"{self.UtcNowString} [STATUS] Server successfully started at {NetConstants.IP}:{NetConstants.PORT}");
            self.ShowActiveConnections();
        except socket.error as error:
            print("{self.UtcNowString} [ERROR] " + str(error));

        while True:
            connection, address = self.__connection.accept();
            threading.Thread(target = self.ClientHandle, args = (connection, address)).start();
        return;

    def CreateGame(self, name):
        game = Game(name);
        self.__games.append(game);
        return;

if __name__ == "__main__":
    Server().Run();
