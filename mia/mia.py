from ez_logger import EZLogger
import os
from file_mover import FileMover, FileMoverException
from fileparser import FileParser, FileParserException
from config import Config
import time

logger = EZLogger(logger_name="MiaLogger", log_filename="mia_log.log", filesize=10*1024*1024, backupCount=5, filemode='w')
config = Config(".miaconfig", logger)

def checkConfig(config):
    """ checks that mia has received the default minimum valid arguments for config """
    valid = True

    if not config.SRC_DIRS:
        logger.error("input configuration file has no Source Directories.\n"\
            + "Please ensure there is at least one line like:\n"\
            + "SRC_DIR=Full/Path/To/Source/Directory")
        valid = False

    if not config.DST_DIR:
        logger.error("input configuration file has no destination directory.\n"\
            + "Please ensure there is a line like:\n"\
            + "DST_DIR=Full/Path/To/Destination/Directory")
        valid = False

    if not config.FILE_EXT:
        logger.error("input configuration file has no file extension set."\
            + "Please ensure there is a line like:\n"\
            + "FILE_EXT=ext\nWhere 'ext' is the extension name of the files to move")
        valid = False

    if not config.CONVERTER:
        logger.error("input configuration file has no Converter location set."\
            + "Please ensure there is a line like:\n"\
            + "CONVERTER=Full/Path/To/ReAdW.exe")
        valid = False

    return valid

def do_work():
    try: 
        mover = FileMover(config.SRC_DIRS, config.INTERIM, config.FILE_EXT, None, logger)
        mover.move_files()
    
        parser = FileParser(config.INTERIM, config.DST_DIR, config.FILE_EXT, "mzXML", config.CONVERTER, config.CONVERTER_FLAGS, logger)
        parser.do_action()
    except FileMoverException as ex:
        logger.error(ex)
    except FileParserException as ex:
        logger.error(ex)


def main():
    """ main loop for mia program """
    if not checkConfig(config):
        exit(0)

    logger.info("Mia starting up. Initializing with config parameters:\n{}".format(config))

    try:
        while True:
            do_work()
            time.sleep(config.INTERVAL)
    except Exception as ex:
        logger.critical("Mia has exited with error: {} ".format(ex))

    logger.info("Exitting.")
    
if __name__ == "__main__":
    main()