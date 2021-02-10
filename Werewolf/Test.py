from game.Game import Game;
from game.Player import Player;

from models.roles.Peasant import Peasant;
from models.roles.Doctor import Doctor;

from game.infrastructure.Client import Client;

from utility.Helpers import nameof;
import threading;

game = Game("A game of Werewolf");

james = Player("James");
donald = Player("Donald");
alison = Player("Alison");

jamesRole = Peasant("James");
donaldRole = Peasant("Sir Donald");
alisonRole = Doctor("Alison VII");

def TestPlayers():
    game.Join(james);
    game.Join(donald);
    game.Join(alison);

    print(game.Players);
    return;

def TestPlayerRoles():
    jamesRole.Talk("Hello there Sir Donald");
    donaldRole.Talk("Hello there James");

    alisonRole.Heal(donaldRole);

    jamesRole.Vote(donaldRole);
    return;

def TestClientConnection():
    jamesClient = Client("James");
    threading.Thread(target = jamesClient.Connect).start();

    donaldClient = Client("Donald");
    threading.Thread(target = donaldClient.Connect).start();

    alisonClient = Client("Alison");
    threading.Thread(target = alisonClient.Connect).start();
    return;
