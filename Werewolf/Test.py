from game.Game import Game;
from game.Player import Player;

from models.roles.Peasant import Peasant;
from models.roles.Doctor import Doctor;

from game.infrastructure.Client import Client;

from utility.Helpers import nameof;

game = Game("A game of Werewolf");

james = Player("James");
donald = Player("Donald");
alison = Player("Alison");

jamesRole = Peasant();
donaldRole = Peasant();
alisonRole = Doctor();

def TestPlayers():
    game.Join(james);
    game.Join(donald);
    game.Join(alison);

    return;

def TestPlayerRoles():
    jamesRole.Talk("Hello there Donald");
    donaldRole.Talk("Hello there James");

    alisonRole.Heal(donaldRole);

    jamesRole.Vote(donaldRole);
    return;

def TestClientConnection():
    jamesClient = Client();
    jamesClient.SetPlayer(jamesRole);

    donaldClient = Client();
    donaldClient.SetPlayer(donaldRole);

    alisonClient = Client();
    alisonClient.SetPlayer(alisonRole);
    return;
