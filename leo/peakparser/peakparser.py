''' packages '''
#import traceback
#import sys
import csv
import re
from leo.peaks import peak as peak_module

class PeakParser:
    """ Reads in a list of peaks generated by MAVEN and removes excess unecessary data """

    def __init__(self):
        """ Constructor for filereader"""
        self.DATA_OFFSET = 24
        self._intensities = {}
        self._colnames = {}

    # parse a peaks file
    #   fields we are interested in (0 aligned):
    #   4: medMz
    #   5: medRt
    #   8: compound
    #   9: compound ID (usually same as compound)
    #   10: category
    #   12: expectedRtDiff, different betwene found RT and medRt
    #   14: parent
    #   15-24: not used
    #   24+ mzXML peak data (column name might be of interest)
    def parse_peaks_file(self, filename):
        """ Parse a given peaks file assumed to be tabbed delimited """

        try:
            with open(filename, 'rt') as csvfile:
                reader = csv.reader(csvfile, delimiter='\t')

                #to hold the peak data
                peaks = []

                # headers - might be important later
                # they are the name of the mzXML sample file
                row = reader.__next__()
                col_names = [str(s).lower() for s in row[self.DATA_OFFSET:] if s != ""]

                # store column names in format {index: (name, time)}
                # note that index is an offset into the data index (24), starting from 0. 
                for idx, col_name in enumerate(col_names):
                    self._colnames[idx] = self.strip_col_name(col_name)

                for row in reader:
                    #holds the intensities
                    intensities = {}

                    # ensure there is actual data in the peak file
                    if len(row) > self.DATA_OFFSET:
                        med_mz = float(row[4])
                        med_rt = float(row[5])
                        compound = str(row[8])
                        category = str(row[10])
                        rt_diff = float(row[12])
                        parent = float(row[14])

                        #for all the data rows
                        for col in range(24, len(row)):
                            cname = self._colnames[col - self.DATA_OFFSET][0]
                            time = self._colnames[col - self.DATA_OFFSET][1]

                            #don't include blank samples
                            if "blank" in cname:
                                continue
                            
                            #if we have not seen this test, add as first value in test
                            if cname in intensities:
                                intensities[cname][time] = float(row[col])
                            #else add to tests
                            else:
                                intensities[cname] = {time: float(row[col])}

                        peak = peak_module.Peak(med_mz, med_rt, compound, \
                            category, rt_diff, parent, intensities)
                        peaks.append(peak)


        except IndexError as ex:
            print("Error reading in csv file. Error message: {}".format(str(ex)))
            return None

        return peaks

    def strip_col_name(self, col_name):
        """ returns the column name and time of T-value """
        time_re = r"t[0-9]+"
        findstr = "hilicneg15_"
        index = col_name.find(findstr, 0, len(col_name))

        if index != -1:
            cutoff = index + len(findstr)
            sample_name = col_name[cutoff:]
            sample_name = sample_name.replace(".mzxml", "")
            times = re.findall(time_re, sample_name)
            if times:
                time = str(times[0])
            else:
                time = "mid"

            #remove t# from end of sample name
            time_cutoff = sample_name.find(time, 0, len(sample_name))
            if index != -1:
                sample_name = sample_name[0:time_cutoff-1]
        else:
            return (-1, None)

        return (sample_name, time)

    def clean_peaks(self, peaks, max_rt_diff, ratio):
        """ """
        bad_peaks = []
        for peak in peaks:
            if not peak.verify_rt_diff(max_rt_diff):
                bad_peaks.append(peak)
                continue

            

    def write_peaks_csv(self, peaks, filename):
        """ Writes a list of peaks to csv file """
        if isinstance(peaks, list):
            if peaks and isinstance(peaks[0], peak_module.Peak):
                try:
                    ## should add a regex to check filename
                    with open(filename, "w+") as csvfile:
                        csvwriter = csv.writer(csvfile, delimiter="\t", quotechar="\"")
                        row = ["medMz", "medRt", "compound", "category", "rt_diff", "parent"]

                        #first write the columns as they appear in peaks
                        for colname, tests in peaks[0].intensities.items():
                            for test_time, _ in tests.items():
                                row.append(colname + "_" + test_time)

                        
                        csvwriter.writerow(row)

                        for peak in peaks:
                            row = [str(peak.med_mz), str(peak.med_rt), str(peak.compound), str(peak.category), str(peak.rt_diff), str(peak.parent)]
                            
                            intensities = []

                            for _, tests in peak.intensities.items():
                                for _, value in tests.items():
                                    intensities.append(value)

                            row = row + [str(intensity) for intensity in intensities]
                            #print(row)
                            csvwriter.writerow(row)

                except Exception as ex:
                    print("Error writing csv file...{}".format(str(ex)))

            else:
                if not peaks == 0:
                    print("Attempted to write empty peaks list.")
                if not isinstance(peaks[0], peak_module.Peak):
                    print("Received unknown list element type. Exiting.")

                return

        else:
            print("Input must be a list of Peak type.")

        return


        