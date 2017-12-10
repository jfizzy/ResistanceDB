import re, os
from decimal import Decimal

class Config:
    """ config class for  """
    PEAKS_FILE = ''
    OUTPUT_FILE = ''
    CONDENSED_FILE = ''
    MINMZ = 0
    MAXRTDIFF = 0.0
    MZRATIO = 0.3

    def __init__(self, cfgfile):
        """ """
        self.cfgfile = cfgfile

    def read_config(self):
        with open(self.cfgfile) as f:
            lines = f.readlines()
        if lines:
            for line in lines:
                line.strip()
                if '#' in line:
                    line = line.split('#')[0].strip()
                if re.match('^$', line):
                    # empty line
                    #print('empty line: ['+line.split('\n')[0]+']')
                    pass
                elif re.match('^COMPOUNDS=[a-zA-Z09_]+.[a-z]+$', line):    
                    # compounds filename line
                    #print('compounds line: ['+line.split('\n')[0]+']')
                    self.set_compounds_file(line.split('=')[1].split('\n')[0])
                elif re.match('^MINMZ=[0-9]+(.[0-9]+)?e[0-9]+$', line):
                    # Minimum intensity
                    #print('min intensity line: ['+line.split('\n')[0]+']')
                    self.set_minmz(line.split('=')[1].split('\n')[0])
                elif re.match('^MAXRTDIFF=[0-9]+.[0-9]+$', line):
                    # maximum Retention time differential
                    #print('rt differential line: ['+line.split('\n')[0]+']')
                    self.set_maxrtdiff(line.split('=')[1].split('\n')[0])
                elif re.match('^MZRATIO=((0.[0-9]+)|0|1)$', line):
                    # intensity ratio
                    #print('intensity differential line: ['+line.split('\n')[0]+']')
                    self.set_mzratio(line.split('=')[1].split('\n')[0])
                else:
                    #invalid line
                    #print('invalid line: ['+line.split('\n')[0]+']')
                    pass

    def set_compounds_file(self, line):
        # TODO we need to check for the file in a relative location
        if os.path.isfile(line):
            print('compounds file exists')
            self.PEAKS_FILE = line
            return
        print('compounds file not found')

    def set_minmz(self, line):
       self.MINMZ = self.format_e(float(line))
       print('set minmz to {}'.format(self.MINMZ))

    def set_maxrtdiff(self, line):
        self.MAXRTDIFF = float(line)
        print('set maxrtdiff to {}'.format(self.MAXRTDIFF))

    def set_mzratio(self, line):
        self.MZRATIO= float(line)
        print('set mzratio to {}'.format(self.MZRATIO))

    def format_e(self, n):
        a = '%E' % n
        return a.split('E')[0].rstrip('0').rstrip('.') + 'E' + a.split('E')[1]
