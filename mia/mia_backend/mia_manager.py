""" imports """
from enum import Enum
import threading
import os
import queue
from mia_backend.ez_logger import EZLogger
from mia_backend.file_mover import FileMover, FileMoverException
#from mia_backend.fileparser import FileParser, FileParserException
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
        Main backend driver class for the Mia application -
        nterfaces with gui and backend components
    """
    LOG_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)), "mia_log.log")
    CONFIG = os.path.join(os.path.abspath(os.path.dirname(__file__)), ".miaconfig")
    
    def __init__(self, parent):
        print(self.LOG_FILE)
        print(self.CONFIG)
        self._db_lock = threading.Lock()
        self._parent = parent
        self._logger = EZLogger(logger_name="MiaLogger",
                                log_filename=self.LOG_FILE,
                                filesize=10*1024*1024, backupCount=5,
                                filemode='w')
        self._config = Config(self._logger)
        self._config.read_config(self.CONFIG)

        #if self._config.
        self._parent.update_status("Initialized!")
        self._config_lock = threading.Lock()
        self._work_queue = queue.Queue()
        self._running = False
        self._worker_thread = threading.Thread(None, self.run, "worker_thread", {}, {})
        self._worker_thread.start()
        self._transfer_thread = None
        self._max_threads = 5

    def get_worker(self):
        """ get the worker thread """
        return self._worker_thread

    def get_config(self):
        """ get configuration settings """
        return self._config

    def start(self, config, callback):
        """ starts mia 
            callback passed by caller, mia will call this callback on successfull execution
        """        
        if not self._running and (config is None or self.check_config(config)):
            try:
                # file mover will throw exception if directories are not found
                # file_mover = FileMover(config.SRC_DIRS, config.INTERIM,
                # config.FILE_EXT, None, self._logger)
                # file_mover.move_files()
                if config:
                    self._config_lock.acquire()

                    self._config.cpy_config(config)
                    self._config.write_config(self.CONFIG)

                    self._config_lock.release()
                    self._parent.update_status("Config valid. Starting Mia!")

                print(str(self._config))

                self._work_queue.put(Instruction.START)
                if callback:
                    callback()
            except FileMoverException as ex:
                self._parent.update_status(ex)
        else:
            self._parent.update_status("Mia is already running.")

    def transfer(self):
        """ handles file transfer and file parsing
            Creates a FileMover object to handle file moving, if there are files left to move
            and we have not received the quit signal, then grab a file and perform transfer.

            If we have not receieved quit signal at the end of the transfer, reset the interval to
            do work again.
        """

        print("in transfer...")
        self._config_lock.acquire()
        print("got lock")
        file_mover = FileMover(self._config.SRC_DIRS,
                               self._config.INTERIM,
                               self._config.DST_DIR,
                               self._config.FILE_EXT,
                               self._config.CONVERTER,
                               self._config.CONVERTER_FLAGS,
                               self._logger,
                               self._config.DATABASE,
                               self._db_lock)

        print("file mover made")
        #number of threads is max_threads if threaded, otherwise 1 (synchronous)
        num_threads = self._max_threads if self._config.THREADED else 1

        self._config_lock.release()        
        threads = []
        
        #file_movers = file_mover.FileMover(src, self._config.DST_DIR, self._config.FILE_EXT, None
        #self._transfer_thread = threading.Timer(0, self.do_transfer, {}, {})

        # while we are still running and have files to move
        while self._running and file_mover.files_left():
            print("parsing a file")
            if self._config.THREADED:
                for i in range(0, num_threads):
                    if file_mover.files_left() and self._running:
                        threads.append(threading.Thread(None, file_mover.process_next_file, "thread_{}".format(i), {None}, {}))
                        threads[i].start()

                for i in range(0, len(threads)):
                    if threads[i]:
                        threads[i].join()

                threads.clear()
            else:
                print("Non-threaded")
                file_mover.process_next_file(lambda x : self._parent.update_status_bar())#"Processing: {}".format(x.get_full_file_src())))
                print("Exitting...")

                                #(lambda x : self._parent.update_status("Processing file {}".format(x.get_full_file_src())),))
                #file_mover.process_next_file(lambda x : self._parent.update_status("Processing file {}".format(x.get_full_file_src())))

        # if still running at end of file, reset interval to do another move
        if self._running:
            self._parent.update_status("Finished parsing raw files. Waiting {} minutes to check again.".format(self._config.INTERVAL))
            self._parent.update_status_bar("Running... waiting to transfer files.")
            self._transfer_thread = threading.Timer(self._config.INTERVAL * 60, self.transfer, {}, {})
            self._transfer_thread.start()

    def run(self):
        """ handles the actual running of mia """
        instruction = self._work_queue.get(block=True, timeout=None)   
        while instruction != Instruction.SHUTDOWN:
            self.parse_instruction(instruction) 
            print("parsed instruction {}".format(instruction))
            instruction = self._work_queue.get(block=True, timeout=None)

        self._running = False
        print("Received shutdown signal")

    def stop(self, callback):
        """ GUI is requesting mia shut down """
        self._work_queue.put(Instruction.QUIT, block=True, timeout=None)

        self._parent.update_status("Quit signal received, waiting for mia to finish processes...")
        self._parent.mia_stopping()

        if self._transfer_thread and self._transfer_thread.is_alive():
            self._transfer_thread.join()

        self._parent.update_status("Mia has stopped transfers.")
        if callback:
            callback()

    def shutdown(self):
        """ shuts down all worker and timer threads, informs parent when threads have joined """
        self._work_queue.put(Instruction.QUIT, block=True, timeout=None)
        self._work_queue.put(Instruction.SHUTDOWN, block=True, timeout=None)
        self._parent.update_status("Shutdown signal received, waiting for mia to finish processes...")

        self._parent.mia_stopping()

        if self._transfer_thread and self._transfer_thread.is_alive():
            print("Waiting on transfer thread?")
            print(self._transfer_thread)
            self._transfer_thread.join()
            print("Transfer joined")

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
            if self._transfer_thread:
                self._transfer_thread.cancel()
            print("quit!")

    def check_config(self, config):
        """ checks that mia has received the default minimum valid arguments for config """
        valid = True

        if not config.DATABASE or config.DATABASE == '':
            self._parent.update_status(\
                "Error detected in config: No Database Selected")
            valid = False

        if not config.SRC_DIRS:
            self._parent.update_status(\
                "Error detected in config: No Source Directories")
            valid = False

        if not config.DST_DIR or config.DST_DIR == '':
            self._parent.update_status(\
                "Error detected in config: No Destination Directory")
            valid = False

        if not config.CONVERTER or config.CONVERTER == '':
            self._parent.update_status(\
                "Error detected in config: ReAdW.exe path not set")
            valid = False

        if not config.INTERIM or config.INTERIM == '':
            self._parent.update_status(\
                "Error detected in config: No Interim Directory"
            )
            valid = False

        return valid