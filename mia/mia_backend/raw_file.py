""" imports """
import os
from datetime import datetime

class RawFile():
    """ defines a single .raw file
        src: It's original name and location
        interim: It's interim directory
        dst_name: It's final destination
    """
    def __init__(self, root_src, src, file_name, interim, dst):
        """ """
        #the source that was specified in the config
        self._root_src = root_src
        #holds full source to file including file name
        self._src = src
        self._file_name = file_name
        
        self._creation_date = os.path.getctime(self._src)

        self._user = self.gen_user()

        if not interim:
            interim = os.getcwd()
            
        self._interim = self.gen_dir(interim)
        self._dst = self.gen_dir(dst)

        #gen_new_name uses both creation date and user, generate it last
        self._new_name = self.gen_new_name()

    def gen_user(self):
        """ get the user name from the subdirectories. Assumed to be the second parent directory of the file """
        split_src = self._src.rsplit("\\", 2)

        if len(split_src) > 1:
            usr = split_src[1].split("\\")
            if usr:
                return usr[0]

        return None

    def gen_new_name(self):
        """ get the new name of the file at destination directory. year_month_day_orig_name.raw """
        return datetime.fromtimestamp(self._creation_date).strftime("%Y_%m_%d_{}_".format(self._user)) + self._file_name

    def gen_dir(self, dir):
        """ get the new directory of the filename, includes subfolders found at source """
        subfolder = self._root_src.rsplit("\\", 1)

        if subfolder:
            orig_src = self._src.split(subfolder[1])
            new_dir = os.path.join(dir, subfolder[1])

            #remove leading slashes because os.path.join treats that as an absolute path
            if orig_src[1].startswith("\\"):
                orig_src[1] = orig_src[1][1:]

            new_dir = os.path.join(new_dir, orig_src[1])

            #new_name = self._dst + "\\" + new_name[1] + orig_src[1]

        return new_dir
        

    def get_full_file_src(self):
        """ returns the full path to the source including filename """
        return os.path.join(self._src, self._file_name)

    def get_full_file_dest(self):
        """ returns the full path to the destination including the new file name """
        return os.path.join(self._dst, self._new_name)

    def __str__(self):
        """ to string method """
        my_str = "File Name: {}\n".format(self._file_name)
        my_str += "Root Source: {}\n".format(self._root_src)
        my_str += "Source: {}\n".format(self._src)
        my_str += "Interim: {}\n".format(self._interim)
        my_str += "Destination: {}\n".format(self._dst)
        my_str += "New Name: {}\n".format(self._new_name)
        my_str += "Creation Date: {}\n".format(datetime.fromtimestamp(self._creation_date).strftime("%Y_%m_%d"))

        return str(my_str)

class RawFileException(Exception):
    """ simple custom exception to indicate RawFileException has occurred """
    def __init__(self, msg):
        """ init for RawFileException """
        Exception.__init__(self)
        self._msg = msg

    def __str__(self):
        """ overwrite tostr """
        return str(self._msg)