""" imports """
from enum import Enum
import threading
import time
import queue
from mia_backend.ez_logger import EZLogger
from mia_backend.file_mover import FileMover, FileMoverException
from mia_backend.fileparser import FileParser, FileParserException
from mia_backend.config import Config

class Instruction(Enum):
    """ defines an enum for mia instruction set """
    START = 1
    UPDATE_CONFIG = 2
    UPDATE_INTERVAL = 3
    QUIT = 4
    SHUTDOWN = 5

class MiaManager():
    """
        Main backend driver class for the Mia application - interfaces with gui and backend components
    """
    LOG_FILE = 'mia_backend/.miaconfig'

    
    def __init__(self, parent):
        self._parent = parent
        self._logger = EZLogger(logger_name="MiaLogger",
                                log_filename="mia_log.log",
                                filesize=10*1024*1024, backupCount=5,
                                filemode='w')
        self._config = Config(self._logger)
        self._config.read_config(self.LOG_FILE)
        self._parent.update_status("Initialized!")
        self._work_queue = queue.Queue()
        self._running = False
        self._worker_thread = threading.Thread(None, self.run, "worker_thread", {}, {})
        self._worker_thread.start()
        self._transfer_thread = None

    def get_worker_thread(self):
        """ gets the worker thread """
        return self._worker_thread

    def get_config(self):
        """ get configuration settings """
        return self._config

    def start(self, config):
        """ starts mia """        
        if self.check_config(config):
            try:
                # file mover will throw exception if directories are not found
                # file_mover = FileMover(config.SRC_DIRS, config.INTERIM,
                # config.FILE_EXT, None, self._logger)
                # file_mover.move_files()
                self._config.cpy_config(config)
                self._config.write_config(self.LOG_FILE)
                self._parent.update_status("Config valid. Starting Mia!")
                self._parent.mia_starting()
                self._work_queue.put(Instruction.START)
            except FileMoverException as ex:
                self._parent.update_status(ex)

    def transfer(self):
        """ """

        #file_movers = file_mover.FileMover(src, self._config.DST_DIR, self._config.FILE_EXT, None
        #self._transfer_thread = threading.Timer(0, self.do_transfer, {}, {})

        #reset timer to do work again, this time using interval
        if self._running:
            self._transfer_thread = threading.Timer(self._config.INTERVAL, self.transfer, {}, {})

    def do_transfer(self):
        """ do a single file move """

    def run(self):
        """ handles the actual running of mia """
        instruction = self._work_queue.get(block=True, timeout=None)   
        while instruction != Instruction.SHUTDOWN:
            self.parse_instruction(instruction) 
            print("parsed instruction {}".format(instruction))
            instruction = self._work_queue.get(block=True, timeout=None)

        print("Received shutdown signal")

    def stop(self):
        """ GUI is requesting mia shut down """
        self._work_queue.put(Instruction.QUIT, block=True, timeout=None)
        if self._transfer_thread.is_alive():
            self._transfer_thread.join()

        self._parent.update_status("Mia has stopped transfers.")
        self._parent.mia_stopped()

    def shutdown(self):
        """ shuts down all worker and timer threads, informs parent when threads have joined """
        self._work_queue.put(Instruction.SHUTDOWN, block=True, timeout=None)
        self._parent.update_status("Shutdown signal received, waiting for mia to finish processes...")
        if self._transfer_thread.is_alive():
            self._transfer_thread.join()
        self._worker_thread.join()
        self._parent.update_status("Mia has shut down.")

    def parse_instruction(self, instruct):
        """
        """
        if instruct == Instruction.START:
            print("start!")
            #immediatelys tart transfer, wait time of 0 milliseconds
            self._running = True
            self._transfer_thread = threading.Timer(0, self.transfer, {}, {})
            self._transfer_thread.start()
        elif instruct == Instruction.UPDATE_CONFIG:
            print("update config!")
        elif instruct == Instruction.UPDATE_INTERVAL:
            print("update interval!")
        elif instruct == Instruction.QUIT:
            self._running = False
            self._transfer_thread.cancel()
            print("quit!")

    def check_config(self, config):
        """ checks that mia has received the default minimum valid arguments for config """
        valid = True

        if not config.SRC_DIRS:
            self._parent.update_status(\
                "Error detected in config: No Source Directories")
            valid = False

        if not config.DST_DIR:
            self._parent.update_status(\
                "Error detected in config: No Destination Directory")
            valid = False

        if not config.CONVERTER:
            self._parent.update_status(\
                "Error detected in config: ReAdW.exe path not set")
            valid = False

        return valid