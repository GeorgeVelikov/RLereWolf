from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

import logging;
import threading;

IP = "localhost";
PORT = 8000;

RESPONSE_OK = 200;

class ServerRequestHandlerBase(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(RESPONSE_OK);
        self.end_headers();
        self.wfile.write(b"Root page");

class ServerBase():
    def __init__(self):
        self.__serverAddress = (IP, PORT);
        self.__server = HTTPServer(self.__serverAddress, ServerRequestHandlerBase);
        self.__serverThread = Thread(target=self.__server.serve_forever);

    @property
    def ServerAddress(self):
        return " ".join(map(str, self.__serverAddress));

    def run(self):
        try:
            self.__serverThread.start();
            logging.info("Server successfully started at " + self.ServerAddress);
        except:
            raise;

    def stop(self):
        try:
            self.__serverThread._stop();
            logging.info("Server successfully stopped at " + self.ServerAddress);
        except:
            raise;
