from game.infrastructure.ServerBase import ServerBase;
from game.Game import Game;

class Server(ServerBase):
    def __init(self, name):
        super().__init__();
        this.Name = name;
        this.Game = Game();
