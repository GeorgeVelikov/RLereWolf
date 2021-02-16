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
        self.__isRunningBackGroundTasks = True;

        self.InitializeScreen();

        self.__threadGetGameList = threading.Thread(target = self.UpdateGamesList);
        self.__threadGetGameList.start();

    def UpdateGamesList(self):
        while self.__isRunningBackGroundTasks:
            games = self.__client.GetGamesList();

            for index, (identifier, name) in enumerate(games.items()):
                pass;

            time.sleep(1);

    def StopBackgroundCalls(self):
        self.__isRunningBackGroundTasks = False;

        self.__threadGetGameList.join();

    def Disconnect_Clicked(self):
        self.StopBackgroundCalls();
        self.__client.Disconnect();
        UIContext.ShowMainMenu(self.__root);

    def Join_Clicked(self):
        pass;