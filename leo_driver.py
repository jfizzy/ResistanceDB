#!/usr/bin/env python3.6
from leo.peakparser import peakparser
from leo.config import config
import unittest

def main():
    pp = peakparser.PeakParser()
    peaks = pp.parse_peaks_file("files/peaks/peaks.tab")
    if peaks:
        print("Sample peak: ")
        print(peaks[0])
    pp.write_peaks_csv(peaks, "test.csv")
    pp.write_condensed_csv(peaks, "condensed.csv")

    unknown = pp.parse_peaks_file("files/peaks/unknown.tab")
    if(unknown):
        pp.write_condensed_csv(unknown, 'unknown.csv')
    else:
        print("bad read")

if __name__ == "__main__":
    main()
