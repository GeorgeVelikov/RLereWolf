from game.infrastructure.Client import Client;

from models.roles.Peasant import Peasant;
from models.roles.Doctor import Doctor;

james = Peasant("James");
donald = Peasant("Donald");
alison = Doctor("Alison");

def TestPlayers():
    james.Talk("Hello there Donald");
    donald.Talk("Hello there James");

    alison.Heal(donald);

    james.Vote(donald);

def TestPlayerConnection():
    jamesClient = Client();
    jamesClient.SetPlayer(james);

    donaldClient = Client();
    donaldClient.SetPlayer(donald);

    alisonClient = Client();
    alisonClient.SetPlayer(alison);
    return;
