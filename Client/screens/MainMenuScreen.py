from Shared.utility.Helpers import nameof;

import Client.utility.UIContext as UIContext;
from Client.screens.ScreenBase import ScreenBase;

class MainMenuScreen(ScreenBase):
    def __init__(self, root, client):
        super().__init__(root);
        self.__root = root;
        self.__client = client;

        self.InitializeScreen();

    def Connect_Clicked(self):
        try:
            self.__client.Connect();
            UIContext.ShowGameList(self.__root, self.__client);
        except Exception as error:
            # TODO: gracefully fail, some error dialog, perhaps?
            pass;

        return;

    def SetName_Clicked(self):
        # TODO: dialog to set name
        self.__client.SetName("George");

        # update button text
        self.GetObject(nameof(self.__client.SetName))\
            .configure(text=f"Set Name ({self.__client.Name})");
        return;
