# R-SNA - LibreSoft

Social Network Analysis for software projects at different levels of granularity.
GraphDataCreator.py is based on Christian Coré Ramiro Shell-Bash script.
Note: This program uses Git and Ctags, please install both programs before running GraphDataCreator
Note 2: A new Super-script has been added to handle wide time-periods, 'SuperGraphDataCreator.py' that divides that time period into shorter periods.

Usage:
$python GraphDataCreator.py -f (starting-date of study[1]) -t (ending date of study[2]) -r (url-repo)/(reuse[3])

[1],[2] Starting and ending date of study format: YYYY-MM-DD
[1] When starting date is empty, study starts at the beginning of times.
[2] When ending date is empty, current date will be chosen.

[3] In '-r' field, 'reuse' Re-uses a previously downloaded repository (It has to be a folder called 'Repository' in directory)

Example:
$python GraphDataCreator.py -f 2014-01-01 -t 2014-03-31 -r https://github.com/GNOME/gedit

Output:

This program creates two main folders, Data and Repository,
and outputs two csv files (DataFiles.csv and DataMethods.csv) in directory Data/output

Other options:

  -h  prints help page.
  -v  Verbose mode.


Usage for SuperGraphDataCreator.py:
$python SuperGraphDataCreator.py
-This program uses a configuration file named 'graph_settings.py' ,included in this repo, which has to be in the same folder that SuperGraphDataCreator.py and GraphDataCreator.py
-Its output is one folder named 'final-outputs' and in this folder creates one sub-folder for each period

Example of configuration file:
config = {}
config['v'] = True  # Verbose
config['f'] = '2005-06-01'  # Starting date of study
config['t'] = '2011-11-18'  # Ending date of study
config['r'] = "https://github.com/GNOME/gedit"  # Repository URL
config['h'] = False  # Shows help
config['p'] = 8  # Months by period
