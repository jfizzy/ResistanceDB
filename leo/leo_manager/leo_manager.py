import os

from peakparser.peakparser import PeakParser
from peakparser.peak import Peak
from config.config import Config

class LeoManager():
    """ Manager interface for leo backend and GUI """
    def __init__(self, parent):
        """ """
        self._parent = parent

    def set_config(self, config):
        """ """
        msg, valid = self.check_config(config)
        if valid:
            print("valid!")
            pass
        else:
            print("invalid!!")
            self._parent.show_message(msg, "Invalid Config")

    def check_config(self, config):
        """ """
        msg = ""
        valid = True
        if not config.MZRATIO or config.MZRATIO < 0.0 or config.MZRATIO > 1.0:
            valid = False
            msg += "Invalid MZ ratio.\n"

        if not config.OUTPUT_FILE:
            valid = False
            msg += "Output file required.\n"

        if not config.PEAKS_FILE or not os.path.isfile(config.PEAKS_FILE):
            valid = False
            msg += "Peaks file unsupplied or does not exist.\n"

        if not config.MAXRTDIFF or config.MAXRTDIFF < 0:
            valid = False
            msg += "Rt diff must be > 0.\n"

        if not config.MINMZ or config.MINMZ < 0:
            valid = False
            msg += "Min MZ must be >= 0.\n"

        if msg:
            msg = "Config invalid:\n" + msg

        return msg, valid
            
