#!/usr/bin/env python3.6
from leo.peakparser import peakparser
from leo.config import config
import unittest

def main():
    #tests = unittest.TestLoader().discover('tests')
    #unittest.TextTestRunner(verbosity=2).run(tests)
    #fr = FileReader("element_weights.csv")
    pp = peakparser.PeakParser()
    peaks = pp.parse_peaks_file("files/peaks/peaks.tab")
    if peaks:
        print("Sample peak: ")
        print(peaks[0])
    pp.write_peaks_csv(peaks, "test.csv")
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
