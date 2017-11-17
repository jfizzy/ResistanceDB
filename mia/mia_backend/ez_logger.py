import time
import datetime
import logging
import logging.handlers

class EZLogger:
    def __init__(self, logger_name, log_filename, filesize, backupCount, filemode):
        self._log_name = logger_name
        self._log_filename = log_filename
        self._filesize = filesize
        self._backupCount = backupCount

        self._logger = logging.getLogger(self._log_name) 
        self._logger.setLevel(logging.DEBUG)

        handler = logging.handlers.RotatingFileHandler(\
            self._log_filename, maxBytes=self._filesize, backupCount=self._backupCount)

        self._logger.addHandler(handler)

    def debug(self, msg, *args, **kwargs):
        """ logs a debug messaege to the log file """
        self._logger.debug(self.set_timestamp("DEBUG: {}".format(msg)), *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        """ logs an info message to the log file """
        self._logger.info(self.set_timestamp("INFO: {}".format(msg)), *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        """ logs a warning message to the log file """
        self._logger.warning(self.set_timestamp("WARNING: {}".format(msg)), *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        """ logs an error message to the log file """
        self._logger.error(self.set_timestamp("ERROR: {}".format(msg)), *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        """ logs a critical message to the log file """
        self._logger.critical(self.set_timestamp("CRITICAL: {}".format(msg)), *args, **kwargs)

    def set_timestamp(self, msg):
        """ prepends a timestamp to the message """
        stamp = time.time()
        formatted = st = datetime.datetime.fromtimestamp(stamp).strftime('%Y-%m-%d %H:%M:%S - ')
        return "{}{}".format(formatted, msg)

