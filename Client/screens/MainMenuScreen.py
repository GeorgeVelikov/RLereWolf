from Shared.utility.Helpers import nameof;

from Client.screens.ScreenBase import ScreenBase;

import tkinter as tk;
import tkinter.ttk as ttk;

class MainMenuScreen(ScreenBase):
    def __init__(self, root, context):
        super().__init__(root, context);

        self.InitializeScreen();

        self.__connectButton = self.GetObject(nameof(self.Client.Connect));
        self.__userName = self.GetVariable(nameof(self.Client.Name));

        self.__userName.set(self.Client.Name);

        self.UpdateConnectButton();

    def UpdateConnectButton(self):
        if not self.Client.Name or self.Client.Name.isspace():
            self.__connectButton["state"] = tk.DISABLED;
            return;

        self.__connectButton["state"] = tk.NORMAL;

    def Connect_Clicked(self):
        try:
            self.Client.Connect();
            self.Context.UIContext.ShowGameList();
        except Exception as error:
            print("[ERROR] " + str(error));
            pass;

        return;

    def SetName_Clicked(self):
        self.Client.SetName(self.__userName.get());

        # update button text
        self.UpdateConnectButton();
        self.Root.focus_set();
        return;

    def QuitGame_Clicked(self):
        self.Client.QuitGame();
        return;
