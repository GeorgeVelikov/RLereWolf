from models.roles.Peasant import Peasant;
from models.roles.Doctor import Doctor;

def TestPlayers():
    j = Peasant("James");
    d = Peasant("Donald");
    a = Doctor("Alison");
    j.Talk("Hello there Donald");
    d.Talk("Hello there James");
    a.Heal(d);
    j.Vote(d);
