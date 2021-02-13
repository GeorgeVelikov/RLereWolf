import constants.NetConstants as NetConstants;
import constants.GameConstants as GameConstants;

from game.Game import Game;

import threading;
import socket;
import pickle;
import sys;

class Server():
    def __init__(self):
        self.__connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        self.__games = list();
        return;

    @property
    def Games(self):
        return self.__games;

    def ClientHandle(self, connection, address):
        print(f"[STATUS] Connected to server - {address}.");

        while True:
            try:
                data = connection\
                    .recv(4 * NetConstants.BYTE)\
                    .decode();

                if not data:
                    break;

                # TODO: grab the game instance from a game identifier param
                #game = next(game for game in self.__games \
                #    if game.Identifier == gameIdentifier);

                #if not game:
                #   break;

                # Do game calls in here!

                # Give users the game state back
                connection.sendall(pickle.dumps(game));
            except Exception as error:
                print("[ERROR] " + str(error));
                break;

        print(f"[STATUS] Lost connection to server - {address}.");

        connection.close();
        return;

    def Run(self):
        try:
            self.__connection.bind(NetConstants.ADDRESS);
            self.__connection.listen();
            print(f"[STATUS] Server successfully started at {NetConstants.IP}:{NetConstants.PORT}");
            print(f"[STATUS] Active connections - {threading.activeCount() - 1}");
        except socket.error as error:
            print("[ERROR] " + str(error));

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
