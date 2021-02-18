from Shared.utility.Helpers import nameof;

import Client.utility.UIContext as UIContext;
from Client.screens.ScreenBase import ScreenBase;

import tkinter as tk;

import threading;
import time;

class GameLobbyScreen(ScreenBase):
    def __init__(self, root, client):
        super().__init__(root, client);
        self.__isRunningBackGroundTasks = True;

        self.InitializeScreen();

        self.__players = dict();
        self.__playersListBox = self.GetObject("PlayerListBox");

        # don't need to keep track of messages, too much memory
        # would go into it with no gains to do it whatsoever.
        self.__messagesListBox = self.GetObject("MessagesListBox");

        self.__threadUpdateGameData = threading.Thread(target = self.UpdateGameData);
        self.__threadUpdateGameData.start();

    def UpdateGameData(self):
        while self.__isRunningBackGroundTasks:

            game = self.Client.GetGameLobby();

            self.UpdatePlayerList(game.Players);

            self.UpdateMessagesList(game.Messages);

            time.sleep(1);

    def UpdatePlayerList(self, players):
        self.__players = dict((p.Identifier, p) for p in players);

        currentSelection = self.__playersListBox.curselection();

        self.__playersListBox.delete(int(), tk.END);

        if not players:
            return;

        for (identifier, player) in self.__players.items():
            self.__playersListBox.insert(tk.END, player.Name);

        if currentSelection:
            index = currentSelection[0];
            self.__playersListBox.select_set(index);
            self.__playersListBox.activate(index);

        return;

    def UpdateMessagesList(self, messages):
        if not messages:
            return;

        for message in messages:
            self.__messagesListBox.insert(tk.END, str(message));

        return;

    def StopBackgroundCalls(self):
        self.__isRunningBackGroundTasks = False;

        self.__threadUpdateGameData.join();
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
    def Ready_Clicked(self):
        return;

    def Quit_Clicked(self):
        self.StopBackgroundCalls();
        self.Client.LeaveGame();
        UIContext.ShowGameList(self.Root);
        return;