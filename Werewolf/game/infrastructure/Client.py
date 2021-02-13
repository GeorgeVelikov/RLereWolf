import constants.NetConstants as NetConstants;
from game.Player import Player;
from game.infrastructure.Packet import Packet;
from models.dtos.ClientJoinGameDto import ClientJoinGameDto;
from utility.Helpers import ClearScreen, nameof;

from datetime import datetime;

import socket;
import pickle;
import threading;
import time;


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
        print("1. Connect to Server");
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
                    self.MenuGameList();
            elif option == 2:
                self.SetName(str(input("Name: ")));
                pass;

            else:
                print("[ERROR] Invalid option.");

        return;

    def MenuGameList(self):
        games = dict();
        option = None;

        while option != 0:
            games = self.GetGamesList();
            gameIndexToIdentifier = dict();
            ClearScreen();

            for index, (identifier, name) in enumerate(games.items()):
                gameIndexToIdentifier[index + 1] = identifier;
                print(f"{index + 1}. {name}");

            print("\n0. Quit\n");

            try:
                option = int(input("> "));
            except Exception as error:
                option = -1;

            if option == 0:
                self.Disconnect();
                self.MenuMain();

            if option > 0 and option <= len(games):
                gameIdentifier = gameIndexToIdentifier[option-1]
                self.JoinGame(gameIdentifier);
                self.MenuGameLobby();

            else:
                print("[ERROR] Invalid option.");

        return;

    def MenuGameLobby(self):
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

    def Send(self, data):
        try:
            # We send some data
            self.__connection.sendall(pickle.dumps(data));

            # We get some reply
            serializedReply = self.__connection.recv(4 * NetConstants.KILOBYTE);

            # this is some serialized object
            reply = pickle.loads(serializedReply);

            return reply;

            print(reply);
        except socket.error as error:
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

    def Disconnect(self):
        try:
            self.__connection.close();
            self.__gameIdentifier = None;
        except Exception as error:
            print("[ERROR] " + str(error));

        return;

    #endregion

    #region Calls

    def GetGamesList(self):
        packet = Packet.GetGamesPacket(list());

        reply = self.Send(packet);

        return reply;

    def JoinGame(self, gameIdentifier):
        dto = ClientJoinGameDto(self, gameIdentifier)
        packet = Packet.GetJoinGamePacket(dto);

        reply = self.Send(packet);

        self.__gameIdentifier = reply;

        return reply;

    #endregion

if __name__ == "__main__":
    Client().MenuMain();