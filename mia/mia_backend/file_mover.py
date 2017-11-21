""" includes """
import os
import queue
import subprocess
from shutil import copyfile

from mia_backend.raw_file import RawFile, RawFileException
from mia_backend.mia_db import MiaDB

class FileMover:
    """ Moves files from source to destination of type file_ext """
    def __init__(self, srcs, interim, dest, file_ext, readw_loc, flags, logger, database):
        """ Constructor for FileMover type
            end_file_ext is optional
        """
        self._source_dirs = srcs
        self._file_queue = queue.Queue()
        self._logger = logger
        self._interim = interim
        self._readw_loc = readw_loc
        self._flags = flags

        if database:
            self._database = MiaDB(database)
        else:
            self._database = None

        if not isinstance(self._source_dirs, list):
            if isinstance(self._source_dirs, str):
                self._source_dirs = [self._source_dirs]
            else:
                raise FileMoverException("Source directory must be a string or list of strings.")

        self._dest_dir = dest
        self._file_ext = file_ext

        self.check_dirs_exist()

        self._logger.info("File Mover Intialized")
        for source in self._source_dirs:
            self._logger.info("Source: {}".format(source))

        self._logger.info("Destination: {}".format(self._dest_dir))
        self._logger.info("Extension: {}".format(self._file_ext))

        files = self.get_files_by_ext()

        # fill file queue
        for file in files:
            self._file_queue.put_nowait(item=file)

    def files_left(self):
        """ indicates if there are still files left to move """
        return not self._file_queue.empty()

    def process_next_file(self):
        """ process the next file in the queue """
        # get file out of queue
        print("Proces_file")
        if not self._file_queue.empty():
            file = self._file_queue.get(block=True, timeout=None)
            try:
                self.copy_file(file.get_src(),
                            file.get_interim(),
                            file.get_src_filename(),
                            file.get_interim_filename(),
                            )

                self.parse_file(file)

                # clean up file
                try:
                    tmp = file.get_full_file_interim()
                    os.remove(tmp)
                except Exception as ex:
                    self._logger.error("Unable to remove temporary file: {} - {}".format(tmp, str(ex)))

            except Exception as ex:
                print("Failed to move file: {}".format(file))
                print("Exception: {}".format(str(ex)))
            #self.parse_file(file)


    def parse_file(self, file): #src, dst, dst_filename):
        """ parse a file with the given command """
        # for readw
        #command = "{} {} {} {}".format(self._readw_loc, ' '.join(self._flags), src, dst)
        print("parse file")
        if file:
            src = file.get_full_file_interim()
            dst = file.get_dest()
            dst_filename = file.get_full_file_dest()

            try:
                self.create_dirs(dst)
                command = "{} {} {} {}".format(self._readw_loc, self._flags, dst_filename, src)
                subprocess.call(command, shell=True)
                #insert into database
                self._database.insert(file)
            except Exception as ex:
                self._logger.error("Unable to convert file: {} - {}".format(src, str(ex)))



    def create_dirs(self, dirs):
        if not self.check_dir_exists(dirs):
            os.makedirs(dirs)

        os.chmod(dirs, 666)

    def copy_file(self, src, dst, src_filename, dst_filename):
        """ copy file to new destination """
        if not self.check_dir_exists(dst):
            os.makedirs(dst)

        os.chmod(dst, 666)
        copyfile(os.path.join(src, src_filename), os.path.join(dst, dst_filename))


    def get_files_by_ext(self):
        """ gets a list of files from a directory by extension 'ext'.
            Returns a list File type objects
        """
        good_files = []
        ext_re = self._file_ext

        if not ext_re.startswith('.'):
            ext_re = '.' + ext_re

        for src in self._source_dirs:
            directory_files = [f for f in os.walk(src)]
            for directory_tuple in directory_files:
                for file in directory_tuple[2]:
                    if file.endswith(ext_re):
                        # if the file has the extension, add to good_file list which is a tuple of
                        # (current directory, destination directory)
                        try:
                            good_file = RawFile(src, directory_tuple[0], file,
                                                self._interim, self._dest_dir)
                            good_files.append(good_file)
                            #good_files.append((file, os.path.join(directory_tuple[0], file)))
                        except RawFileException as ex:
                            self._logger.error(str(ex))

        return good_files

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

class FileMoverException(Exception):
    """ Custom Exception for FileMover Class """
    def __init__(self, message):
        """ Constructor """
        self._msg = message

    def __str__(self):
        """ to string """
        return repr(self._msg)
