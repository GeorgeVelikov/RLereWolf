from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler

PORT = 8000;

class ServerBase():
    def __init__(self):
        self.ServerAddress = (str(), PORT);
        self.__server = HTTPServer(self.ServerAddress, BaseHTTPRequestHandler);

    def run(self):
        self.__server.serve_forever();
