import csv
import re
from sympy import sympify

class FileReader:

    """ """
    def __init__(self, elements):
        """ 
        init :  expects a file 'elements' that contains the weights of the 
        periodic table
        """
        if not elements.endswith(".csv"):
            raise FileReaderException("Elements file must be a csv file.")


        self._elements = {}

        with open(elements, 'rt') as csvfile:
            reader = csv.reader(open(elements, 'rt'))
            
            for line in reader:
                self._elements[line[0]] = line[1]

        

    def parseFile(self, filename):
        """ determines the type  """

    def parseMZXML(self, filename):
        """ 
        parzeMZXML parses a mzxml file 
        in: filename of an MZXML file
        out: a sample data structure: structure to be determined

        Unknown: Can an mzxml file be too large to store in memory? 
        How many mzxml files do we have to store at a given time?
        """

    def parseKM(self, filename):
        """ 
        parse KM parses a known markers file
        in: filename of a known markers file
        out: a list containing the contents of the known marker file
             None if filename did not end with csv or an exception is thrown
        """

        if not filename.endswith(".csv"):
            return None

        out = []
        
        try:
            with open(filename, 'rt') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')

                #skip header row
                next(reader, None)

                #format is compound, formula, retention time, category
                for row in reader:
                    row[1] = str(self.getMolarMass(row[1]))
                    print(',\t'.join(row))

                    
                     
        except Exception as e:
            print(e)
            return None


    def getMolarMass(self, formula):
        """ gets the molar mass of a given formula """

        mass = re.sub(r'(\d+)', r'\1+', formula)
        mass = re.sub(r'([a-zA-Z])', r'\1*', mass)

        #if molecular formula ended with a digit
        if mass.endswith('+'):
            mass = mass[:-1]

        #if molecular formula ended with a character
        elif mass.endswith('*'):
            mass = mass + "1"

        #substitute element symbol with molecular weight
        pattern = re.compile('|'.join(self._elements.keys()))
        mass = pattern.sub(lambda x: self._elements[x.group()], mass)

        weight = sympify(mass).evalf()
        return weight
    

class FileReaderException(Exception):
    def __init(self, message):
        self._message = message

    def __str__(self):
        return repr(self._message)
