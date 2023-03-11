# Python Source Metrics

A tool that analyses a Python's project source files and calculate useful metrics and graphs. 
The main goal of the metrics is to reflect information about the structure of the code, the dependencies and 
also the relations of the objects it contains such as modules and classes. This could help on improving the 
quality of the code, fix vulnerable design choices and clean the codebase. 

## How to use
After cloning this project, execute the `pystruct.py` file and point it to the directory or git repository containing
the Python codebase you want to analyse.   
**Example**  
`python pystruct.py https://github.com/jimkon/Python-source-metrics.git`

This will make a copy of all the python files in the codebase and start analysing them. The end result will be a 
`FullReport.html` file in the report_files/obj directory that gets created after the execution.