import os
import fileutil
import subprocess

class FileParser:
    """ applies some file permuting action to a directory of files
    
        performs the action in format [action] [flags] [src file] [dest file]
     """

    def __init__(self, src, dest, file_ext, end_ext, action, flags, logger):
        """ constructor
            src: Directory where files are
            dest: Directory to store results
            file_ext: extension of file to apply action to
            end_ext: extension of output file
            action: program to be applied to files found in source
            flags: flags for action
         """

        self._src_dir = src
        self._dst_dir = dest
        self._file_ext = file_ext
        self._end_ext = end_ext
        self._action = action
        self._flags = flags
        self._logger = logger

        #assumed to be a program 
        self._action = action

        #if not os.path.exists(self._action):
        #    raise FileParserException("Action file not found.")
    
        self._logger.info("FileParser initialized with arguments:")
        self._logger.info(self)

    def do_action(self):
        ''' '''
        good_files = fileutil.get_files_by_ext(self._src_dir, self._dst_dir, self._file_ext, self._end_ext)

        for file in good_files:
            command = "{} {} {} {}".format(self._action, file[0], file[1], ' '.join(self._flags))
            self._logger.info("Running command: {}".format(command))
            result = subprocess.call(command, shell=True)

    def __str__(self):
        msg = ""

        msg = msg + "Source Directory: {}\n".format(self._src_dir)
        msg = msg + "End Destination: {}\n".format(self._dst_dir)
        msg = msg + "Start extension: {}\n".format(self._file_ext)
        msg = msg + "End extension: {}\n".format(self._end_ext)
        msg = msg + "Action: {}\n".format(self._action)
        msg = msg + "Flags: {}\n".format(self._flags)

        return str(msg)



class FileParserException(Exception):
    def __init__(self, msg):
        """ constructor """
        self._msg = msg

    def __str__(self):
        return str(self._msg)