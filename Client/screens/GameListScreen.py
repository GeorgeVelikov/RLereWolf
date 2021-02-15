import tkinter as tk
import tkinter.ttk as ttk

class GameListScreen(ttk.Frame):
    def __init__(self, root, client):
        self.__client = client;
        super().__init__(root);

