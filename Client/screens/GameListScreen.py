from Shared.utility.KillableThread import KillableThread;
from Shared.utility.Helpers import nameof;

from Client.screens.ScreenBase import ScreenBase;

import tkinter as tk;

class GameListScreen(ScreenBase):
    def __init__(self, root, context):
        super().__init__(root, context);
        self.InitializeScreen();

        self.__gamesGrid = self.GetObject(nameof(self.Context.ServiceContext.GetGamesList));
        self.__gamesGridScrollBar = self.GetObject(\
            nameof(self.Context.ServiceContext.GetGamesList) + "Scrollbar");

        self.__gamesGrid.config(yscrollcommand = self.__gamesGridScrollBar.set);
        self.__gamesGridScrollBar.config(command = self.__gamesGrid.yview);

        self.__userName = self.GetVariable(nameof(self.Client.Name));
        self.__userName.set(self.Client.Name);

        self.__userIdentifier = self.GetVariable(nameof(self.Client.Identifier));
        self.__userIdentifier.set(self.Client.Identifier);

        self.__threadGetGameList = KillableThread(func = self.UpdateGamesList);
        self.__threadGetGameList.start();

    def UpdateGamesList(self):
        games = self.Context.ServiceContext.GetGamesList();

        currentSelection = self.__gamesGrid.focus();

        self.__gamesGrid.delete(*self.__gamesGrid.get_children());

        for game in games:
            # Store the identifier as "text", it's a hidden field anyways.
            self.__gamesGrid.insert(str(), tk.END,\
                text = game.Identifier,\
                values = (game.Name, game.Players));

        if currentSelection:
            # kind of a horrible hack to have  the current selection
            # still selected and not interfere with the user.
            # This is done because Tkinter indexes its items using capital
            # hex numbers under the format "I<hex>" where <hex> has at least 3 digits, i.e. "00A"
            intIndex = eval("0x" + currentSelection[1:]) + len(games);
            index = f"I{intIndex:03x}".upper();
            self.__gamesGrid.focus(index);
            self.__gamesGrid.selection_set(index);

        return;

    def StopBackgroundCalls(self):
        self.__threadGetGameList.Kill();
        return;

    def Disconnect_Clicked(self):
        self.StopBackgroundCalls();
        self.Context.ServiceContext.Disconnect();
        self.Context.UIContext.ShowMainMenu();
        return;

    def Join_Clicked(self):
        selection = self.__gamesGrid.focus();

        if not selection:
            return;

        item = self.__gamesGrid.item(selection);
        gameIdentifier = item["text"];

        self.StopBackgroundCalls();

        self.Context.ServiceContext.JoinGame(gameIdentifier);
        self.Context.UIContext.ShowGameLobby();

        return;