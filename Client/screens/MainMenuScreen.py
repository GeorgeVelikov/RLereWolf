from Shared.utility.Helpers import nameof;

import Client.utility.UIContext as UIContext;
from Client.screens.ScreenBase import ScreenBase;

class MainMenuScreen(ScreenBase):
    def __init__(self, root, client):
        super().__init__(root, client);

        self.InitializeScreen();
        self.UpdateButtonWithClientName();

    def UpdateButtonWithClientName(self):
        self.GetObject(nameof(self.Client.SetName))\
            .configure(text=f"Set Name ({self.Client.Name})");

    def Connect_Clicked(self):
        try:
            self.Client.Connect();
            UIContext.ShowGameList(self.Root);
        except Exception as error:
            # TODO: gracefully fail, some error dialog, perhaps?
            pass;

        return;

    def SetName_Clicked(self):
        # TODO: dialog to set name
        self.Client.SetName("George");

        # update button text
        self.UpdateButtonWithClientName();
        return;
