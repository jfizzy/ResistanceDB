# ResistanceDB
ResistanceDB Project

## Usage Instructions ##
There are 3 tools in this repository, also included are a list of sample files. The tools are called Mia, Leo, and Pablo. **Please note that you will not be able to use Mia to perform actual raw conversion without the Thermo Scientific Xcalibur software installed, however you can start her**.

### Mia ###
Please note that Mia was developed for a Windows environment. This setup guide assumes a windows environment and Python3.6. Although the GUI will work on Linux based systems, it is not supported.

To run Mia, enter the Mia directory and create a virtual environment:
`virvualenv .miavenv`
Activate the virtual environment
`.\.miaenv\Sources\activate`
Run mia
`python3.6 mia.pyw`


## :two_men_holding_hands: Authors ##
Tyrone Lagore and James MacIsaac

## :bookmark: Context ##
The Lewis Research Group is investigating the connection between metabolic adaptation and virulence of human pathogens. Using Mass Spectrometry, they aim to help reduce the time it takes to identify high risk patients by interpreting the results of tests on infection strains. The process developed has proven to be more efficient than currently implemented methods, and speeding up the analysis of data will allow for even faster results. Currently, extensive analysis is performed by lab technicians on data produced by MAVEN (Metabolomic Analysis and Visualization Engine). Our research project aims to automate the repetitive work done in the process of data analysis performed by lab technicians. 

## :soccer: Goals ##
The initial objective is to build a tool that takes as input a configuration file of known bio-markers as well as an input XML file of ‘good’ peaks to be compared against these markers. The output will be a resulting file containing information on how each peak compares to its most similar benchmark in the configuration. Our belief is that this will be the optimal approach to this problem, and will lead to a solution that is reliable and ready to be scaled up.
 
The extension to this first objective will be to adapt the tool to use a database management system in order to keep a running history of both known marker files, as well as the results produced by these markers against any given data file and its configuration parameters. This will be a valuable asset for the future of the greater project.
