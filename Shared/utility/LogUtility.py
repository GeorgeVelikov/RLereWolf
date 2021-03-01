import Shared.constants.NetConstants as NetConstants;
import Shared.constants.LogConstants as LogConstants;
from Shared.dtos.MessageDto import MessageDto;

from datetime import datetime;
import os;
from pathlib import Path

SHARED_PATH = Path(os.path.dirname(os.path.dirname(__file__)));
LOGS_PATH = str(SHARED_PATH.parent) + "/Logs";

def Log(status, message, game = None):
    utcNow = datetime.utcnow();

    fileName = utcNow.strftime("%d-%m-%Y");

    if game:
        fileName += "-" + str(game);

    if not os.path.exists(LOGS_PATH):
        os.makedirs(LOGS_PATH);

    utcNowFormatted = utcNow.strftime(NetConstants.DATETIME_FORMAT);

    logMessage = f"{utcNowFormatted} {status} {message}.";
    print(logMessage);

    log = open(f"{LOGS_PATH}{os.path.sep}{fileName}.txt", "a");
    log.write("\n" + logMessage);
    log.close();

    return;

def CreateGameMessage(message, game):
    dto = MessageDto(None, message);
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
