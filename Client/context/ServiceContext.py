class ServiceContext():
    def __init__(self, context):
        self.__context = context;

    @property
    def ViewModelContext(self):
        return self.__context;
