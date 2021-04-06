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

    def ShowClientManualDialog(self):
        # TODO: add actual manual, this is more of a
        # placeholder with some minor formatting hints
        manual = \
            "I. Placeholder Alpha" +\
            \
            "\n\t1. Morbi gravida libero nisi, et ultricies sem mattis id. Cras vitae diam ipsum. " +\
            "Sed porta ac est eget gravida. Praesent mattis, sapien nec laoreet venenatis, metus eros " +\
            "interdum lacus, id ultrices felis nulla ut nibh. Donec ut dui eu est ornare vestibulum. " +\
            "Donec suscipit vel nisl in vulputate. Mauris congue iaculis odio, ut tempus nisi porta non. " +\
            "Morbi eget turpis a nisl suscipit pretium eu quis tortor. Lorem ipsum dolor sit amet, " +\
            "consectetur adipiscing elit. Mauris commodo feugiat lectus, vitae egestas eros lacinia sed. " +\
            "Donec interdum mollis magna. Nulla a ex id urna maximus tristique." +\
            \
            "\nII. Placeholder Beta";

        return self.ShowInformationDialog(manual, "Client Manual");

    def ShowStringInputDialog(self, title, prompt):
        return simpledialog.askstring(title = title, prompt = prompt);

    def ShowErrorDialog(self, error, title = "Error"):
        return messagebox.showerror(title, error);

    def ShowInformationDialog(self, message, title = "Information"):
        return messagebox.showinfo(title, message);

    #endregion
