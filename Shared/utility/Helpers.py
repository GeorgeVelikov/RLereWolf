# A collection of various methods which I found useful throughout the development.

from varname.helpers import nameof;
from faker import Faker;

# using English only because we'll get a failure when trying to pickle
fakerFactory = Faker(['en_GB', 'en_US']);

def GenerateFirstName():
    return fakerFactory.first_name();

def GenerateLastName():
    return fakerFactory.last_name();

def GenerateFullName():
    return GenerateFirstName() + " " + GenerateLastName();
