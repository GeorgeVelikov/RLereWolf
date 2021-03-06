import threading;
import traceback;

# Heavily inspired from https://stackoverflow.com/a/325528
class KillableThread(threading.Thread):
    def __init__(self, func, sleepIntervalSeconds = 1):
        super().__init__();
        self.__func = func;
        self.__killEvent = threading.Event();
        self.__sleepIntervalSeconds = sleepIntervalSeconds;

        self.setDaemon(True);

    #override
    def run(self):
        try:
            while True:
                self.__func();

                # If no kill signal is set, sleep for the interval,
                # If kill signal comes in while sleeping, immediately
                # wake up and handle
                if self.__killEvent.wait(self.__sleepIntervalSeconds):
                    return;
        except Exception as error:
            trace = traceback.format_exc();

            # Log this somewhere for the user?
            print(str(error) + "\n\n" + trace);

        return;

    def Kill(self):
        self.__killEvent.set();
