from Shared.utility.Helpers import nameof;

import Client.utility.UIContext as UIContext;
from Client.screens.ScreenBase import ScreenBase;

import tkinter as tk;
import tkinter.ttk as ttk;

class MainMenuScreen(ScreenBase):
    def __init__(self, root, client):
        super().__init__(root, client);

        self.InitializeScreen();

        self.__connectButton = self.GetObject(nameof(self.Client.Connect));

        self.UpdateConnectButton();

    def UpdateConnectButton(self):
        if not self.Client.Name:
            self.__connectButton["state"] = tk.DISABLED;
            return;

        self.__connectButton["state"] = tk.NORMAL;

    def Connect_Clicked(self):
        try:
            self.Client.Connect();
            UIContext.ShowGameList(self.Root);
        except Exception as error:
            # TODO: gracefully fail, some error dialog, perhaps?
            pass;

        return;

    def SetName_Clicked(self):
        # TODO: dialog to set name
        userName = self.GetVariable(nameof(self.Client.Name));

        self.Client.SetName(userName.get());

        # update button text
        self.UpdateConnectButton();
        self.Root.focus_set();
        return;
