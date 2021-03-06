import Client.context.UIContext as UIContext;

import tkinter as tk
import tkinter.ttk as ttk

from tkinter import messagebox;

class MainWindow(tk.Tk):
    def __init__(self, context):
        self.__context = context;
        self.__content = None;
        super().__init__();

        self.title("Client");
        self.geometry("800x600");
        self.resizable(False, False);
        self.protocol("WM_DELETE_WINDOW", self.Close);

    #Override
    def Close(self):
        if not messagebox.askyesno("Exit", "Are you sure you want to exit the client?"):
            return False;

        self.__context.ServiceContext.LeaveGame();
        self.__context.ServiceContext.Disconnect();
        self.destroy();
        return True;

    def DisplayScreen(self, screen):
        newScreen = screen(self, self.__context);

        if self.__content is not None:
            self.__content.destroy();

        self.__content = newScreen.Content;