import tkinter as tk
import tkinter.ttk as ttk

import threading;
import time;

class GameListScreen(ttk.Frame):
    def __init__(self, root, client):
        self.__root = root;
        self.__client = client;
        super().__init__(root);

        self.pack(anchor="center", expand="true", side="top");

        self.__button_Group = ttk.Frame(self)
        self.__button_Group.grid();
        self.__button_Group.rowconfigure("3", pad="0");

        self.__listBox_Games = ttk.Listbox(self.__button_Group,\
            selectmode=tkinter.SINGLE);

        self.__threadGetGameList = threading.Thread(target = self.UpdateGamesList);
        self.__threadGetGameList.start();

    def UpdateGamesList(self):
        games = self.__client.GetGamesList();

        self.__listBox_Games.delete(0, tkinter.END);

        for index, (identifier, name) in enumerate(games):
            self.__listBox_Games.insert(index, name);

        time.sleep(2)
        self.UpdateGamesList();