from game.Game import Game;
from game.Player import Player;

from models.roles.Peasant import Peasant;
from models.roles.Doctor import Doctor;

from game.infrastructure.Client import Client;

from utility.Helpers import nameof;
import threading;

game = Game("A game of Werewolf");

james = Player();
james.SetName("James");

donald = Player();
donald.SetName("Donald");

alison = Player();
alison.SetName("Alison");

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
    jamesClient = Client();
    jamesClient.SetName(james.Name);
    threading.Thread(target = jamesClient.Connect).start();

    donaldClient = Client();
    donaldClient.SetName(donald.Name);
    threading.Thread(target = donaldClient.Connect).start();

    alisonClient = Client();
    alisonClient.SetName(alison.Name);
    threading.Thread(target = alisonClient.Connect).start();
    return;
