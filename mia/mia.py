import os
import shutil
from file_mover import FileMover
from fileparser import FileParser
from config import Config

def main():
    """ main loop for mia program """
    confg = Config(".miaconfig")
    print(confg)
    mover = FileMover(confg.SRC_DIRS, confg.INTERIM, confg.FILE_EXT, None)
    mover.move_files()
    
    parser = FileParser(confg.INTERIM, confg.DST_DIR, confg.FILE_EXT, "mzXML", confg.CONVERTER, confg.CONVERTER_FLAGS)
    parser.do_action()


if __name__ == "__main__":
    main()