import Shared.constants.CommunicationPresetConstants as CommunicationPresets;

class MessageRequestDto():
    def __init__(self,\
        gameIdentifier,\
        playerIdentifier,\
        talkMessage,\
        targetPlayerIdentifier = None,\
        targetPlayerRole = None):

        self.__gameIdentifier = gameIdentifier;
        self.__playerIdentifier = playerIdentifier;
        self.__talkMessage = talkMessage;
        self.__targetPlayerIdentifier = targetPlayerIdentifier;
        self.__targetPlayerRole = targetPlayerRole;

    @property
    def GameIdentifier(self):
        return self.__gameIdentifier;

    @property
    def PlayerIdentifier(self):
        return self.__playerIdentifier;

    @property
    def TalkMessage(self):
        return self.__talkMessage;

    @property
    def TargetPlayerIdentifier(self):
        return self.__targetPlayerIdentifier;

    @property
    def TargetPlayerRole(self):
        return self.__targetPlayerRole;

    # TODO: probably can go ahead and exclude this as this is a client only check
    @property
    def IsValid(self):
        return CommunicationPresets.IsMessageValid(\
            self.__talkMessage.MessageTemplate,\
            self.__targetPlayerIdentifier,\
            self.__targetPlayerRole);

#def ConstructMessageText(talkMessage, targetPlayer, targetRole):
#    if not talkMessage:
#        return None;

#    text = talkMessage.MessageTemplate;

#    if (CommunicationPresets.PLAYER in text) and targetPlayer:
#        text = text\
#            .replace(CommunicationPresets.PLAYER, targetPlayer.Name);
#    elif (CommunicationPresets.PLAYER in text) and not targetPlayer:
#        return None;

#    if (CommunicationPresets.ROLE in text) and targetRole:
#        text = text\
#            .replace(CommunicationPresets.ROLE, str(targetRole));
#    elif (CommunicationPresets.ROLE in text) and not targetRole:
#        return None;

#    return text;