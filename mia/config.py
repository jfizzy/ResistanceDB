import re, os

class Config:

    SRC_DIRS = []
    DST_DIR = None
    CONVERTER = None
    CONVERTER_FLAGS = []
    INTERIM = None

    def __init__(self, cfgfile):
        self.cfgfile = cfgfile

    def read_config(self):
        with open(self.cfgfile) as f:
            lines = f.readlines()
        if lines:
            for line in lines:
                print(line)
                line.strip()
                if '#' in line:
                    line = line.split('#')[0].strip()
                if re.match('^$', line):
                    # empty line
                    print('empty line : ['+line.split('\n')[0]+']')
                elif re.match('^SRC_DIR=((?:[\w]\:|\\\\)(\\\\[a-z_\-\s0-9\.]+)+|(.+)/([^/]+))$', line):
                    # source directory line (can have several)
                    self.add_source_dir(line.split('=')[1])
                elif re.match('^DST_DIR=((?:[\w]\:|\\\\)(\\\\[a-z_\-\s0-9\.]+)+|(.+)/([^/]+))$', line):
                    # destination directory line
                    self.set_destination_dir(line.split('=')[1])
                elif re.match('^CONVERTER=((?:[\w]\:|\\\\)(\\\\[a-z_\-\s0-9\.]+)+|(.+)/([^/]+))$', line):
                    # converter program executable location
                    self.set_converter_loc(line.split('=')[1])
                elif re.match('^CONVERTER_FLAGS=((\-)+[a-zA-Z]+( (\-)+[a-zA-Z]+)*)$', line):
                    #converter execution flag parameters
                    self.set_converter_args(line.split('=')[1])
                elif re.match('^INTERIM=((?:[\w]\:|\\\\)(\\\\[a-z_\-\s0-9\.]+)+|(.+)/([^/]+))$', line):
                    # temporary folder
                    self.set_interim_dir(line.split('=')[1])
                    

    def add_source_dir(self, line):
        print('>>>'+line)
        if os.path.isdir(line):
            print('found a source dir')
            self.SRC_DIRS.append(line)
            return
        print('directory given could not be resolved')

    def set_destination_dir(self, line):
        print('>>>'+line)
        if os.path.isdir(line):
            print('found the dest dir')
            self.DST_DIR = line
            return
        print('dest dir could not be resolved')

    def set_converter_loc(self, line):
        print('>>>'+line)
        if os.path.isfile(line):
            print('found the converter executable')
            self.CONVERTER = line
            return
        print('could not resolve the converter executable location')

    def set_converter_args(self, line):
        print('>>>'+line)
        args = line.split(' ')
        for arg in args:
            self.CONVERTER_FLAGS.append(arg)
        print('added converter arguments')

    def set_interim_dir(self, line):
        print('>>>'+line)
        if os.path.isdir(line):
            print('found the interim directory')
            self.INTERIM = line
            return
        print('could not resolve the interim directory')