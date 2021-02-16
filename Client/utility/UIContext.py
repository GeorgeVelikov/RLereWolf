import Shared.constants.GameConstants as GameConstants;

from Client.screens.MainMenuScreen import MainMenuScreen;
from Client.screens.GameListScreen import GameListScreen;
from Client.screens.PlayerListScreen import PlayerListScreen;

import tkinter as tk
import tkinter.ttk as ttk

def ShowMainMenu(window):
    window.DisplayScreen(MainMenuScreen);

def ShowGameList(window):
    window.DisplayScreen(GameListScreen);

def ShowPlayerList(window):
    window.DisplayScreen(PlayerListScreen);
