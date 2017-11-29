""" imports """
import time
import datetime
import threading
import sys
from mia_backend.mia_manager import MiaManager

class MiaHandler():
    def __init__(self):
        """ init """

    def set_mia(self, mia):
        self._mia = mia

    """def signal_handler(self, signal, frame):
        print('You pressed Ctrl+C!')
        self._mia.stop(None)
        if self._mia.get_worker.isAlive():
            self._mia.get_worker.join()

        sys.exit(0)"""

    def update_status(self, msg):
        """ handles update 
        messages from mia manager """
        msg = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S - ') + msg
        print(msg)

    def update_status_bar(self, msg):
        """ stub to handle message bar status updates from the manager to the gui, no gui so redirect to update_status"""
        self.update_status(msg)


def started():
    """ mia will call this once she's started up, put code here to handle the event """
    print("started")

def main():
    """ start mia with config file, if mia fails to start, wait 10 minutes and try again. """
    handler = MiaHandler()
    print("Registered signal...")
    try:
        #handler will handle Mia callbacks
        #create mia
        mia = MiaManager(handler)
        handler.set_mia(mia)

        #start mia
        mia.start(None, started)

    except KeyboardInterrupt as ex:
        if mia:
            mia.stop(None)
        # Need to handle the control C evennt here 
    except Exception as ex:
        print("Exploding: {}".format(str(ex)))
        print("Trying to start up again")
        time.sleep(60*10)

if __name__ == "__main__":
    main()
    while not __miaexit__:
        time.sleep(5)

   
