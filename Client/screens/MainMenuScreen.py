from Shared.utility.Helpers import nameof;

from Client.screens.ScreenBase import ScreenBase;

import tkinter as tk;
import tkinter.ttk as ttk;

class MainMenuScreen(ScreenBase):
    def __init__(self, root, context):
        super().__init__(root, context);

        self.InitializeScreen();

        self.__connectButton = self.GetObject(nameof(self.Context.ServiceContext.Connect));
        self.__userName = self.GetVariable(nameof(self.Client.Name));
        self.__userName.set((self.Client.Name if self.Client.Name else "N/A"));

        self.UpdateConnectButton();

    def UpdateConnectButton(self):
        if not self.Client.Name or self.Client.Name.isspace():
            self.__connectButton["state"] = tk.DISABLED;
            return;

        self.__connectButton["state"] = tk.NORMAL;

    def Connect_Clicked(self):
        try:
            self.Context.ServiceContext.Connect();
            self.Context.UIContext.ShowGameList();
        except Exception as error:
            print("[ERROR] " + str(error));
            pass;

        return;

    def SetName_Clicked(self):
        userName = self.Context.UIContext\
            .ShowStringInputDialog("Set Name", "Enter your name:");

        if not userName or userName.isspace():
            return;

        self.Client.SetName(userName);
        self.__userName.set(self.Client.Name);

        # update button text
        self.UpdateConnectButton();
        self.Root.focus_set();
        return;

    def GameManual_Clicked(self):
        self.Context.UIContext.ShowClientManualDialog();
        return;

    def QuitGame_Clicked(self):
        self.Context.UIContext.CloseMainWindow();
        return;
