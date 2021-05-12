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
            "Welcome to RLereWolf's Client!" +\
            \
            "\n\n" +\
            "I. What is this?\n" +\
            "The RLereWolf Client is an implementation of the Werewolf game. This application allows you to play " +\
            "Werewolf with other human and AI players. In its current iteration only the Villager, Guard, Seer, " +\
            "and Werewolf roles are implemented. For more information on RLereWolf, visit the URL " +\
            "github.com/GeorgeVelikov/RLereWolf" +\
            "\n\n" +\
            \
            "II. What do I do now?\n" +\
            "In order to start playing with other players, you must set your name/alias, by pressing the " +\
            "'Set Name' button, located in the main menu. Once you have set your name, you will be able to connect " +\
            "to the game server!" +\
            "\n\n" +\
            \
            "III. How do I join a game once I am connected?\n" +\
            "In order to join a specific game, you must select the game you want to join and press the 'Join' " +\
            "button, located at the bottom right of the screen. Alternatively, you can create your own game by " +\
            "pressing the 'Create' button in the bottom right of the screen." +\
            "\n\n" +\
            \
            "IV. How do I play the game once I have joined a game?\n" +\
            "Whenever you join a game, it will be a non-started state as not all of the players are ready! You can " +\
            "set yourself as ready by pressing the 'Ready' button at the bottom right of the screen. Once everyone " +\
            "ready, the game will randomly distribute roles and start at day time." +\
            "\n\n" +\
            \
            "V. How do I play my role?\n" +\
            "The game is based entirely on the base Werewolf game. In order to further familiarize yourself " +\
            "with the rules and Player roles of Werewolf and RLereWolf, please read the user manual or the " +\
            "official rule book.";

        return self.ShowInformationDialog(manual, "Client Manual");

    def ShowStringInputDialog(self, title, prompt):
        return simpledialog.askstring(title = title, prompt = prompt);

    def ShowErrorDialog(self, error, title = "Error"):
        return messagebox.showerror(title, error);

    def ShowInformationDialog(self, message, title = "Information"):
        return messagebox.showinfo(title, message);

    #endregion
