import constants.NetConstants as NetConstants;

from game.Player import Player;

import socket;
import pickle;

class Client(Player):
    def __init__(self, name):
        super().__init__(name);
        self.__connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

    def Connect(self):
        try:
            self.__connection.connect(NetConstants.ADDRESS)
            return self.__connection\
                .recv(2 * NetConstants.BYTE)\
                .decode();
        except:
            pass

        return;

    def Send(self, data):
        try:
            self.__connection.send(str.encode(data))
            return pickle.loads(self.client.recv(4 * NetConstants.BYTE))
        except socket.error as error:
            # Better print
            print(error)

        return;