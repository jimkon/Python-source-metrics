# Python Source Metrics

A tool that analyses a Python's project source files and calculate useful metrics and graphs. 
The main goal of the metrics is to reflect information about the structure of the code, the dependencies and 
also the relations of the objects it contains such as modules and classes. This could help on improving the 
quality of the code, fix vulnerable design choices and clean the codebase. 

More specifically, this app can output in a website form the insights about:
* the **distribution of the number of lines of code** for packages, modules, classes and functions. This can help identify
god-objects and unclassified code
* **UML Class** and **Class Relation diagrams** to help users understand the structure and the relation of objects
* detailed insights about the module-level imports (**import statements**) like most imported external or internal 
packages and modules, invalid imports and unused internal modules
* detailed **information and diagrams around dependencies** to help better understand how code is designed,
highly dependent and vulnerable points of the architecture and general information about how it is structured

## How to use
After cloning this project, change to `Python-source-metrics` directory and run `docker-compose up`. Then open [this
 URL](http://localhost:5001/).