from models.roles.Peasant import Peasant;
from models.roles.Doctor import Doctor;

def TestPlayers():
    james = Peasant("James");
    donald = Peasant("Donald");
    alison = Doctor("Alison");

    james.Talk("Hello there Donald");
    donald.Talk("Hello there James");

    alison.Heal(donald);

    james.Vote(donald);
