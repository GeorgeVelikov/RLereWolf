import constants.NetConstants as NetConstants;

from game.Player import Player;
from utility.Helpers import ClearScreen;

import socket;
import pickle;

class Client(Player):
    def __init__(self):
        super().__init__();
        self.__connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

    #region UI

    def Menu(self):
        ClearScreen();
        print("1. Join Server");
        print("2. Set Name");
        print("\n0. Quit\n");

        option = None;

        while option != 0:
            option = int(input("> "));

            if option == 0:
                pass;

            elif option == 1:
                if (not self.Name or self.Name.isspace()):
                    print("[ERROR] Cannot connect until you have set your name.");
                else:
                    self.Connect();
            elif option == 2:
                self.SetName(str(input("Name: ")));
                pass;

            else:
                print("[ERROR] Invalid option.");

        return;

    #endregion

    #region Connection

    def Connect(self):
        try:
            self.__connection.connect(NetConstants.ADDRESS)

            data = self.__connection\
                .recv(2 * NetConstants.BYTE)\
                .decode();

            return data;
        except Exception as error:
            print("[ERROR] " + str(error));

        return;

    def Send(self, data):
        try:
            self.__connection.send(str.encode(data));

            data = pickle.loads(self__connection.recv(4 * NetConstants.BYTE))

            return data;
        except socket.error as error:
            print("[ERROR] " + str(error));

        return;

    #endregion

if __name__ == "__main__":
    Client().Menu();