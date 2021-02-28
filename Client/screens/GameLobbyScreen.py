from Shared.utility.KillableThread import KillableThread;
from Shared.utility.Helpers import nameof;

from Client.screens.ScreenBase import ScreenBase;

from Shared.enums.PlayerTypeEnum import PlayerTypeEnum;

import tkinter as tk;

class GameLobbyScreen(ScreenBase):
    def __init__(self, root, context):
        super().__init__(root, context);
        self.InitializeScreen();

        self.__playersListBox = self.GetObject("PlayerListBox");

        # don't need to keep track of messages, too much memory
        # would go into it with no gains to do it whatsoever.
        self.__messagesListBox = self.GetObject("MessagesListBox");

        self.__villagerButtons = self.GetObject(str(PlayerTypeEnum.Villager));
        self.__werewolfButtons = self.GetObject(str(PlayerTypeEnum.Werewolf));
        self.__seerButtons = self.GetObject(str(PlayerTypeEnum.Seer));
        self.__guardButtons = self.GetObject(str(PlayerTypeEnum.Guard));

        self.__isReadyButton = self.GetObject(nameof(self.Client.Player.IsReady));
        self.__isReadyButtonText = self.GetVariable(nameof(self.Client.Player.IsReady));

        self.UpdateButtons();

        self.__threadUpdateGameData = KillableThread(func = self.UpdateGameData);
        self.__threadUpdateGameData.start();

    #region Game Loop updates

    def UpdateGameData(self):
        game = self.Context.ServiceContext.GetGameLobby();

        self.UpdatePlayerList(game.Players);

        self.UpdateMessagesList(game.Messages);

    def UpdatePlayerList(self, players):
        newPlayerIdentifiers = [player.Identifier for player in players];

        currentPlayerIndices = self.__playersListBox.get_children();

        for playerIndex in currentPlayerIndices:
            item = self.__playersListBox.item(playerIndex);
            playerIdentifier = self.GetPlayerIdentifierFromIndex(playerIndex);

            if playerIdentifier not in newPlayerIdentifiers:
                self.__playersListBox.delete(playerIndex);
            else:
                columns = item["values"];
                player = next(player for player in players if player.Identifier == playerIdentifier)
                players.remove(player);

                newDisplayName = self.GetPlayerDisplayName(player);

                if (columns[0] == newDisplayName):
                    continue;

                columns[0] = newDisplayName;

                self.__playersListBox.delete(playerIndex);

                self.__playersListBox.insert(str(), tk.END,\
                text = playerIdentifier,\
                values = columns);

        for player in players:
            # Store the identifier as "text", it's a hidden field anyways.
            self.__playersListBox.insert(str(), tk.END,\
                text = player.Identifier,\
                values = (self.GetPlayerDisplayName(player)));

        return;

    def UpdateMessagesList(self, messages):
        if not messages:
            return;

        for message in messages:
            self.__messagesListBox.insert(tk.END, str(message));

        return;

    def UpdateButtons(self):
        self.UpdateGameControlButtons();
        self.UpdateIsReadyButton();

    def UpdateGameControlButtons(self):
        if not self.Client.Game.HasStarted:
            self.__villagerButtons.pack_forget();
            self.__werewolfButtons.pack_forget();
            self.__seerButtons.pack_forget();
            self.__guardButtons.pack_forget();
            return;

        self.__villagerButtons.pack();

        if not self.Client.Player.Role:
            print("No Role in the game.");
            return

        if self.Client.Player.Role == PlayerTypeEnum.Werewolf:
            self.__werewolfButtons.pack();

        elif self.Client.Player.Role == PlayerTypeEnum.Seer:
            self.__seerButtons.pack();

        elif self.Client.Player.Role == PlayerTypeEnum.Guard:
            self.__guardButtons.pack();

        return;

    def UpdateIsReadyButton(self):
        if self.Client.Game.HasStarted:
            self.__isReadyButton.grid_remove();
            return;

        if not self.__isReadyButton.winfo_ismapped():
            self.__isReadyButton.grid();

        buttonText = ("Cancel" if self.Client.Player.IsReady else "Ready");
        self.__isReadyButtonText.set(buttonText);

    #endregion

    #region Helpers

    def StopBackgroundCalls(self):
        self.__threadUpdateGameData.Kill();
        return;

    def GetPlayerDisplayName(self, player):
        readyStatus = str();
        identifier = str();
        deadStatus = str();

        if not self.Client.Game.HasStarted:
            readyStatus = "+" if player.IsReady else "-";
        elif self.Client.Game.HasStarted and not player.IsAlive:
            deadStatus = "[Dead]";

        if player.Identifier == self.Client.Player.Identifier:
            identifier = "(You)";

        return readyStatus + deadStatus + player.Name + identifier;

    def GetSelectedPlayerIdentifierFromTreeView(self):
        selectedPlayerIndex = self.__playersListBox.focus();

        if not selectedPlayerIndex or selectedPlayerIndex.isspace():
            return None;

        return self.GetPlayerIdentifierFromIndex(selectedPlayerIndex);

    def GetPlayerIdentifierFromIndex(self, index):
        playerItem = self.__playersListBox.item(index);

        return playerItem["text"];

    #endregion

    # General Controls
    def Talk_Clicked(self):
        return;

    def Vote_Clicked(self):
        selectedPlayerIdentifier = self.GetSelectedPlayerIdentifierFromTreeView();

        if not selectedPlayerIdentifier:
            return;

        self.Context.ServiceContext.Vote(selectedPlayerIdentifier);
        return;

    def Wait_Clicked(self):
        return;

    # Werewolf Controls
    def Whisper_Clicked(self):
        return;

    def Attack_Clicked(self):
        return;

    # Seer Controls
    def Divine_Clicked(self):
        return;

    # Guard Controls
    def Guard_Clicked(self):
        return;

    # Misc
    def Ready_Clicked(self):
        self.Context.ServiceContext.VoteStart();
        self.UpdateButtons();

    def Quit_Clicked(self):
        self.StopBackgroundCalls();
        self.Context.ServiceContext.LeaveGame();
        self.Context.UIContext.ShowGameList();
        return;
