from leo.fileparser import fileparser


def main():
    #fr = FileReader("element_weights.csv")
    fp = fileparser.FileParser()
    peaks = fp.parse_peaks_file("files/peaks/peaks_wknown.tab")
    fp.write_peaks_csv(peaks, "test.csv")
    #filename = "../../files/known_markers/2017_05_10RG_HILIC15-Neg_MSMLS-List.csv"
    #fr.parseKM(filename)

if __name__ == "__main__":
    main()
