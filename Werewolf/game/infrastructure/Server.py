import constants.NetConstants as NetConstants;
import constants.GameConstants as GameConstants;

from game.Game import Game;

from _thread import start_new_thread;
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

    def ConnectClient(self, connection, gameIdentifier):
        print("Connected to server.");

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
                print(error);
                break;

        print("Lost connection to server.");

        connection.close();
        return;

    def Run(self):
        try:
            self.__connection.bind(NetConstants.ADDRESS);
            self.__connection.listen(GameConstants.MAXIMUM_PLAYER_COUNT);
            print("Server successfully started at port " + str(NetConstants.PORT));
        except socket.error as error:
            print(error);

        while True:
            connection, address = self.__connection.accept();
            gameIdentifier = None;
            start_new_thread(self.ConnectClient, (connection, gameIdentifier));

        return;

    def CreateGame(self, name):
        game = Game(name);
        self.__games.append(game);
        return;

if __name__ == "__main__":
    Server().Run();
