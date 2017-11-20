import re, os

class Config:

    SRC_DIRS = []
    DST_DIR = None
    CONVERTER = None
    CONVERTER_FLAGS = []
    INTERIM = None
    FILE_EXT = None
    # time between runs
    # TODO: REMEMBER TO ADD A CHECK FOR THIS VARIABLE
    INTERVAL = 10

    def __init__(self, logfile):
        self.logger = logfile

    def cpy_config(self, config):
        """ copy constructor """
        if(config.logger):
            self.logger = config.logger

        self.SRC_DIRS= config.SRC_DIRS
        self.DST_DIR = config.DST_DIR
        self.CONVERTER = config.CONVERTER
        self.CONVERTER_FLAGS = config.CONVERTER_FLAGS
        self.INTERIM = config.INTERIM
        self.FILE_EXT = config.FILE_EXT
        self.INTERVAL = config.INTERVAL

    ## TODO check input
    def set_config(self, src_dirs, dst, converter, converter_flags, interim, file_ext, interval):
        """
            sets config values directly
        """
        self.SRC_DIRS= [src.strip() for src in src_dirs]
        self.DST_DIR = dst.strip()
        self.CONVERTER = converter.strip()
        self.CONVERTER_FLAGS = converter_flags.strip()
        self.INTERIM = interim.strip()
        self.FILE_EXT = file_ext.strip()
        self.INTERVAL = int(interval)

    def write_config(self, cfgfile):
        """
            writes config values to file in a readable format
        """
        try:
            with open(cfgfile, "w") as cfg:
                for src in self.SRC_DIRS:
                    cfg.write("SRC_DIR={}\n".format(src))
                    
                cfg.write("INTERIM={}\n".format(self.INTERIM))
                cfg.write("DST_DIR={}\n".format(self.DST_DIR))
                cfg.write("INTERVAL={}\n".format(self.INTERVAL))
                cfg.write("CONVERTER_FLAGS={}\n".format(self.CONVERTER_FLAGS))
                cfg.write("CONVERTER={}\n".format(self.CONVERTER))
                cfg.write("EXT={}\n".format(self.FILE_EXT))
        except:
            self.logger.error("Error writing config")

    def read_config(self, cfgfile):
        """
            reads config from a cfg file
        """
        with open(cfgfile) as f:
            lines = f.readlines()
        
        if lines:
            for line in lines:
                #self.logger.info(line)
                line = line.strip()
                if '#' in line:
                    line = line.split('#')[0].strip()
                if re.match('^$', line):
                    pass
                    # empty line
                elif re.match('^SRC_DIR=.+$', line):
                    self.add_source_dir(line.split('=')[1])
                elif re.match('^FILE_EXT=.+$', line):
                    self.add_file_ext(line.split('=')[1])
                elif re.match('^DST_DIR=.+$', line):
                    # destination directory line
                    self.set_destination_dir(line.split('=')[1])
                elif re.match('^CONVERTER=.+$', line):
                    # converter program executable location
                    self.set_converter_loc(line.split('=')[1])
                #elif re.match('^CONVERTER_FLAGS=((\-)+[a-zA-Z]+( (\-)+[a-zA-Z]+)*)$', line):
                elif re.match('^CONVERTER_FLAGS=.+$', line):
                    #converter execution flag parameters
                    self.set_converter_args(line.split('=')[1])
                elif re.match('^INTERIM=.+$', line):
                    # temporary folder
                    self.set_interim_dir(line.split('=')[1])
                elif re.match('^INTERVAL=[0-9]+$', line):
                    # temporary folder
                    self.set_interval(line.split('=')[1])
    def set_interval(self, line):
        self.logger.info(' Config >>> {}'.format(line))
        try: 
            val = int(line)
            self.INTERVAL = val
            self.logger.info(" Config >>> Set Interval to {} minutes.".format(val))
        except ValueError as ex:
            self.logger.warning(" Config >>> Did not set interval, found invalid value")

    def add_file_ext(self, line):
        self.logger.info(' Config >>>' + line)
        self.FILE_EXT = line

    def add_source_dir(self, line):
        self.logger.info(' Config >>>' + line)
        #line = line.replace('\\', '\\\\')
        #self.logger.info(line)
        if os.path.isdir(line):
            self.logger.info('found a source dir')
            self.SRC_DIRS.append(line)
            return
        self.logger.info('directory given could not be resolved')

    def set_destination_dir(self, line):
        self.logger.info(' Config >>>'+line)
        self.DST_DIR = line

    def set_converter_loc(self, line):
        self.logger.info(' Config >>>'+line)
        self.CONVERTER = line
        #return
        #self.logger.info('could not resolve the converter executable location')

    def set_converter_args(self, line):
        self.logger.info(' Config >>>'+line)
        args = line.split(' ')
        for arg in args:
            self.CONVERTER_FLAGS.append(arg)
        self.logger.info(' Config >>> added converter arguments')

    def set_interim_dir(self, line):
        self.logger.info(' Config >>>'+line)
        if os.path.isdir(line):
            self.logger.info(' Config >>> found the interim directory')
            self.INTERIM = line
            return
        self.logger.warning(' Config >>> could not resolve the interim directory')

    def __str__(self):
        """ to string method of config """
        msg = ""
        for source in self.SRC_DIRS:
            msg = msg + "Source Directory: {}\n".format(source)

        msg = msg + "Destination Directory: {}\n".format(self.DST_DIR)
        msg = msg + "Converter Location: {}\n".format(self.CONVERTER)
        msg = msg + "Converter Flags: {}\n".format(self.CONVERTER_FLAGS)
        msg = msg + "Interim Directory: {}\n".format(self.INTERIM)
        msg = msg + "File extension: {}\n".format(self.FILE_EXT) 
        msg = msg + "Running on interval of: {} minutes\n".format(self.INTERVAL)
        

        return str(msg)