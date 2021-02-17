from Shared.utility.Helpers import nameof;

import Client.utility.UIContext as UIContext;
from Client.screens.ScreenBase import ScreenBase;

import tkinter as tk;

import threading;
import time;

class GameLobbyScreen(ScreenBase):
    def __init__(self, root, client):
        super().__init__(root);
        self.__root = root;
        self.__client = client;
        self.__isRunningBackGroundTasks = True;

        self.InitializeScreen();

        self.__players = dict();
        self.__playersListBox = self.GetObject(nameof(self.__client.GetPlayerList));

        self.__threadGetPlayerList = threading.Thread(target = self.UpdatePlayerList);
        self.__threadGetPlayerList.start();

    # TODO: have a "shared" game object which the server can toss to all clients
    def UpdatePlayerList(self):
        while self.__isRunningBackGroundTasks:
            self.__players = self.__client.GetPlayerList();

            game = self.__client.GetGameLobby();

            currentSelection = self.__playersListBox.curselection();

            self.__playersListBox.delete(int(), tk.END);

            for index, (identifier, name) in enumerate(self.__players.items()):
                self.__playersListBox.insert(tk.END, name);

            if currentSelection:
                index = currentSelection[0];
                self.__playersListBox.select_set(index);
                self.__playersListBox.activate(index);

            time.sleep(1);

    def StopBackgroundCalls(self):
        self.__isRunningBackGroundTasks = False;

        self.__threadGetPlayerList.join();
        return;

    # General Controls
    def Talk_Clicked(self):
        return;

    def Vote_Clicked(self):
        return;

    def Wait_Clicked(self):
        return;

    # Werewolf Controls
    def Whisper_Clicked(self):
        return;

    def Attack_Clicked(self):
        return;

    # Seer Controls
    def Divine_Clicked(self):
        return;

    # Guard Controls
    def Guard_Clicked(self):
        return;

    # Misc
    def Quit_Clicked(self):
        self.StopBackgroundCalls();
        self.__client.LeaveGame();
        UIContext.ShowGameList(self.__root);
        return;