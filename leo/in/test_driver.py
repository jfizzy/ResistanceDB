from filereader import FileReader


def main():
    fr = FileReader("element_weights.csv")
    filename = "../../files/known_markers/2017_05_10RG_HILIC15-Neg_MSMLS-List.csv"
    fr.parseKM(filename)

if __name__ == "__main__":
    main()
