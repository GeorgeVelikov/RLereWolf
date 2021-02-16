from Shared.utility.Helpers import nameof;

import Client.utility.UIContext as UIContext;
from Client.screens.ScreenBase import ScreenBase;

import tkinter as tk;

import threading;
import time;

class PlayerListScreen(ScreenBase):
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

    def UpdatePlayerList(self):
        while self.__isRunningBackGroundTasks:
            self.__players = self.__client.GetPlayerList();

            self.__playersListBox.delete(int(), tk.END);

            for index, (identifier, name) in enumerate(self.__players.items()):
                self.__playersListBox.insert(tk.END, name);

            time.sleep(1);

    def StopBackgroundCalls(self):
        self.__isRunningBackGroundTasks = False;

        self.__threadGetPlayerList.join();
        return;

    def Quit_Clicked(self):
        self.StopBackgroundCalls();
        self.__client.LeaveGame();
        UIContext.ShowGameList(self.__root);
        return;