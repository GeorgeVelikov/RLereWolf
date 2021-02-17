class UpdatedEntityDto():
    def __init__(self, entity, updatedUtc):
        self.__entity = entity;
        self.__updatedUtc = updatedUtc;

    @property
    def Entity(self):
        return self.__entity;

    @property
    def UpdatedUtc(self):
        return self.__updatedUtc;
