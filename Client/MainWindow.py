import Client.utility.UIContext as UIContext;

import tkinter as tk
import tkinter.ttk as ttk

from tkinter import messagebox;

class MainWindow(tk.Tk):
    def __init__(self, client):
        self.__client = client;
        self.__content = None;
        super().__init__();

        self.title("Client");
        self.geometry("800x600");
        self.resizable(False, False);
        self.protocol("WM_DELETE_WINDOW", self.OnWindowClose);

        self.DisplayMainMenu();

        self.mainloop();

    #Override
    def OnWindowClose(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit the client?"):
            self.__client.Disconnect();
            self.destroy();

    def DisplayScreen(self, screen):
        newScreen = screen(self, self.__client);

        if self.__content is not None:
            self.__content.destroy();

        self.__content = newScreen.Content;

    def DisplayMainMenu(self):
        UIContext.ShowMainMenu(self);