import Shared.constants.GameConstants as GameConstants;
import Shared.constants.NetConstants as NetConstants;

from Shared.dtos.ClientGameDto import ClientGameDto;
from Shared.dtos.GamePlayerListDto import GamePlayerListDto;

from Shared.Packet import Packet;

from Shared.utility.Helpers import nameof;

from Werewolf.game.Player import Player;

import Client.constants.ClientConstants as ClientConstants;
import Client.utility.UIContext as UIContext;
from Client.utility.Helpers import ClearScreen, PromptOption;

from datetime import datetime;

import socket;
import pickle;
import threading;
import time;
import pygame;

class ClientInstance(Player):
    def __init__(self):
        super().__init__();
        self.__connection = None;
        self.__lastUpdateUtc = None;
        self.__screen = None;
        self.__clock = None;

    def __getstate__(self):
        state = self.__dict__.copy();
        state["_" + type(self).__name__ + nameof(self.__connection)] = None;
        state["_" + type(self).__name__ + nameof(self.__screen)] = None;
        state["_" + type(self).__name__ + nameof(self.__clock)] = None;
        return state;

    # TODO: Do we need to do __setstate__ as well? Will I ever override Client/Player?

    #region UI

    def Load(self):
        self.__screen = pygame.display.set_mode([ClientConstants.WIDTH, ClientConstants.HEIGHT])
        self.__clock = pygame.time.Clock();
        self.Main();

    def Main(self):

        clientIsRunning = True;

        while True:
            clicked = False;
            self.__screen.fill((255, 255, 255));

            mouseCoordiantes = UIContext.GetMousePosition();

            label = UIContext.Label(self.__screen, "Hello", 50, 50);

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    clientIsRunning = False;
                    self.Disconnect();
                    pygame.display.quit();
                    pygame.quit();
                    exit();

                if event.type == pygame.MOUSEBUTTONDOWN:
                    clicked = True;


            if clicked and label.collidepoint(mouseCoordiantes):
                print("XD");

            pygame.display.update();
            self.__clock.tick(ClientConstants.FRAME_RATE);

        return;

    def MenuMain(self):
        ClearScreen();
        print("1. Connect to Server");
        print("2. Set Name");
        print("\n0. Quit\n");

        option = None;

        while option != 0:
            option = PromptOption();

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

            option = PromptOption();

            if option == 0:
                self.Disconnect();
                self.MenuMain();

            if option > 0 and option <= len(games):
                gameIdentifier = gameIndexToIdentifier[option]
                self.JoinGame(gameIdentifier);
                self.MenuGameLobby();

            else:
                print("[ERROR] Invalid option.");

        return;

    def MenuGameLobby(self):
        players = dict();
        option = -1;

        while option != 0:
            playerIndexToIdentifier = dict();
            players = self.GetPlayerList();
            ClearScreen();
            print("1. Placeholder");
            print("\n0. Quit\n");

            print("Players:");
            for index, (identifier, name) in enumerate(players.items()):
                playerIndexToIdentifier[index + 1] = identifier;
                print(f"\t- {name}");

            option = PromptOption();

            if option == 0:
                self.LeaveGame();
                self.MenuGameList();

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
        if not self.__connection:
            return;

        try:
            self.__connection.close();
            self.__gameIdentifier = None;
        except Exception as error:
            print("[ERROR] " + str(error));

        return;

    #endregion

    #region Calls

    def GetGamesList(self):
        packet = Packet.GetGamesPacket();

        reply = self.Send(packet);

        return reply;

    def LeaveGame(self):
        if not self.__gameIdentifier:
            return;

        dto = ClientGameDto(self, self.__gameIdentifier);
        packet = Packet.GetLeaveGamePacket(dto)

        reply = self.Send(packet);

        if reply:
            self.__gameIdentifier = None;

        return reply;


    def JoinGame(self, gameIdentifier):
        dto = ClientGameDto(self, gameIdentifier)
        packet = Packet.GetJoinGamePacket(dto);

        reply = self.Send(packet);

        self.__gameIdentifier = reply;

        return reply;

    def GetPlayerList(self):
        if not self.__gameIdentifier:
            return None;

        dto = GamePlayerListDto(self.__gameIdentifier);
        packet = Packet.GetPlayersListPacket(dto);

        reply = self.Send(packet);

        return reply.Players;

    #endregion

if __name__ == "__main__":
    pygame.init();
    ClientInstance().MenuMain();
