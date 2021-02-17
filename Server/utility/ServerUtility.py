import Shared.constants.NetConstants as NetConstants;
from Shared.dtos.MessageDto import MessageDto;

import Server.constants.LogConstants as LogConstants;

from datetime import datetime;
import os;

def Log(status, message):

    utcNow = datetime.utcnow();

    fileName = utcNow.strftime("%d-%m-%Y");

    if not os.path.exists(LogConstants.DIRECTORY_LOGS):
        os.makedirs(LogConstants.DIRECTORY_LOGS);

    utcNowFormatted = utcNow.strftime(NetConstants.DATETIME_FORMAT);

    logMessage = f"{utcNowFormatted} {status} {message}.";
    print(logMessage);

    log = open(f"{LogConstants.DIRECTORY_LOGS}{os.path.sep}{fileName}.txt", "a");
    log.write("\n" + logMessage);
    log.close();

    return;

def CreateGameMessage(message):
    dto = MessageDto(None, message);
    Log(LogConstants.MESSAGE, dto.Content);
    return dto;
