from Client.screens.MainMenuScreen import MainMenuScreen;
from Client.screens.GameListScreen import GameListScreen;
from Client.screens.GameLobbyScreen import GameLobbyScreen;

from Client.MainWindow import MainWindow;

import tkinter as tk;
import tkinter.ttk as ttk;

from tkinter import simpledialog;
from tkinter import messagebox;

class UIContext():
    def __init__(self, context):
        self.__context = context;
        self.__mainWindow = MainWindow(context);

    @property
    def ViewModelContext(self):
        return self.__context;

    @property
    def MainWindow(self):
        return self.__mainWindow;

    def StartMainWindow(self):
        self.ShowMainMenu();
        self.__mainWindow.mainloop();
        return;

    def CloseMainWindow(self):
        if self.__mainWindow.Close():
            self.__context.ServiceContext.Disconnect();
        return;

    #region Window screens

    def ShowMainMenu(self):
        self.__mainWindow.DisplayScreen(MainMenuScreen);
        return;

    def ShowGameList(self):
        self.__mainWindow.DisplayScreen(GameListScreen);
        return;

    def ShowGameLobby(self):
        self.__mainWindow.DisplayScreen(GameLobbyScreen);
        return;

    #endregion

    #region Dialogs

    def ShowErrorDialog(self, error):
        return messagebox.showerror("Error", error);

    def ShowStringInputDialog(self, title, prompt):
        return simpledialog.askstring(title = title, prompt = prompt);

    #endregion
