import Shared.constants.NetConstants as NetConstants;
import Shared.constants.LogConstants as LogConstants;
from Shared.dtos.MessageDto import MessageDto;

from datetime import datetime;
import os;
from pathlib import Path;

SHARED_PATH = Path(os.path.dirname(os.path.dirname(__file__)));
LOGS_PATH = str(SHARED_PATH.parent) + os.path.sep + "Logs"\

def Log(status, message, game = None):
    # if you're training AI, you should probably do an early return in here because
    # that will speed up the iteration/second by 2.5x-3x, which could mean hours if you
    # are doing thousands of games. Furthermore, if you disable this, you can easily do more
    # concurrent games as none of the actions will prompt a file write lock.
    # return;

    utcNow = datetime.utcnow();

    filePath = LOGS_PATH \
        + os.path.sep + datetime.utcnow().strftime("%d-%m-%Y");

    fileName =  ("server" if not game else str(game)) + ".txt";

    if not os.path.exists(filePath):
        os.makedirs(filePath);

    utcNowFormatted = utcNow.strftime(NetConstants.DATETIME_FORMAT);

    logMessage = f"{utcNowFormatted} {status} {message}.";

    # This is only if you want to print stuff to the console for debugging purposes
    # This should already be stored in the Logs folder created by the framework, but
    # I suppose it's quite handy to have this easily accessible so that you can
    # keep track of any changes and how they affect the game logic/steps
    # print(logMessage);

    with open(filePath + os.path.sep + fileName, "a") as log:
        log.write("\n" + logMessage);

    return;

def CreateGameMessage(message, game):
    dto = MessageDto(None, message);
    Log(LogConstants.MESSAGE, dto.Content, game);
    game.Messages.add(dto);
    return dto;

# TODO: could you potentially DM other people? Should be pretty straight forward!
def CreatePrivateGameMessage(message, game, forPlayer):
    dto = MessageDto(None, message, forPlayer = forPlayer);
    Log(LogConstants.MESSAGE, dto.Content, game);
    game.Messages.add(dto);
    return dto;

def CreateTalkGameMessage(author, message, messageMetaData, game):
    dto = MessageDto(\
        author,\
        message,\
        messageMetaData = messageMetaData);

    Log(LogConstants.MESSAGE, dto.Content, game);
    game.Messages.add(dto);
    return dto

def CreateWhisperGameMessage(author, message, messageMetaData, game, forRole):
    dto = MessageDto(\
        author,\
        message,\
        messageMetaData = messageMetaData,\
        forRole = forRole);

    Log(LogConstants.MESSAGE, dto.Content, game);
    game.Messages.add(dto);
    return dto;

def Error(message, game = None):
    Log(LogConstants.ERROR, message, game);

def Warning(message, game = None):
    Log(LogConstants.WARNING, message, game);

def Information(message, game = None):
    Log(LogConstants.INFORMATION, message, game);

def Request(message, game = None):
    Log(LogConstants.REQUEST, message, game);
