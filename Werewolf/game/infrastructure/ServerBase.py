from http.server import HTTPServer, BaseHTTPRequestHandler;
from threading import Thread;
import socket;

import constants.NetConstants as NetConstants;

class ServerRequestHandlerBase(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(NetConstants.RESPONSE_OK);
        self.end_headers();
        self.wfile.write(b"Root page");

class ServerBase():
    def __init__(self):
        self.__serverAddress = (NetConstants.IP, NetConstants.PORT);
        self.__server = HTTPServer(self.__serverAddress, ServerRequestHandlerBase);
        self.__serverThread = Thread(target=self.__server.serve_forever);

    @property
    def ServerAddress(self):
        return ":".join(map(str, self.__serverAddress));

    def run(self):
        try:
            self.__serverThread.start();
            print("Server successfully started at " + self.ServerAddress);
        except:
            raise;

    def stop(self):
        try:
            self.__serverThread._stop();
            print("Server successfully stopped at " + self.ServerAddress);
        except:
            raise;
