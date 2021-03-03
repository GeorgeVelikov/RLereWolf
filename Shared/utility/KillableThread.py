import threading

# Heavily inspired from https://stackoverflow.com/a/325528
class KillableThread(threading.Thread):
    def __init__(self, func, sleepIntervalSeconds = 1):
        super().__init__();
        self.__func = func;
        self.__killEvent = threading.Event();
        self.__sleepIntervalSeconds = sleepIntervalSeconds;

    #override
    def run(self):
        while True:
            self.__func();

            # If no kill signal is set, sleep for the interval,
            # If kill signal comes in while sleeping, immediately
            # wake up and handle
            if self.__killEvent.wait(self.__sleepIntervalSeconds):
                return;

    def Kill(self):
        self.__killEvent.set();
