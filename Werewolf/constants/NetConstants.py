import socket;

IP = socket.gethostbyname(socket.gethostname());
PORT = 26011;
ADDRESS = (IP, PORT);

BYTE = 2**10;
KILOBYTE = 2**20;

DATETIME_FORMAT = "%d/%m/%Y %H:%M:%S";