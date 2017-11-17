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
    LOG_FILE = 'mia_backend/.miaconfig'
    
    def __init__(self, parent):
        self._parent = parent
        self._logger = EZLogger(logger_name="MiaLogger", log_filename="mia_log.log", filesize=10*1024*1024, backupCount=5, filemode='w')
        self._config = Config(self._logger)
        self._config.read_config(self.LOG_FILE)
        self._parent.update_status("Initialized!")

    def get_config(self):
        return self._config

    def start(self, config):
        """ """
        if (self.checkConfig(config)):
            self._config.cpy_config(config)
            self._config.write_config(self.LOG_FILE)
            self._parent.update_status("Config valid. Starting Mia!")
            self._parent.mia_starting()

    def checkConfig(self, config):
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