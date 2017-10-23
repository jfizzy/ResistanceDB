# ResistanceDB
ResistanceDB Project

## :two_men_holding_hands: Authors ##
Tyrone Lagore and James MacIsaac

## :arrow_backward: Prologue ##
We will update this readme as the project progresses with more technical information about the project and how to run it.

## :bookmark: Context ##
The Lewis Research Group is investigating the connection between metabolic adaptation and virulence of human pathogens. Using Mass Spectrometry, they aim to help reduce the time it takes to identify high risk patients by interpreting the results of tests on infection strains. The process developed has proven to be more efficient than currently implemented methods, and speeding up the analysis of data will allow for even faster results. Currently, extensive analysis is performed by lab technicians on data produced by MAVEN (Metabolomic Analysis and Visualization Engine). Our research project aims to automate the repetitive work done in the process of data analysis performed by lab technicians. 

## :soccer: Goals ##
The initial objective is to build a tool that takes as input a configuration file of known bio-markers as well as an input XML file of ‘good’ peaks to be compared against these markers. The output will be a resulting file containing information on how each peak compares to its most similar benchmark in the configuration. Our belief is that this will be the optimal approach to this problem, and will lead to a solution that is reliable and ready to be scaled up.
 
The extension to this first objective will be to adapt the tool to use a database management system in order to keep a running history of both known marker files, as well as the results produced by these markers against any given data file and its configuration parameters. This will be a valuable asset for the future of the greater project.


## :pencil: Method ## 
We intend to use Python for the majority of the application programing, but will remain open minded about using the proper language for the task at hand. The known marker files will be read into the program with each individual run. Time permitting, we aim to move the storage of all data acquired by the program into a database.
