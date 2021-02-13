import constants.NetConstants as NetConstants;

from game.Player import Player;
from utility.Helpers import ClearScreen, nameof;

from datetime import datetime;

import socket;
import pickle;

class Client(Player):
    def __init__(self):
        super().__init__();
        self.__connection = None;
        self.__lastUpdateUtc = None;

    def __getstate__(self):
        state = self.__dict__.copy();
        state["_" + type(self).__name__ + nameof(self.__connection)] = None;
        return state;

    # TODO: Do we need to do __setstate__ as well? Will I ever override Client/Player?

    #region UI

    def MenuMain(self):
        ClearScreen();
        print("1. Join Server");
        print("2. Set Name");
        print("\n0. Quit\n");

        option = None;

        while option != 0:
            try:
                option = int(input("> "));
            except Exception as error:
                option = -1;

            if option == 0:
                pass;

            elif option == 1:
                if (not self.Name or self.Name.isspace()):
                    print("[ERROR] Cannot connect until you have set your name.");
                else:
                    self.Connect();
                    self.Send("Hello server");
                    self.MenuGame();
            elif option == 2:
                self.SetName(str(input("Name: ")));
                pass;

            else:
                print("[ERROR] Invalid option.");

        return;

    def MenuGame(self):
        ClearScreen();
        print("1. Player List");
        print("\n0. Quit\n");

        option = None;

        while option != 0:
            try:
                option = int(input("> "));
            except Exception as error:
                option = -1;

            if option == 0:
                self.Disconnect();
                self.MenuMain();

            elif option == 1:
                pass;

            else:
                print("[ERROR] Invalid option.");

        return;

    #endregion

    #region Connection

    def Disconnect(self):
        try:
            self.__connection.close();
        except Exception as error:
            print("[ERROR] " + str(error));

        return;

    def Connect(self):
        try:
            self.__connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
            self.__connection.connect(NetConstants.ADDRESS);

            data = self.__connection.recv(4 * NetConstants.KILOBYTE).decode();

            return data;
        except Exception as error:
            print("[ERROR] " + str(error));

        return;

    def Send(self, data):
        try:
            # We send some data
            self.__connection.send(str.encode(data));

            # We get some reply
            serializedReply = self.__connection.recv(4 * NetConstants.BYTE);

            # this is some serialized object
            reply = pickle.loads(serializedReply);

            self.JoinGame(reply.Identifier);
            return data;
        except socket.error as error:
            print("[ERROR] " + str(error));

        return;

    #endregion

if __name__ == "__main__":
    Client().MenuMain();