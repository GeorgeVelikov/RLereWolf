from Shared.utility.KillableThread import KillableThread;
from Shared.utility.Helpers import nameof;

import Client.utility.TalkMessageUtility as TalkMessageUtility;
from Client.screens.ScreenBase import ScreenBase;

from Shared.enums.PlayerTypeEnum import PlayerTypeEnum;
from Shared.enums.TimeOfDayEnum import TimeOfDayEnum;

import tkinter as tk;

class GameLobbyScreen(ScreenBase):
    def __init__(self, root, context):
        super().__init__(root, context);
        self.InitializeScreen();

        self.__playersListBox = self.GetObject("PlayerListBox");
        self.__playersScrollBar = self.GetObject("PlayersScrollbar");
        self.__playersColumnId = "PlayersColumn";

        self.__playersListBox.config(yscrollcommand = self.__playersScrollBar.set);
        self.__playersScrollBar.config(command = self.__playersListBox.yview);

        # would go into it with no gains to do it whatsoever.
        self.__messagesListBox = self.GetObject("MessagesListBox");
        self.__messagesScrollBar = self.GetObject("MessagesScrollbar");

        self.__talkMessagesMenu = None;
        self.__whisperMessagesMenu = None;

        self.__gameName = self.GetVariable("GameName");
        self.__gameTurn = self.GetVariable("GameTurn");
        self.__gameTime = self.GetVariable("GameTime");
        self.__playerRole = self.GetVariable("RoleType");
        self.__playerRoleState = self.GetVariable("RoleState");

        self.__validTimeOfDayValues = TimeOfDayEnum.Values();

        self.__messagesListBox.config(yscrollcommand = self.__messagesScrollBar.set);
        self.__messagesScrollBar.config(command = self.__messagesListBox.yview);

        self.__villagerButtons = self.GetObject(str(PlayerTypeEnum.Villager));
        self.__werewolfButtons = self.GetObject(str(PlayerTypeEnum.Werewolf));
        self.__seerButtons = self.GetObject(str(PlayerTypeEnum.Seer));
        self.__guardButtons = self.GetObject(str(PlayerTypeEnum.Guard));

        self.__addAgentButton = self.GetObject("AddAgentButton");
        self.__removeAgentButton = self.GetObject("RemoveAgentButton");

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

        self.UpdateGameHeader();

        self.UpdateButtons();

        return;

    def UpdatePlayerList(self, players):
        players = sorted(players,\
            key = lambda p: p.Name, \
            reverse = False);

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
                values = [self.GetPlayerDisplayName(player)]);

        self.__playersListBox.heading(self.__playersColumnId,\
            text="Players " + self.Client.Game.PlayersCount)

        return;

    def UpdateMessagesList(self, messages):
        if not messages:
            return;

        # ascending order
        messages.sort(key = lambda m: m.TimeUtc,\
            reverse = False);

        (scrollX, scrollY) = self.__messagesScrollBar.get();
        shouldScrollToBottom = scrollY == 1;

        self.__messagesListBox.config(state = tk.NORMAL);

        for message in messages:
            self.__messagesListBox.insert(tk.END, str(message) + "\n");

        self.__messagesListBox.config(state = tk.DISABLED);

        if shouldScrollToBottom:
            self.__messagesListBox.see(tk.END);

        return;

    def UpdateGameHeader(self):
        self.__gameName.set(self.Client.Game.Name);

        if self.Client.Game.HasStarted:
            lastCycleTimeOfDay = self.__gameTime.get();
            lastCycleTimeOfDayEnum = TimeOfDayEnum.FromString(lastCycleTimeOfDay);

            self.__gameTurn.set(self.Client.Game.Turn);
            self.__gameTime.set(self.Client.Game.TimeOfDay);
            self.__playerRole.set(self.Client.Player.Role.Type);
            self.__playerRoleState.set("Alive" if self.Client.Player.IsAlive else "Dead");

            if lastCycleTimeOfDayEnum != self.Client.Game.TimeOfDay\
                and lastCycleTimeOfDayEnum in self.__validTimeOfDayValues:
                # this is a bit of an optimization, we probably don't want to call this on every loop
                # since we're using tkinter and not a dedicated graphics library, we try to be mindful
                self.UpdateGameControlButtons();

        else:
            self.__gameTurn.set("0");
            self.__gameTime.set("N/A");
            self.__playerRole.set("N/A");
            self.__playerRoleState.set("N/A");

        return;

    def UpdateButtons(self):
        self.UpdateGameControlButtons();
        self.UpdateIsReadyButton();
        self.SetupTalkAndWhisperSubMenu();

    def UpdateGameControlButtons(self):
        if not self.Client.Game.HasStarted:
            self.__villagerButtons.grid_remove();
            self.__werewolfButtons.grid_remove();
            self.__seerButtons.grid_remove();
            self.__guardButtons.grid_remove();
            return;

        self.__villagerButtons.grid();

        if not self.Client.Player.Role:
            print("No Role in the game.");
            return

        if self.Client.Player.Role.Type == PlayerTypeEnum.Werewolf:
            self.__werewolfButtons.grid();

        elif self.Client.Player.Role.Type == PlayerTypeEnum.Seer:
            self.__seerButtons.grid();

        elif self.Client.Player.Role.Type == PlayerTypeEnum.Guard:
            self.__guardButtons.grid();

        return;

    def UpdateIsReadyButton(self):
        if self.Client.Game.HasStarted:
            self.__addAgentButton.grid_remove();
            self.__removeAgentButton.grid_remove();
            self.__isReadyButton.grid_remove();
            return;

        if not self.__addAgentButton.winfo_ismapped():
            self.__addAgentButton.grid();

        if not self.__removeAgentButton.winfo_ismapped():
            self.__removeAgentButton.grid();

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
        specialRoleIdentifier = str();

        # TODO: this is really not great, but this will do for now since we have no formal game GUI

        # before player.Name
        if not self.Client.Game.HasStarted:
            readyStatus = "+ " if player.IsReady else "- ";
        elif self.Client.Game.HasStarted and not player.IsAlive:
            deadStatus = "[Dead] ";

        # after player.Name
        if player.Identifier == self.Client.Player.Identifier:
            identifier = " (You)";

        if self.Client.Player.Role\
            and player.Role\
            and self.Client.Player.Role.Type == PlayerTypeEnum.Werewolf\
            and player.Role.Type == PlayerTypeEnum.Werewolf:
            specialRoleIdentifier = " (Werewolf)";

        return readyStatus + deadStatus + player.Name + identifier + specialRoleIdentifier;

    def GetSelectedPlayerIdentifierFromTreeView(self):
        selectedPlayerIndex = self.__playersListBox.focus();

        if not selectedPlayerIndex or selectedPlayerIndex.isspace():
            return None;

        return self.GetPlayerIdentifierFromIndex(selectedPlayerIndex);

    def GetPlayerIdentifierFromIndex(self, index):
        playerItem = self.__playersListBox.item(index);

        return playerItem["text"];

    def ToggleButtonsInLayout(self, layout):
        buttons = layout.winfo_children();

        for button in buttons:
            state = button["state"];
            button.config(state = tk.DISABLED if state == tk.NORMAL else tk.NORMAL);

        return;

    def SetupTalkAndWhisperSubMenu(self):
        if (self.Client.Game.HasStarted and self.__talkMessagesMenu) or\
            (not self.Client.Game.HasStarted and not self.__talkMessagesMenu):

            return;

        if not self.Client.Game.HasStarted and self.__talkMessagesMenu:
            self.__talkMessagesMenu = None;
            self.__whisperMessagesMenu = None;
            return;

        # This is a bit hacky, but makes sure we only pass this
        # there is a change in the has started game property
        self.__talkMessagesMenu = tk.Menu(self.Root, tearoff = False);
        clientRole = self.Client.Player.Role.Type;
        previousMessageRole = None;

        for message in TalkMessageUtility.TalkMessagesForRole(clientRole):

            if previousMessageRole != message.PlayerType:
                self.__talkMessagesMenu.add_separator();

            if message.IsRoleBased:
                bufferMenu = tk.Menu(self.Root, tearoff = False);

                for role in PlayerTypeEnum.Values():
                    bufferMenu.add_command(\
                        label = str(role),\
                        command = lambda: self.Talk_SendMessage(message, role));

                    pass;

                self.__talkMessagesMenu.add_cascade(\
                    label = message.MessageName,\
                    menu = bufferMenu);
            else:
                self.__talkMessagesMenu.add_command(\
                    label = message.MessageName,\
                    command = lambda: self.Talk_SendMessage(message));

            previousMessageRole = message.PlayerType;

            continue;

        if clientRole in TalkMessageUtility.ROLES_THAT_CAN_WHISPER:
            self.__whisperMessagesMenu = tk.Menu(self.Root, tearoff = False);

            for message in TalkMessageUtility.WhisperMessagesForRole(clientRole):
                 self.__whisperMessagesMenu.add_command(\
                    label = message.MessageName,\
                    command = lambda: self.Talk_SendMessage(message));

                 continue;

        return;

    #endregion

    # General Controls
    def Talk_Clicked(self):
        x = self.Root.winfo_pointerx();
        y = self.Root.winfo_pointery();

        self.__talkMessagesMenu.tk_popup(x, y);
        return;

    def Talk_SendMessage(self, messageType, role = None):
        return;

    def Vote_Clicked(self):
        if self.Client.Game.TimeOfDay != TimeOfDayEnum.Day:
            return;

        selectedPlayerIdentifier = self.GetSelectedPlayerIdentifierFromTreeView();

        if not selectedPlayerIdentifier:
            return;

        if selectedPlayerIdentifier == self.Client.Player.Identifier:
            return;

        self.Context.ServiceContext.Vote(selectedPlayerIdentifier);
        return;

    def Wait_Clicked(self):
        self.Context.ServiceContext.Wait();
        return;

    # Werewolf Controls
    def Whisper_Clicked(self):
        return;

    def Attack_Clicked(self):
        if self.Client.Game.TimeOfDay != TimeOfDayEnum.Night or\
            self.Client.Player.Role.Type != PlayerTypeEnum.Werewolf:
            return;

        selectedPlayerIdentifier = self.GetSelectedPlayerIdentifierFromTreeView();

        if not selectedPlayerIdentifier:
            return;

        if selectedPlayerIdentifier == self.Client.Player.Identifier:
            return;

        self.Context.ServiceContext.Attack(selectedPlayerIdentifier);
        return;

    # Seer Controls
    def Divine_Clicked(self):
        if self.Client.Game.TimeOfDay != TimeOfDayEnum.Night or\
            self.Client.Player.Role.Type != PlayerTypeEnum.Seer:
            return;

        selectedPlayerIdentifier = self.GetSelectedPlayerIdentifierFromTreeView();

        if not selectedPlayerIdentifier:
            return;

        if selectedPlayerIdentifier == self.Client.Player.Identifier:
            return;

        self.Context.ServiceContext.Divine(selectedPlayerIdentifier);
        return;

    # Guard Controls
    def Guard_Clicked(self):
        if self.Client.Game.TimeOfDay != TimeOfDayEnum.Night or\
            self.Client.Player.Role.Type != PlayerTypeEnum.Guard:
            return;

        selectedPlayerIdentifier = self.GetSelectedPlayerIdentifierFromTreeView();

        if not selectedPlayerIdentifier:
            return;

        self.Context.ServiceContext.Guard(selectedPlayerIdentifier);
        return;

    # Misc
    def AddAgent_Clicked(self):
        if self.Client.Game.HasStarted:
            return;

        self.Context.ServiceContext.AddAgentToGame();
        return;

    def RemoveAgent_Clicked(self):
        if self.Client.Game.HasStarted:
            return;

        self.Context.ServiceContext.RemoveAgentFromGame();
        return;

    def Ready_Clicked(self):
        if self.Client.Game.HasStarted:
            return;

        self.Context.ServiceContext.VoteStart();
        self.UpdateButtons();
        return;

    def Quit_Clicked(self):
        self.StopBackgroundCalls();
        self.Context.ServiceContext.LeaveGame();
        self.Context.UIContext.ShowGameList();
        return;
