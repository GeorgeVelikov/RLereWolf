from Shared.utility.Helpers import nameof;

import Client.utility.UIContext as UIContext;
from Client.screens.ScreenBase import ScreenBase;

import threading;
import time;

class GameListScreen(ScreenBase):
    def __init__(self, root, client):
        super().__init__(root);
        self.__root = root;
        self.__client = client;

        self.InitializeScreen();

        self.__threadGetGameList = threading.Thread(target = self.UpdateGamesList);
        self.__threadGetGameList.start();

    def UpdateGamesList(self):
        games = self.__client.GetGamesList();

        for index, (identifier, name) in enumerate(games.items()):
            pass;

        time.sleep(2)
        self.UpdateGamesList();