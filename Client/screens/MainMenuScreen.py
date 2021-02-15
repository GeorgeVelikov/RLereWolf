import tkinter as tk
import tkinter.ttk as ttk

from functools import partial

class MainMenuScreen(ttk.Frame):
    def __init__(self, root, client):
        self.__client = client;
        super().__init__(root);

        self.pack(anchor="center", expand="true", side="top");

        self.__button_Group = ttk.Frame(self)
        self.__button_Group.grid();
        self.__button_Group.rowconfigure("3", pad="0");

        self.__button_Connect = ttk.Button(self.__button_Group,\
            command=self.Connect_Click);

        self.__button_Connect.configure(text="Connect");
        self.__button_Connect.pack(ipadx="100", ipady="5", pady="10", side="top");

        self.__button_SetName = ttk.Button(self.__button_Group,\
            command=self.SetName_Click);

        self.__button_SetName.configure(default="normal", text=f"Set Name ({self.__client.Name})");
        self.__button_SetName.pack(ipadx="100", ipady="5", pady="10", side="top");

    def Connect_Click(self):
        self.__client.Connect();
        return;

    def SetName_Click(self):
        # TODO: dialog to set name
        self.__client.SetName("George");
        self.__button_SetName.configure(default="normal", text=f"Set Name ({self.__client.Name})");
        return;
