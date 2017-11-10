""" includes """
import os
import sys
import re
from glob import glob
import fileutil
import itertools

def eprint(*args, **kwargs):
    """ error print """
    print(*args, file=sys.stderr, **kwargs)

class FileMover:
    """ Moves files from source to destination of type file_ext """
    def __init__(self, src, dest, file_ext, end_file_ext):
        """ Constructor for FileMover type 
            end_file_ext is optional
        """
        self._source_dirs = src

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

        print("File Mover Intialized")
        for source in self._source_dirs:
            print("Source: {}".format(source))

        print("Destination: {}".format(self._dest_dir))
        print("Extension: {}".format(self._file_ext))

    def check_dirs_exist(self):
        """ checks if the directories passed in on object creation are valid """
        print("checking source dirs")
        for source in self._source_dirs:
            if not self.check_dir_exists(source):
                eprint("Specified source directory: '{}' does not exist.".format(source))
                raise FileMoverException("Specified destination directory: '{}' does not exist."\
                    .format(self._dest_dir))

        print("checking dest dir")
        if not self.check_dir_exists(self._dest_dir):
            eprint("Specified destination directory: '{}' does not exist.".format(self._dest_dir))
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
            print()
            print(">>> FileMover: moving files from {} director{}".format(len(self._source_dirs), \
                'ies' if len(self._source_dirs) > 1 else 'y'))

        for source in self._source_dirs:
            print(">>> Directory: {}".format(source))
            #os.walk returns a list of 3-tuples in the form (directory, [directories in directory], [files in directory])
            '''
            directory_files = [f for f in os.walk(source)]
            good_files = []
            for directory_tuple in directory_files:
                for f in directory_tuple[2]:
                    if re.findall(self._file_ext, f):
                        # if the file has the extension, add to good_file list which is a tuple of (current directory, destination directory)
                        good_files.append((os.path.join(directory_tuple[0], f), os.path.join(self._dest_dir, f)))
            '''
            good_files = fileutil.get_files_by_ext(source, self._dest_dir, self._file_ext, self._end_file_ext)

            #print(good_files)
            for f in good_files:
                print(">>> Moving {} -> {}".format(f[0], f[1]))
                os.rename(f[0], f[1])

        print(">>> FileMover done move.\n")


class FileMoverException(Exception):
    """ Custom Exception for FileMover Class """
    def __init__(self, message):
        """ Constructor """
        self._msg = message

    def __str__(self):
        """ to string """
        return repr(self._msg)
