# A collection of various methods which I found useful throughout the development.
import os

UNIX_CLEAR = "clear";
WIN_CLEAR = "cls";

def ClearScreen():
    os.system(UNIX_CLEAR if os.name == "posix" else WIN_CLEAR);

def PromptOption():
    try:
        return int(input("> "));
    except Exception as error:
        return -1;