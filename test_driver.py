#!/usr/bin/env python3.6
from leo.fileparser import fileparser
from leo.config import config
import unittest

def main():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    #fr = FileReader("element_weights.csv")
    #fp = fileparser.FileParser()
    #peaks = fp.parse_peaks_file("files/peaks/peaks_wknown.tab")
    #fp.write_peaks_csv(peaks, "test.csv")
    #filename = "../../files/known_markers/2017_05_10RG_HILIC15-Neg_MSMLS-List.csv"
    #fr.parseKM(filename)

    # config stuff
    #cfg = config.Config()
    #cfg.read_config() 
    #print(cfg.MINMZ) 
    #print(cfg.COMPOUNDSFILE)
    #print(cfg.MAXRTDIFF)
    #print(cfg.MZDIFF)
if __name__ == "__main__":
    main()
