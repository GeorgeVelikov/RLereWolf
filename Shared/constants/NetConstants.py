import socket;

IP = socket.gethostbyname(socket.gethostname());
PORT = 26011;
ADDRESS = (IP, PORT);

BYTE = 2**10;
KILOBYTE = 2**20;

DATE_FORMAT = "%d/%m/%Y";
TIME_FORMAT = "%H:%M:%S";
DATETIME_FORMAT = DATE_FORMAT + " " + TIME_FORMAT;