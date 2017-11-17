""" includes """
import os
import sys
import re
from glob import glob
import itertools

import mia_backend.fileutil

class FileMover:
    """ Moves files from source to destination of type file_ext """
    def __init__(self, src, dest, file_ext, end_file_ext, logger):
        """ Constructor for FileMover type 
            end_file_ext is optional
        """
        self._source_dirs = src
        self._logger = logger

        if not isinstance(self._source_dirs, list):
            if isinstance(self._source_dirs, str):
                self._source_dirs = [self._source_dirs]
            else:
                raise FileMoverException("Source directory must be a string or list of strings.")

        self._dest_dir = dest
        self._file_ext = file_ext

        if not end_file_ext:
            self._end_file_ext = file_ext
        else:
            self._end_file_ext = end_file_ext

        self.check_dirs_exist()

        self._logger.info("File Mover Intialized")
        for source in self._source_dirs:
            self._logger.info("Source: {}".format(source))

        self._logger.info("Destination: {}".format(self._dest_dir))
        self._logger.info("Extension: {}".format(self._file_ext))

    def check_dirs_exist(self):
        """ checks if the directories passed in on object creation are valid """
        for source in self._source_dirs:
            if not self.check_dir_exists(source):
                raise FileMoverException("Specified destination directory: '{}' does not exist."\
                    .format(self._dest_dir))

        if not self.check_dir_exists(self._dest_dir):
            raise FileMoverException("Specified destination directory: '{}' does not exist."\
                .format(self._dest_dir))

    def check_dir_exists(self, path):
        """ checks if a single directory exists and is a directory """
        if os.path.exists(path):
            if os.path.isdir(path):
                return True

        return False

    def move_files(self):
        """ does file move """

        if self._source_dirs:
            self._logger.info(">>> FileMover: moving files from {} director{}".format(len(self._source_dirs), \
                'ies' if len(self._source_dirs) > 1 else 'y'))

        for source in self._source_dirs:
            self._logger.info(">>> Directory: {}".format(source))
            #os.walk returns a list of 3-tuples in the form (directory, [directories in directory], [files in directory])
            good_files = fileutil.get_files_by_ext(source, self._dest_dir, self._file_ext, self._end_file_ext)

            #print(good_files)
            for f in good_files:
                self._logger.info(">>> Moving {} -> {}".format(f[0], f[1]))
                os.rename(f[0], f[1])

        self._logger.info(">>> FileMover done move.\n")


class FileMoverException(Exception):
    """ Custom Exception for FileMover Class """
    def __init__(self, message):
        """ Constructor """
        self._msg = message

    def __str__(self):
        """ to string """
        return repr(self._msg)
