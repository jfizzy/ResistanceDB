import os
import time
from ez_logger import EZLogger
from file_mover import FileMover, FileMoverException
from fileparser import FileParser, FileParserException
from config import Config

class MiaManager():
    """
        Main backend driver class for the Mia application - interfaces with gui and backend components
    """
    def __init__(self, parent):
        self.parent = parent
        self.parent.update_status("Initialized!")

