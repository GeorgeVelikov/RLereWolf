import Shared.constants.NetConstants as NetConstants;
import Shared.constants.LogConstants as LogConstants;
from Shared.dtos.MessageDto import MessageDto;

from datetime import datetime;
import os;
from pathlib import Path;

SHARED_PATH = Path(os.path.dirname(os.path.dirname(__file__)));
LOGS_PATH = str(SHARED_PATH.parent) + os.path.sep + "Logs"\

def Log(status, message, game = None):
    utcNow = datetime.utcnow();

    filePath = LOGS_PATH \
        + os.path.sep + datetime.utcnow().strftime("%d-%m-%Y");

    fileName =  ("server" if not game else str(game)) + ".txt";

    if not os.path.exists(filePath):
        os.makedirs(filePath);

    utcNowFormatted = utcNow.strftime(NetConstants.DATETIME_FORMAT);

    logMessage = f"{utcNowFormatted} {status} {message}.";
    print(logMessage);

    with open(filePath + os.path.sep + fileName, "a") as log:
        log.write("\n" + logMessage);

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
