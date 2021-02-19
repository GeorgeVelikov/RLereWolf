from Client.context.UIContext import UIContext;
from Client.context.ServiceContext import ServiceContext;

class ViewModelContext():
    def __init__(self, client):
        self.__client = client;

        self.__uiContext = UIContext(self);
        self.__serviceContext = ServiceContext(self);

    @property
    def Client(self):
        return self.__client;

    @property
    def UIContext(self):
        return self.__uiContext;

    @property
    def ServiceContext(self):
        return self.__serviceContext;
