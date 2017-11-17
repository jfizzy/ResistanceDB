import os
import time
from mia_backend.ez_logger import EZLogger
from mia_backend.file_mover import FileMover, FileMoverException
from mia_backend.fileparser import FileParser, FileParserException
from mia_backend.config import Config

class MiaManager():
    """
        Main backend driver class for the Mia application - interfaces with gui and backend components
    """

    def __init__(self, parent):
        self._parent = parent
        self._logger = EZLogger(logger_name="MiaLogger", log_filename="mia_log.log", filesize=10*1024*1024, backupCount=5, filemode='w')
        self._config = Config(self._logger)
        self._parent.update_status("Initialized!")