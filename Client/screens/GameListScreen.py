import tkinter as tk
import tkinter.ttk as ttk

import threading;

class GameListScreen(ttk.Frame):
    def __init__(self, root, client):
        self.__client = client;
        super().__init__(root);

        self.__threadGetGameList = threading.Thread();
