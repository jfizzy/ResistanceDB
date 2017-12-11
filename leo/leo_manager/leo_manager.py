import os

from peakparser.peakparser import PeakParser
from peakparser.peak import Peak
from config.config import Config

class LeoManager():
    """ Manager interface for leo backend and GUI """
    def __init__(self, parent):
        """ """
        self._parent = parent

    def run_leo(self, config):
        """ """
        msg, valid = self.check_config(config)
        read_success = True
        write_success = True
        condense_success = True

        if not valid:
            self._parent.show_message(msg, "Invalid Config")
        else:
            peak_parser = PeakParser(config)
            msg = ""
            try:
                peaks = peak_parser.parse_peaks_file()
            except:
                msg += "Failed to open and parse peaks file. The file may be in use, or does not exist.\n"
                read_success = False
            
            if read_success and peaks:
                try:
                    peak_parser.write_peaks_csv(peaks)
                except:
                    write_success = False
                    msg += "Failed to write filtered peaks to file. The file may be in use.\n"

                if (config.CONDENSED_FILE):
                    try:
                        peak_parser.write_condensed_csv(peaks)
                    except:
                        condense_success = False
                        msg += "Failed to write condensed peaks to file. The file may be in use.\n"
                
                self._parent.finished_parse(msg, config, write_success, condense_success)
            else:
                self._parent.show_message(msg, "Failed to Load Peaks")


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
            
