from Shared.utility.Helpers import nameof;

import Client.utility.UIContext as UIContext;
from Client.screens.ScreenBase import ScreenBase;

import tkinter as tk;

import threading;
import time;

class GameListScreen(ScreenBase):
    def __init__(self, root, client):
        super().__init__(root, client);
        self.__isRunningBackGroundTasks = True;

        self.InitializeScreen();

        self.__games = dict();
        self.__gamesListBox = self.GetObject(nameof(self.Client.GetGamesList));

        self.__threadGetGameList = threading.Thread(target = self.UpdateGamesList);
        self.__threadGetGameList.start();

    def UpdateGamesList(self):
        while self.__isRunningBackGroundTasks:
            self.__games = self.Client.GetGamesList();

            currentSelection = self.__gamesListBox.curselection();

            self.__gamesListBox.delete(int(), tk.END);

            for index, (identifier, name) in enumerate(self.__games.items()):
                self.__gamesListBox.insert(tk.END, name);

            if currentSelection:
                index = currentSelection[0];
                self.__gamesListBox.select_set(index);
                self.__gamesListBox.activate(index);

            time.sleep(1);

    def StopBackgroundCalls(self):
        self.__isRunningBackGroundTasks = False;

        self.__threadGetGameList.join();
        return;

    def Disconnect_Clicked(self):
        self.StopBackgroundCalls();
        self.Client.Disconnect();
        UIContext.ShowMainMenu(self.Root);
        return;

    def Join_Clicked(self):
        selection = self.__gamesListBox.curselection();

        if not selection:
            return;

        self.StopBackgroundCalls();

        selectedGameIndex = selection[0];
        selectedGameIdentifier = list(self.__games)[selectedGameIndex];

        self.Client.JoinGame(selectedGameIdentifier);
        UIContext.ShowGameLobby(self.Root);

        return;