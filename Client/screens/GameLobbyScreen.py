from Shared.utility.Helpers import nameof;

from Client.screens.ScreenBase import ScreenBase;

import tkinter as tk;

import threading;
import time;

class GameLobbyScreen(ScreenBase):
    def __init__(self, root, context):
        super().__init__(root, context);
        self.__isRunningBackGroundTasks = True;

        self.InitializeScreen();

        self.__playersListBox = self.GetObject("PlayerListBox");

        # don't need to keep track of messages, too much memory
        # would go into it with no gains to do it whatsoever.
        self.__messagesListBox = self.GetObject("MessagesListBox");

        self.__isReadyButton = self.GetObject(nameof(self.Client.Player.IsReady));
        self.__isReadyButtonText = self.GetVariable(nameof(self.Client.Player.IsReady));

        self.UpdateIsReadyButton();

        self.__threadUpdateGameData = threading.Thread(target = self.UpdateGameData);
        self.__threadUpdateGameData.start();

    def UpdateGameData(self):
        while self.__isRunningBackGroundTasks:

            game = self.Context.ServiceContext.GetGameLobby();

            self.UpdatePlayerList(game.Players);

            self.UpdateMessagesList(game.Messages);

            time.sleep(1);

    def UpdatePlayerList(self, players):
        currentSelection = self.__playersListBox.curselection();

        self.__playersListBox.delete(int(), tk.END);

        if not players:
            return;

        for player in players:
            readyStatus = str();
            identifier = str();

            if not self.Client.Game.HasStarted:
                readyStatus = "+ " if player.IsReady else "- ";

            if player.Identifier == self.Client.Player.Identifier:
                identifier = " (You)";

            self.__playersListBox.insert(tk.END, readyStatus + player.Name + identifier);

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

    def UpdateIsReadyButton(self):
        if self.Client.Game.HasStarted:
            self.__isReadyButton.grid_remove();
            return;

        if not self.__isReadyButton.winfo_ismapped():
            self.__isReadyButton.grid();

        buttonText = ("Cancel" if self.Client.Player.IsReady else "Ready");
        self.__isReadyButtonText.set(buttonText);

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
        self.Context.ServiceContext.VoteStart();
        self.UpdateIsReadyButton();

    def Quit_Clicked(self):
        self.StopBackgroundCalls();
        self.Context.ServiceContext.LeaveGame();
        self.Context.UIContext.ShowGameList();
        return;