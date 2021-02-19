class ServiceContext():
    def __init__(self, context):
        self.__context = context;

    @property
    def ViewModelContext(self):
        return self.__context;

    @property
    def Client(self):
        if not self.__context:
            return None;

        return self.__context.Client;


