import Client.constants.ClientConstants as ClientConstants;

import tkinter as tk;
import tkinter.ttk as ttk;
import pygubu;

class ScreenBase():
    def __init__(self, root, client):
        self.__root = root;
        self.__client = client;
        self.__builder = pygubu.Builder();
        self.__content = None;

    def InitializeScreen(self):
        self.__builder.add_from_file(ClientConstants.RELATIVE_UI_PATH + self.ClassName + ".ui");
        self.__content = self.__builder.get_object(self.ClassName);
        self.__builder.connect_callbacks(self);

    def GetObject(self, objectId):
        return self.__builder.get_object(objectId);

    @property
    def ClassName(self):
        return self.__class__.__name__;

    @property
    def Content(self):
        return self.__content;

    @property
    def Root(self):
        return self.__root;

    @property
    def Client(self):
        return self.__client;
