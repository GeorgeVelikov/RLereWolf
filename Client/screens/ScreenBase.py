import Client.constants.ClientConstants as ClientConstants;

import tkinter as tk;
import tkinter.ttk as ttk;
import pygubu;

class ScreenBase():
    def __init__(self, root, context):
        self.__root = root;
        self.__context = context;
        self.__builder = pygubu.Builder();
        self.__content = None;

    def InitializeScreen(self):
        self.__builder.add_from_file(ClientConstants.RELATIVE_UI_PATH + self.ClassName + ".ui");
        self.__content = self.__builder.get_object(self.ClassName);
        self.__builder.connect_callbacks(self);

    def GetObject(self, objectId):
        return self.__builder.get_object(objectId);

    def GetVariable(self, variableId):
        return self.__builder.get_variable(variableId);

    @property
    def ClassName(self):
        return self.__class__.__name__;

    @property
    def Root(self):
        return self.__root;

    @property
    def Context(self):
        return self.__context;

    @property
    def Client(self):
        if not self.__context:
            return None;

        return self.__context.Client;

    @property
    def Content(self):
        return self.__content;
